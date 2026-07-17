import ontology
from ontology import (
    model, FinancialSnapshot, SECStatement, Company, CreditRating, Bond,
    EarningsEstimate, BankruptcyRisk, ESGRating, IndexConstituent, Person,
    BoardMember, InsiderTransaction, InstitutionalHolding, Product, Patent,
    VCInvestment, FederalContract, LayoffEvent, BuybackRecord, TradeCredit,
    MADeal, AviationIncident, AviationFleetOrder, AviationPassengerTraffic,
    AviationRoutePerformance, BiotechFunding, ClinicalTrial, DiseaseBurden,
    DrugApproval, PharmaFinancials, ChipMarketMetric, SemiconductorFinancials,
    ChipPrice, SemiconductorExportControl, SemiconductorFabCapacity, NewsHeadline,
    SentimentRecord, Commodity, PriceSeries, OHLCV, Country, SovereignRating,
    CountryMacro, MacroIndicator, SectorReturn
)

# Load all logical submodules to register the 240 derived rules in Swan Datalog
import rules.profitability
import rules.solvency
import rules.governance
import rules.macro
import rules.valuation
import rules.capital

print("=== SWAN LOGICAL RULES IMPORTED AND REGISTERED SUCCESSFULLY FROM MODULAR PACKAGE ===")
