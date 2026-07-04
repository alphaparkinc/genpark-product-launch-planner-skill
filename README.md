# product-launch-planner-skill

> **GenPark AI Agent Skill** -- Generate structured product launch plans with phased timelines, task checklists, and budget allocations.

## Features

- 4 launch phases: Pre-Launch (60d), Soft Launch (7d), Launch Day, Post-Launch (30d)
- 33 pre-built tasks with priorities, owners, and due dates
- Budget allocation by primary sales channel
- 12-item pre-launch checklist
- Multi-channel support: Shopify, Amazon, Instagram, TikTok, Email

## Quick Start

```python
from client import ProductLaunchClient

client = ProductLaunchClient()
plan = client.plan(
    product_name="My New Product",
    launch_date="2026-09-01",
    channels=["shopify", "instagram", "email"],
    budget_usd=10000,
)
print(plan["summary"])
for phase in plan["phases"]:
    print(f"{phase['phase']}: {phase['task_count']} tasks")
```

## Installation

```bash
python example_usage.py  # No external dependencies
```

---
Built by [GenPark](https://genpark.ai) | [alphaparkinc](https://github.com/alphaparkinc)
