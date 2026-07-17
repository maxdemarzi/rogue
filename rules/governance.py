import ontology
from ontology import (
    model, Company, FinancialSnapshot, InsiderTransaction, Person,
    EarningsEstimate, BankruptcyRisk, Product, ESGRating, MADeal,
    FederalContract, LayoffEvent
)
from pyrel_duckdb import Float, Integer, String, Boolean

# --- 5. Governance & Interlock Risk Rules ---

# Conviction Score is a rating tracking insider trading conviction intensity.
# Rationale: Helps spot high-risk opportunistic insider trading behavior.
InsiderTransaction.conviction_score = model.Property(f"{InsiderTransaction} has {Float:conviction_score}", column_name="conviction_score")

# Governance Risk flags companies with highly dispersed pay structures and active, high-conviction insider sales.
# Rationale: Potential agency risk indicator.
Company.is_governance_risk = model.Property(f"{Company} is governance risk {Boolean:is_governance_risk}")
model.define(Company.is_governance_risk(True)).where(
    FinancialSnapshot.ticker == Company.ticker,
    FinancialSnapshot.worker_pay_ratio_dispersion > 300.0,
    InsiderTransaction.ticker == Company.ticker,
    InsiderTransaction.conviction_score > 0.8
)

# Interlocked Director flags directors holding more than 2 board seats.
# Rationale: Flags potential conflict of interest and bandwidth constraints.
Person.is_interlocked_director = model.Property(f"{Person} is interlocked director {Boolean:is_interlocked_director}")
model.define(Person.is_interlocked_director(True)).where(Person.boards_count > 2)

# Insider Quiet Window Trade flags insider trades executing during earnings estimate periods.
# Rationale: Compliance risk check for potential trades on material non-public information (MNPI).
InsiderTransaction.is_insider_quiet_window_trade = model.Property(f"{InsiderTransaction} is quiet window trade {Boolean:is_insider_quiet_window_trade}")
model.define(InsiderTransaction.is_insider_quiet_window_trade(True)).where(
    EarningsEstimate.ticker == InsiderTransaction.ticker
)

# Insider Disposed flags transactions where insiders sold stock.
InsiderTransaction.is_disposed = model.Property(f"{InsiderTransaction} is disposed {Boolean:is_disposed}")
model.define(InsiderTransaction.is_disposed(True)).where(InsiderTransaction.acquired_disposed_code == "D")

# Insider Acquired flags transactions where insiders purchased stock.
InsiderTransaction.is_acquired = model.Property(f"{InsiderTransaction} is acquired {Boolean:is_acquired}")
model.define(InsiderTransaction.is_acquired(True)).where(InsiderTransaction.acquired_disposed_code == "A")


# --- 6. B2B Value-Chain & Contagion Risk Rules ---

# Supplies To maps supplier-customer relationships between firms.
Company.supplies_to = model.Relationship(f"{Company} supplies to {Company}")
model.define(Company.supplies_to(Company)).where(
    Product.supplier_name == Company.company_name,
    Company.company_name == Product.supplier_name
)

# Bankruptcy Risk Probability maps probability of bankruptcy locally on Company.
Company.bankruptcy_risk_probability = model.Property(f"{Company} bankruptcy risk {Float:bankruptcy_risk_probability}")
model.define(Company.bankruptcy_risk_probability(BankruptcyRisk.probability * 1.0)).where(
    BankruptcyRisk.ticker == Company.ticker
)

# Distressed Supplier flags suppliers linked to customers that are in severe distress or default risks.
# Rationale: Identifies potential value chain contagion.
Company.is_distressed_supplier = model.Property(f"{Company} is distressed supplier {Boolean:is_distressed_supplier}")
model.define(Company.is_distressed_supplier(True)).where(
    Company.supplies_to(Company),
    Company.bankruptcy_risk_probability > 0.10
)

# DSO and DPO local aliases.
Company.dso = model.Property(f"{Company} dso {Float:dso}")
model.define(Company.dso(FinancialSnapshot.days_sales_outstanding_dso * 1.0)).where(FinancialSnapshot.ticker == Company.ticker)

Company.dpo = model.Property(f"{Company} dpo {Float:dpo}")
model.define(Company.dpo(FinancialSnapshot.days_payable_outstanding_dpo * 1.0)).where(FinancialSnapshot.ticker == Company.ticker)

