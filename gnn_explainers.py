from pyrel_duckdb import select
from gnn_model import gnn_revenue, gnn_ebitda

def explain_company_predictions(company_ticker):
    """
    Traces and returns attribution tables for the given company ticker
    for both the revenue and EBITDA forecasting models.
    """
    print(f"Generating predictions explanation for: {company_ticker}...")
    
    # 1. Revenue model explanation
    node_concept_rev, edge_concept_rev = gnn_revenue.explain(
        target_id=company_ticker,
        top_k=5,
        method="ood_robust",
        noise_std=0.1
    )
    df_nodes_rev = select(
        node_concept_rev.node.alias("node_id"),
        node_concept_rev.weight.alias("importance")
    ).to_df()
    
    df_edges_rev = select(
        edge_concept_rev.src.alias("src_id"),
        edge_concept_rev.dst.alias("dst_id"),
        edge_concept_rev.weight.alias("importance")
    ).to_df()
    
    # 2. EBITDA model explanation
    node_concept_eb, edge_concept_eb = gnn_ebitda.explain(
        target_id=company_ticker,
        top_k=5,
        method="ood_robust",
        noise_std=0.1
    )
    df_nodes_eb = select(
        node_concept_eb.node.alias("node_id"),
        node_concept_eb.weight.alias("importance")
    ).to_df()
    
    df_edges_eb = select(
        edge_concept_eb.src.alias("src_id"),
        edge_concept_eb.dst.alias("dst_id"),
        edge_concept_eb.weight.alias("importance")
    ).to_df()
    
    return {
        "revenue": {"nodes": df_nodes_rev, "edges": df_edges_rev},
        "ebitda": {"nodes": df_nodes_eb, "edges": df_edges_eb}
    }

if __name__ == "__main__":
    # Fit the GNNs first to ensure models are trained before explaining
    from gnn_model import train_forecasters
    train_forecasters()
    
    try:
        explanations = explain_company_predictions("AIR")
        print("\nRevenue Node Attribution Importance:")
        print(explanations["revenue"]["nodes"])
        print("\nEBITDA Edge Attribution Importance:")
        print(explanations["ebitda"]["edges"])
    except Exception as e:
        print("Explanation generation failed:", e)
