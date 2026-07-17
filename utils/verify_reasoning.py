import os
import sys

# Ensure rogue directory is in the PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

def run_verification_suite():
    print("=" * 60)
    print("       ROGO AI ANALYST - PHASE 3 VERIFICATION SUITE")
    print("=" * 60)
    
    success = True
    
    # 1. Merton Simulator
    print("\n[1/10] Running Merton Credit Default Simulator...")
    try:
        import merton_simulator
        merton_simulator.simulate_merton()
        print("  --> SUCCESS")
    except Exception as e:
        print(f"  --> FAILED: {e}")
        success = False
        
    # 2. Path Reasoner (PageRank and WCC)
    print("\n[2/10] Running Graph Contagion and Board Interlocks Pathfinder...")
    try:
        import path_reasoner
        pr_df = path_reasoner.run_pagerank()
        wcc_df = path_reasoner.run_wcc()
        deg_df = path_reasoner.run_board_centrality()
        print(f"  --> PageRank Rows: {len(pr_df)}, WCC Rows: {len(wcc_df)}, Board Centrality Rows: {len(deg_df)}")
        print("  --> SUCCESS")
    except Exception as e:
        print(f"  --> FAILED: {e}")
        success = False
        
    # 3. GNN Model
    print("\n[3/10] Running GNN Multiple Forecasters Training...")
    try:
        import gnn_model
        r_gnn, e_gnn = gnn_model.train_forecasters()
        print("  --> SUCCESS")
    except Exception as e:
        print(f"  --> FAILED: {e}")
        success = False
        
    # 4. GNN Explainers
    print("\n[4/10] Running GNN Explainer and Attribution Trace...")
    try:
        import gnn_explainers
        exps = gnn_explainers.explain_company_predictions("AIR")
        print(f"  --> Revenue Node Attribution Size: {len(exps['revenue']['nodes'])}")
        print("  --> SUCCESS")
    except Exception as e:
        print(f"  --> FAILED: {e}")
        success = False
        
    # 5. Optimizer (LBO MIP)
    print("\n[5/10] Running LBO Prescriptive MIP Optimizer...")
    try:
        import optimizer
        companies, info = optimizer.run_lbo_optimization()
        print(f"  --> Optimal Targets Selected: {len(companies)}")
        print("  --> SUCCESS")
    except Exception as e:
        print(f"  --> FAILED: {e}")
        success = False
        
    # 6. Merger Accretion Solver
    print("\n[6/10] Running M&A Combined EPS accretion solver...")
    try:
        import merger_solver
        res = merger_solver.solve_merger_accretion("AIR", "AIR", offer_price=25.0)
        print(f"  --> Standalone EPS: {res['acquirer_standalone_eps']:.4f}, Combined EPS: {res['combined_eps']:.4f}")
        print("  --> SUCCESS")
    except Exception as e:
        print(f"  --> FAILED: {e}")
        success = False
        
    # 7. Path Tracer (Bayesian leak tracer)
    print("\n[7/10] Running Insider pre-event leak tracer...")
    try:
        import path_tracer
        leak_paths = path_tracer.trace_information_leak("AIR")
        print(f"  --> Traced suspects count: {len(leak_paths)}")
        print("  --> SUCCESS")
    except Exception as e:
        print(f"  --> FAILED: {e}")
        success = False
        
    # 8. Macro Optimizer
    print("\n[8/10] Running Macro Carry Trade LP Optimizer...")
    try:
        import macro_optimizer
        allocs, info = macro_optimizer.optimize_carry_trade()
        print(f"  --> Allocated currencies: {len(allocs[allocs['allocation'] > 0])}")
        print("  --> SUCCESS")
    except Exception as e:
        print(f"  --> FAILED: {e}")
        success = False
        
    # 9. Live Excel Modeler
    print("\n[9/10] Running Live Excel Modeler...")
    try:
        import live_modeler
        live_modeler.generate_live_excel()
        print("  --> SUCCESS")
    except Exception as e:
        print(f"  --> FAILED: {e}")
        success = False
        
    # 10. Citation Audit Engine
    print("\n[10/10] Running Citation Audit Engine...")
    try:
        import citation_engine
        cite_info = citation_engine.locate_source_row("E9")
        print(f"  --> Audited cell type: {cite_info['type']}, formula: {cite_info['formula']}")
        print("  --> SUCCESS")
    except Exception as e:
        print(f"  --> FAILED: {e}")
        success = False
        
    print("\n" + "=" * 60)
    if success:
        print("       ALL SYSTEM REASONING MODULES VERIFIED SUCCESSFULLY!")
    else:
        print("       SOME REASONING MODULES FAILED VERIFICATION.")
    print("=" * 60)
    
if __name__ == "__main__":
    run_verification_suite()