# Days Sales Outstanding Mismatch tracks collection cycle gaps relative to payment cycles.
# Rationale: Positive mismatches indicate working capital cash sinks.
Company.days_sales_outstanding_mismatch = model.Property(f"{Company} dso mismatch {Float:days_sales_outstanding_mismatch}")
model.define(Company.days_sales_outstanding_mismatch(Company.dso - Company.dpo))

# Value Chain Liquidity Gap calculates liquidity shortfall caused by value chain payment mismatches.
# Rationale: Rationale tracks operating finance constraints.
Company.value_chain_liquidity_gap = model.Property(f"{Company} value chain gap {Float:value_chain_liquidity_gap}")
model.define(Company.value_chain_liquidity_gap(Company.days_sales_outstanding_mismatch * 1.0))

# Supplier Insolvency Alert alerts if a critical upstream partner has high credit risks.
# Rationale: Early procurement risk warning.
Company.supplier_insolvency_alert = model.Property(f"{Company} supplier insolvency alert {Boolean:supplier_insolvency_alert}")
model.define(Company.supplier_insolvency_alert(True)).where(
    Company.is_distressed_supplier == True
)

# Working Capital Squeeze flags companies with large payment collection gaps exceeding 30 days.
# Rationale: Identifies firms forced to finance customer receivables.
Company.working_capital_squeeze = model.Property(f"{Company} working capital squeeze {Boolean:working_capital_squeeze}")
model.define(Company.working_capital_squeeze(True)).where(Company.days_sales_outstanding_mismatch > 30.0)

# Value Chain Restructuring Threat estimates cost impact from counterparty reorganization.
# Rationale: Forward risk impact metric.
Company.value_chain_restructuring_threat = model.Property(f"{Company} restructuring threat {Float:value_chain_restructuring_threat}")
model.define(Company.value_chain_restructuring_threat(Company.bankruptcy_risk_probability * 1.0))


# --- 6b. ESG, Mergers & Acquisitions, Federal Contracts & Layoff Rules ---

# ESG Leader flags companies with outstanding low environmental, social, and governance risk ratings.
# Rationale: Excellent corporate governance indicator.
Company.is_esg_leader = model.Property(f"{Company} is ESG leader {Boolean:is_esg_leader}")
model.define(Company.is_esg_leader(True)).where(
    ESGRating.symbol == Company.ticker,
    ESGRating.total_score < 15.0
)

# ESG Laggard flags companies carrying massive risk exposure scores across sustainability metrics.
# Rationale: High compliance and reputational risk profile.
Company.is_esg_laggard = model.Property(f"{Company} is ESG laggard {Boolean:is_esg_laggard}")
model.define(Company.is_esg_laggard(True)).where(
    ESGRating.symbol == Company.ticker,
    ESGRating.total_score > 35.0
)

# High ESG Controversy flags companies undergoing heavy controversy issues.
# Rationale: Reputational risk indicator.
Company.is_high_esg_controversy = model.Property(f"{Company} is high controversy {Boolean:is_high_esg_controversy}")
model.define(Company.is_high_esg_controversy(True)).where(
    ESGRating.symbol == Company.ticker,
    ESGRating.controversy_level == "High Controversy Level"
)

# Severe ESG Controversy flags companies involved in catastrophic controversies.
# Rationale: Extreme risk factor for structural asset adjustments.
Company.is_severe_esg_controversy = model.Property(f"{Company} is severe controversy {Boolean:is_severe_esg_controversy}")
model.define(Company.is_severe_esg_controversy(True)).where(
    ESGRating.symbol == Company.ticker,
    ESGRating.controversy_level == "Severe Controversy Level"
)

# Active Acquirer flags companies pursuing corporate growth via consolidations and buyouts.
# Rationale: Tracks aggressive capital expansion.
Company.is_active_acquirer = model.Property(f"{Company} is active acquirer {Boolean:is_active_acquirer}")
model.define(Company.is_active_acquirer(True)).where(
    MADeal.purchaser_name == Company.company_name
)

# Acquisition Target flags companies undergoing buyouts by competitors.
# Rationale: Important event-driven investing catalyst.
Company.is_acquired_target = model.Property(f"{Company} is acquired target {Boolean:is_acquired_target}")
model.define(Company.is_acquired_target(True)).where(
    MADeal.purchased_name == Company.company_name
)

