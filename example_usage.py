"""
example_usage.py -- Demonstrates the ProductLaunchClient SDK.
"""
from client import ProductLaunchClient
from datetime import date, timedelta

def main():
    client = ProductLaunchClient()

    launch_date = str(date.today() + timedelta(days=45))

    print("[Product Launch Plan Generator]")
    result = client.plan(
        product_name="HydraGlow Vitamin C Serum",
        launch_date=launch_date,
        channels=["shopify", "instagram", "email", "tiktok"],
        budget_usd=15000,
        team_size=4,
    )
    print(f"\nSummary: {result['summary']}")
    print(f"Total Tasks: {result['total_tasks']}")
    print(f"\nBudget Allocation:")
    for cat, amt in result["budget_allocation"].items():
        print(f"  {cat:<15}: ${amt:,.2f}")
    print(f"\nLaunch Phases:")
    for phase in result["phases"]:
        print(f"\n  [{phase['phase']}]  {phase['start_date']} to {phase['end_date']}")
        for task in phase["tasks"][:3]:
            print(f"    - [{task['priority'].upper()}] {task['task']}")
        if phase["task_count"] > 3:
            print(f"    ... and {phase['task_count']-3} more tasks")
    print(f"\nPre-Launch Checklist ({len(result['launch_checklist'])} items):")
    for item in result["launch_checklist"][:5]:
        print(f"  [ ] {item}")

if __name__ == "__main__":
    main()
