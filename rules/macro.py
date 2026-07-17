import ontology
from ontology import (
    model, Country, SovereignRating, AviationPassengerTraffic, Company,
    AviationIncident, SemiconductorExportControl, PharmaFinancials,
    SemiconductorFinancials, BiotechFunding, DrugApproval
)
from pyrel_duckdb import Float, Integer, String, Boolean

# --- 7. Macro, Carry Trade & Arbitrage Rules ---

# Economic Freedom Rank maps freedom scores from heritage indexes.
# Rationale: Measures corporate regulatory safety boundaries.
Country.economic_freedom_rank = model.Property(f"{Country} economic freedom rank {Float:economic_freedom_rank}")
model.define(Country.economic_freedom_rank(Country.business_freedom * 1.0))

# Capacity Utilization maps flight seat loading factors.
# Rationale: Key efficiency metric representing asset usage efficiency.
Company.airline_capacity_utilization = model.Property(f"{Company} airline capacity {Float:airline_capacity_utilization}")
model.define(Company.airline_capacity_utilization(AviationPassengerTraffic.load_factor * 1.0)).where(
    AviationPassengerTraffic.airline == Company.company_name
)

# High Incident Airline flags carriers linked to severe fatal accidents.
# Rationale: Flags severe operational, safety and reputational liabilities.
Company.is_high_incident_airline = model.Property(f"{Company} is high incident airline {Boolean:is_high_incident_airline}")
model.define(Company.is_high_incident_airline(True)).where(
    AviationIncident.airline == Company.company_name,
    AviationIncident.fatalities > 50
)


# --- 8. Sector Specialty Ratios (Aviation, Pharma, Semiconductor) ---

# R&D Intensity (Pharma) is biotech/pharma R&D spend relative to revenue.
# Rationale: Measures research focus of pharma developers.
Company.pharma_rnd_intensity = model.Property(f"{Company} has pharma R&D intensity {Float:pharma_rnd_intensity}")
model.define(Company.pharma_rnd_intensity(PharmaFinancials.rd_spend / PharmaFinancials.revenue)).where(
    PharmaFinancials.company_name == Company.company_name
)

# R&D Intensity (Semiconductor) is chip R&D spend relative to revenue.
# Rationale: Measures innovation investments in tech manufacturing.
Company.semiconductor_rnd_intensity = model.Property(f"{Company} has semiconductor R&D intensity {Float:semiconductor_rnd_intensity}")
model.define(Company.semiconductor_rnd_intensity(SemiconductorFinancials.rnd_spending / SemiconductorFinancials.revenue)).where(
    SemiconductorFinancials.company_name == Company.company_name
)

# Received Biotech Funding flags firms receiving venture capital or licensing capital.
# Rationale: Vital funding resource signals.
Company.has_received_biotech_funding = model.Property(f"{Company} received biotech funding {Boolean:has_received_biotech_funding}")
model.define(Company.has_received_biotech_funding(True)).where(
    BiotechFunding.company_name == Company.company_name
)

# Recent Drug Approval flags companies securing regulatory approvals for their therapies.
# Rationale: Key catalyst for bottom line growth.
Company.has_recent_drug_approval = model.Property(f"{Company} has drug approval {Boolean:has_recent_drug_approval}")
model.define(Company.has_recent_drug_approval(True)).where(
    DrugApproval.company == Company.company_name
)