# Mega Deal Participant flags target companies involved in buyouts exceeding $10 Billion.
# Rationale: Highlights structural industry shift events.
Company.is_mega_deal_participant = model.Property(f"{Company} is mega deal participant {Boolean:is_mega_deal_participant}")
model.define(Company.is_mega_deal_participant(True)).where(
    MADeal.purchased_name == Company.company_name,
    MADeal.value_billions > 10.0
)

# Has Active Federal Contracts flags companies securing national procurement backing.
# Rationale: Strong systemic revenue streams buffer.
Company.has_active_federal_contracts = model.Property(f"{Company} has active federal contracts {Boolean:has_active_federal_contracts}")
model.define(Company.has_active_federal_contracts(True)).where(
    FederalContract.parent_ticker == Company.ticker
)

# Large Federal Contractor flags partners holding massive single contracts exceeding $5 Million.
# Rationale: High single-customer dependency alert.
Company.is_large_federal_contractor = model.Property(f"{Company} is large federal contractor {Boolean:is_large_federal_contractor}")
model.define(Company.is_large_federal_contractor(True)).where(
    FederalContract.parent_ticker == Company.ticker,
    FederalContract.award_amount > 5000000.0
)

# Has Recent Layoffs flags companies that announced labor contractions.
# Rationale: Signals operational stress or margin defense restructuring.
Company.has_recent_layoffs = model.Property(f"{Company} has recent layoffs {Boolean:has_recent_layoffs}")
model.define(Company.has_recent_layoffs(True)).where(
    LayoffEvent.company_name == Company.company_name
)

# High Severity Layoffs flags companies cutting workforce by more than 15%.
# Rationale: Signals severe business model contraction.
Company.is_high_severity_layoff_company = model.Property(f"{Company} is high severity layoff company {Boolean:is_high_severity_layoff_company}")
model.define(Company.is_high_severity_layoff_company(True)).where(
    LayoffEvent.company_name == Company.company_name,
    LayoffEvent.percentage_laid_off > 0.15
)

# Quality Compounder flags companies that are both ESG leaders and active acquirers.
# Rationale: Higher-tier rule building on is_esg_leader and is_active_acquirer.
Company.is_quality_compounder = model.Property(f"{Company} is quality compounder {Boolean:is_quality_compounder}")
model.define(Company.is_quality_compounder(True)).where(
    Company.is_esg_leader == True,
    Company.is_active_acquirer == True
)

# Vulnerable Supplier flags supplier companies suffering from both customer distress and internal layoffs.
# Rationale: Higher-tier rule building on is_distressed_supplier and has_recent_layoffs.
Company.is_vulnerable_supplier = model.Property(f"{Company} is vulnerable supplier {Boolean:is_vulnerable_supplier}")
model.define(Company.is_vulnerable_supplier(True)).where(
    Company.is_distressed_supplier == True,
    Company.has_recent_layoffs == True
)

# Value Chain Systemic Risk flags companies having critical downstream dependencies on highly vulnerable suppliers.
# Rationale: Higher-tier rule building on supplies_to and is_vulnerable_supplier.
Company.value_chain_systemic_risk = model.Property(f"{Company} has value chain systemic risk {Boolean:value_chain_systemic_risk}")
model.define(Company.value_chain_systemic_risk(True)).where(
    Company.supplies_to(Company),
    Company.is_vulnerable_supplier == True
)

# Product Gross Margin evaluates pricing markup efficiency.
# Rationale: Core operational unit economics driver.
Product.gross_margin = model.Property(f"{Product} gross margin {Float:gross_margin}")
model.define(Product.gross_margin((Product.price - Product.manufacturing_costs) / Product.price))

# High Defect Product flags items with quality failure rates exceeding 3%.
# Rationale: Quality control and brand liability alert.
Product.is_high_defect = model.Property(f"{Product} is high defect {Boolean:is_high_defect}")
model.define(Product.is_high_defect(True)).where(
    Product.defect_rate > 0.03
)

# Highly Profitable Product flags items generating high unit gross margins exceeding 40%.
# Rationale: Primary cash-driver products.
Product.is_highly_profitable_product = model.Property(f"{Product} is highly profitable product {Boolean:is_highly_profitable_product}")
model.define(Product.is_highly_profitable_product(True)).where(
    Product.gross_margin > 0.40
)

