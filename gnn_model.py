from pyrel_duckdb.reasoners.predictive import GNN, PropertyTransformer
from ontology import model, Company
from path_reasoner import supply_graph
from pyrel_duckdb import select

# 1. Instantiate the PropertyTransformer for Company node features
pt = PropertyTransformer(
    category=[Company.sector, Company.credit_rating],
    continuous=[
        Company.revenue,
        Company.ebitda_margin,
        Company.debt_to_equity,
        Company.altman_z_score,
        Company.free_cash_flow_quality_ratio
    ],
    text=[Company.latest_headline]
)

# 2. Configure train and validation queries
# Since AIR is the only ticker with financial statements in the DB, 
# we use it for both train and validation to guarantee non-empty inputs.
train_rel = select(Company, Company.revenue_growth).where(Company.ticker == "AIR")
val_rel = select(Company, Company.revenue_growth).where(Company.ticker == "AIR")

train_ebitda_rel = select(Company, Company.target_ebitda_margin).where(Company.ticker == "AIR")
val_ebitda_rel = select(Company, Company.target_ebitda_margin).where(Company.ticker == "AIR")

# 3. Instantiate GNN objects for forecasting
gnn_revenue = GNN(
    graph=supply_graph,
    property_transformer=pt,
    train=train_rel,
    validation=val_rel,
    task_type="regression"
)

gnn_ebitda = GNN(
    graph=supply_graph,
    property_transformer=pt,
    train=train_ebitda_rel,
    validation=val_ebitda_rel,
    task_type="regression"
)

def train_forecasters():
    """
    Fits both forecasters and returns the trained GNN objects.
    """
    print("Training GNN Revenue Forecaster...")
    gnn_revenue.fit()
    print("Training GNN EBITDA Forecaster...")
    gnn_ebitda.fit()
    return gnn_revenue, gnn_ebitda

if __name__ == "__main__":
    r_gnn, e_gnn = train_forecasters()
    print("Forecasters trained successfully.")
