import os
import sys

# Ensure rogue directory is in the PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sandbox import exec_in_sandbox
from agent_pipeline import NexusCoordinator

def test_sandbox_prohibitions():
    print("Testing sandbox AST validation rules...")
    
    # 1. Prohibited Import Test
    bad_code_1 = "import os; print(os.getcwd())"
    try:
        exec_in_sandbox(bad_code_1)
        print("  --> FAILED: Prohibited import 'os' executed successfully!")
        return False
    except PermissionError as e:
        print(f"  --> SUCCESS: Blocked 'os' import as expected: {e}")
        
    # 2. Prohibited Call Test
    bad_code_2 = "eval('1 + 1')"
    try:
        exec_in_sandbox(bad_code_2)
        print("  --> FAILED: Prohibited function 'eval' executed successfully!")
        return False
    except PermissionError as e:
        print(f"  --> SUCCESS: Blocked 'eval' call as expected: {e}")
        
    # 3. Prohibited From Import Test
    bad_code_3 = "from sys import exit"
    try:
        exec_in_sandbox(bad_code_3)
        print("  --> FAILED: Prohibited import from 'sys' executed successfully!")
        return False
    except PermissionError as e:
        print(f"  --> SUCCESS: Blocked 'sys' import as expected: {e}")
        
    return True

def test_playbook_routing_and_execution():
    print("\nTesting 24 due diligence playbooks compilation, routing and sandboxed execution...")
    
    coordinator = NexusCoordinator()
    
    # Test cases mapping prompts to expected playbook IDs
    test_prompts = [
        ("Compare actual earnings consensus surprise for AIR", 1, "Luna"),
        ("Screen startups funding rounds and founder board interlocks", 2, "Luna"),
        ("Track bond coupon maturity refinancing stress walls", 3, "Luna"),
        ("Determine supplier commodity contagion price exposure", 4, "Luna"),
        ("Monitor layoffs and bankruptcy default risk correlation", 5, "Luna"),
        ("Track broker ratings sentiment recommendations changes", 6, "Luna"),
        ("Compile a generative comps grid of SEC financials", 7, "Luna"),
        ("Analyze deal covenant and litigation damage default triggers", 8, "Luna"),
        ("Evaluate valuation multiple comparables EV EBITDA gross margin", 9, "Luna"),
        ("Generate an IC memo pitchbook with citations", 10, "Luna"),
        ("Generate a live Excel model sheet with projection formulas", 11, "Luna"),
        ("Run the weakly connected components supplier contagion simulator", 12, "Sol"),
        ("Run the prescriptive LBO target selection portfolio optimizer", 13, "Sol"),
        ("Trace the Bayesian information leak paths for suspect insider trades", 14, "Sol"),
        ("Solve optimal sovereign allocations for FX carry trade swap basis spreads", 15, "Sol"),
        ("Simulate federal contracting award backlog decay curves", 16, "Luna"),
        ("Trace ESG capital flight controversy rating multiples discounts", 17, "Luna"),
        ("Project biotech clinical trial approval success jump NPV", 18, "Luna"),
        ("Stress-test aviation route operating margin fleet disruptions", 19, "Luna"),
        ("Flag restricted semiconductor export control clients and fab capacities", 20, "Luna"),
        ("Compute executive pay performance TSR elasticity alignments", 21, "Luna"),
        ("Analyze supply chain holding cost inventory inflation margins", 22, "Luna"),
        ("Trace startup liquidity cash burn runway cliffs", 23, "Luna"),
        ("Formulate optimal commodity raw material futures hedging purchase schedules", 24, "Sol")
    ]
    
    all_passed = True
    
    for prompt, expected_id, expected_broker in test_prompts:
        print(f"\n[Use Case {expected_id}] Prompt: '{prompt[:45]}...'")
        try:
            res = coordinator.run_pipeline(prompt)
            assert res["success"] is True, "Pipeline failed execution status"
            assert res["playbook_id"] == expected_id, f"Routed to ID {res['playbook_id']} instead of {expected_id}"
            assert res["broker"] == expected_broker, f"Routed to broker {res['broker']} instead of {expected_broker}"
            print(f"  --> Routed to: {res['broker']} | Playbook: {res['playbook_id']} | Execution: SUCCESS")
        except Exception as e:
            print(f"  --> FAILED: {e}")
            all_passed = False
            
    return all_passed

def main():
    print("=" * 60)
    print("       NEXUS COORDINATOR & SANDBOX VERIFICATION SUITE")
    print("=" * 60)
    
    sandbox_ok = test_sandbox_prohibitions()
    playbooks_ok = test_playbook_routing_and_execution()
    
    print("\n" + "=" * 60)
    if sandbox_ok and playbooks_ok:
        print("       ALL COORDINATOR SYSTEM CHECKS VERIFIED SUCCESSFULLY!")
    else:
        print("       VERIFICATION SUITE COMPLETED WITH ERRORS.")
    print("=" * 60)

if __name__ == "__main__":
    main()