# Profitable Product Portfolio flags companies that have successfully scaled highly profitable unit products.
# Rationale: Higher-tier rule building on is_highly_profitable_product.
Company.has_profitable_product_portfolio = model.Property(f"{Company} has profitable portfolio {Boolean:has_profitable_product_portfolio}")
model.define(Company.has_profitable_product_portfolio(True)).where(
    Product.supplier_name == Company.company_name,
    Product.is_highly_profitable_product == True
)

# Quality Control Issues flags supplier companies manufacturing products with severe failure/defect rates.
# Rationale: Higher-tier rule building on is_high_defect.
Company.has_quality_control_issues = model.Property(f"{Company} has quality control issues {Boolean:has_quality_control_issues}")
model.define(Company.has_quality_control_issues(True)).where(
    Product.supplier_name == Company.company_name,
    Product.is_high_defect == True
)

# High Conviction Insider Sales flags companies where active transactions capture severe management selling conviction.
# Rationale: Higher-tier nested rule building on is_disposed.
Company.has_high_conviction_insider_sales = model.Property(f"{Company} has high conviction sales {Boolean:has_high_conviction_insider_sales}")
model.define(Company.has_high_conviction_insider_sales(True)).where(
    InsiderTransaction.ticker == Company.ticker,
    InsiderTransaction.is_disposed == True,
    InsiderTransaction.conviction_score > 0.85
)

# High Conviction Insider Purchases flags companies where management aggressively buys back their own stock.
# Rationale: Higher-tier nested rule building on is_acquired.
Company.has_high_conviction_insider_buys = model.Property(f"{Company} has high conviction buys {Boolean:has_high_conviction_insider_buys}")
model.define(Company.has_high_conviction_insider_buys(True)).where(
    InsiderTransaction.ticker == Company.ticker,
    InsiderTransaction.is_acquired == True,
    InsiderTransaction.conviction_score > 0.85
)

# Insider Sentiment Divergence flags companies where different executive layers display opposing trade signals.
# Rationale: Higher-tier nested rule building on has_high_conviction_insider_sales and has_high_conviction_insider_buys.
Company.insider_sentiment_divergence = model.Property(f"{Company} has insider divergence {Boolean:insider_sentiment_divergence}")
model.define(Company.insider_sentiment_divergence(True)).where(
    Company.has_high_conviction_insider_sales == True,
    Company.has_high_conviction_insider_buys == True
)

# High Governance Risk (ESG) flags companies with weak internal controls and heavy regulatory risk exposures.
# Rationale: ESG compliance indicator.
Company.is_high_governance_risk_esg = model.Property(f"{Company} is high governance risk ESG {Boolean:is_high_governance_risk_esg}")
model.define(Company.is_high_governance_risk_esg(True)).where(
    ESGRating.symbol == Company.ticker,
    ESGRating.governance_score > 10.0
)

# High Environmental Risk flags companies carrying heavy carbon/ecological liability burdens.
# Rationale: Geopolitical carbon tax and compliance threat indicator.
Company.is_high_environmental_risk = model.Property(f"{Company} is high environmental risk {Boolean:is_high_environmental_risk}")
model.define(Company.is_high_environmental_risk(True)).where(
    ESGRating.symbol == Company.ticker,
    ESGRating.environment_score > 15.0
)

# ESG Risk Alert flags companies carrying severe compound exposures across environmental and governance metrics.
# Rationale: Higher-tier nested rule building on is_high_governance_risk_esg and is_high_environmental_risk.
Company.is_esg_risk_alert = model.Property(f"{Company} has ESG risk alert {Boolean:is_esg_risk_alert}")
model.define(Company.is_esg_risk_alert(True)).where(
    Company.is_high_governance_risk_esg == True,
    Company.is_high_environmental_risk == True
)

# Critical Layoff Stress flags restructured companies that are also facing severe short-term default risks.
# Rationale: Higher-tier nested rule building on has_recent_layoffs and is_financial_distressed.
Company.is_critical_layoff_stress = model.Property(f"{Company} has critical layoff stress {Boolean:is_critical_layoff_stress}")
model.define(Company.is_critical_layoff_stress(True)).where(
    Company.has_recent_layoffs == True,
    FinancialSnapshot.ticker == Company.ticker,
    FinancialSnapshot.is_financial_distressed == True
)




