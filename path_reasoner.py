from pyrel_duckdb.reasoners.graph import Graph
from ontology import model, Company, SupplierRelation, Person, DirectorInterlock
from pyrel_duckdb import Float, Integer

# 1. Initialize the directed supply chain graph
supply_graph = Graph(
    model,
    directed=True,
    weighted=True,
    node_concept=Company,
    edge_concept=SupplierRelation,
    edge_src_relationship=SupplierRelation.supplier,
    edge_dst_relationship=SupplierRelation.customer,
    edge_weight_relationship=SupplierRelation.revenue_share
)

# 2. Initialize the homogeneous board interlock graph
board_graph = Graph(
    model,
    directed=False,
    weighted=False,
    node_concept=Person,
    edge_concept=DirectorInterlock,
    edge_src_relationship=DirectorInterlock.src,
    edge_dst_relationship=DirectorInterlock.dst
)

def run_pagerank():
    """
    PageRank Distress Contagion.
    """
    PR = supply_graph.pagerank(damping_factor=0.85, max_iter=20, tolerance=1e-6)
    score = Float.ref("score")
    df = model.where(PR(Company, score)).select(
        Company.ticker.alias("company_id"),
        score.alias("distress_influence")
    ).to_df()
    return df

def check_reachability(supplier_ticker, customer_ticker):
    """
    Traces downstream B2B reachability using C++ reachability caches.
    """
    CompanyA = Company.ref("a")
    CompanyB = Company.ref("b")
    df = model.where(
        CompanyA.ticker == supplier_ticker,
        CompanyB.ticker == customer_ticker,
        supply_graph.reachable(CompanyA, CompanyB, use_cache=True)
    ).select(
        CompanyA.ticker,
        CompanyB.ticker
    ).to_df()
    return len(df) > 0

def run_wcc():
    """
    Calculates Weakly Connected Components for supplier partitions.
    """
    Wcc = supply_graph.weakly_connected_component(
        use_cache=True,
        cache_table="supplier_relation_clean",
        cache_src="supplier",
        cache_tgt="customer"
    )
    comp = Integer.ref("comp")
    df = model.where(Wcc(Company, comp)).select(
        Company.ticker.alias("company_id"),
        comp.alias("component_id")
    ).to_df()
    return df

def run_board_centrality():
    """
    Extracts degree centrality on directors.
    """
    Deg = board_graph.degree(of=Person)
    centrality = Integer.ref("centrality")
    df = model.where(Deg(Person, centrality)).select(
        Person.id.alias("person_id"),
        centrality.alias("centrality")
    ).to_df()
    return df

if __name__ == "__main__":
    print("PageRank Contagion Results:")
    try:
        print(run_pagerank().head())
    except Exception as e:
        print("PageRank error:", e)
        
    print("\nSupplier Components:")
    try:
        print(run_wcc().head())
    except Exception as e:
        print("WCC error:", e)
