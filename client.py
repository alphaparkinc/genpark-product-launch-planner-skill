"""
product-launch-planner-skill: Client SDK
Generate structured product launch plans with phased timelines and task checklists.
"""
from __future__ import annotations
from datetime import datetime, date, timedelta
from typing import Optional

PHASE_TEMPLATES = {
    "pre_launch": {
        "name": "Pre-Launch Preparation",
        "offset_start": -60,
        "offset_end": -8,
        "tasks": [
            {"task": "Finalize product photography and video assets", "owner": "creative", "priority": "high"},
            {"task": "Write product descriptions and SEO metadata", "owner": "content", "priority": "high"},
            {"task": "Set up product listings on all channels", "owner": "ecommerce", "priority": "high"},
            {"task": "Configure inventory and fulfillment workflows", "owner": "ops", "priority": "high"},
            {"task": "Build email launch sequence (teaser, launch, follow-up)", "owner": "marketing", "priority": "high"},
            {"task": "Set up tracking pixels and analytics dashboards", "owner": "marketing", "priority": "medium"},
            {"task": "Recruit and brief influencer partners", "owner": "marketing", "priority": "medium"},
            {"task": "Create social media content calendar for launch month", "owner": "content", "priority": "medium"},
            {"task": "Set up customer service FAQs and chatbot flows", "owner": "support", "priority": "medium"},
            {"task": "Configure abandoned cart and post-purchase email flows", "owner": "ecommerce", "priority": "medium"},
            {"task": "Run pre-launch landing page A/B test", "owner": "marketing", "priority": "low"},
            {"task": "Conduct QA on all product pages and checkout flow", "owner": "ecommerce", "priority": "high"},
        ]
    },
    "soft_launch": {
        "name": "Soft Launch (VIP / Waitlist)",
        "offset_start": -7,
        "offset_end": -1,
        "tasks": [
            {"task": "Send exclusive early access to VIP email list", "owner": "marketing", "priority": "high"},
            {"task": "Activate influencer content drops (stories/reels)", "owner": "marketing", "priority": "high"},
            {"task": "Monitor inventory levels and fulfillment speed", "owner": "ops", "priority": "high"},
            {"task": "Collect and respond to early customer feedback", "owner": "support", "priority": "medium"},
            {"task": "Run paid social ads to warm audiences only", "owner": "marketing", "priority": "medium"},
            {"task": "Confirm all tracking and attribution is working", "owner": "marketing", "priority": "high"},
        ]
    },
    "launch_day": {
        "name": "Launch Day",
        "offset_start": 0,
        "offset_end": 0,
        "tasks": [
            {"task": "Send launch email to full subscriber list", "owner": "marketing", "priority": "critical"},
            {"task": "Publish launch announcement on all social channels", "owner": "content", "priority": "critical"},
            {"task": "Activate broad paid ad campaigns (Google, Meta)", "owner": "marketing", "priority": "critical"},
            {"task": "Go live on all sales channels simultaneously", "owner": "ecommerce", "priority": "critical"},
            {"task": "Monitor site performance and server load", "owner": "tech", "priority": "high"},
            {"task": "Issue press release / pitch to media outlets", "owner": "pr", "priority": "high"},
            {"task": "Respond to all customer inquiries within 2 hours", "owner": "support", "priority": "high"},
            {"task": "Post real-time updates and stories throughout day", "owner": "content", "priority": "medium"},
        ]
    },
    "post_launch": {
        "name": "Post-Launch Optimization",
        "offset_start": 1,
        "offset_end": 30,
        "tasks": [
            {"task": "Analyze launch day metrics (conversion, AOV, CAC)", "owner": "analytics", "priority": "high"},
            {"task": "Send post-purchase review request sequence", "owner": "marketing", "priority": "high"},
            {"task": "Optimize ad creative based on performance data", "owner": "marketing", "priority": "high"},
            {"task": "Replenish inventory based on sell-through rate", "owner": "ops", "priority": "medium"},
            {"task": "Publish customer testimonials and UGC content", "owner": "content", "priority": "medium"},
            {"task": "A/B test product page based on heatmap data", "owner": "ecommerce", "priority": "medium"},
            {"task": "Conduct post-launch team retrospective", "owner": "all", "priority": "low"},
        ]
    }
}

CHANNEL_BUDGET_SPLITS = {
    "shopify":   {"ads": 0.40, "content": 0.20, "email": 0.15, "influencer": 0.15, "ops": 0.10},
    "amazon":    {"ads": 0.50, "content": 0.15, "email": 0.10, "influencer": 0.10, "ops": 0.15},
    "instagram": {"ads": 0.35, "content": 0.25, "email": 0.10, "influencer": 0.25, "ops": 0.05},
    "tiktok":    {"ads": 0.30, "content": 0.20, "email": 0.05, "influencer": 0.35, "ops": 0.10},
    "email":     {"ads": 0.20, "content": 0.30, "email": 0.30, "influencer": 0.10, "ops": 0.10},
    "default":   {"ads": 0.40, "content": 0.20, "email": 0.15, "influencer": 0.15, "ops": 0.10},
}

PRE_LAUNCH_CHECKLIST = [
    "Product pages live and fully optimized on all channels",
    "Checkout flow tested end-to-end with real payment",
    "Inventory confirmed available and allocated",
    "All email sequences activated and tested",
    "Paid ad campaigns paused and ready to activate",
    "Customer support team briefed on product details",
    "Analytics and conversion tracking verified",
    "Social content scheduled and approved",
    "Influencer content reviewed and confirmed",
    "Fulfillment SLAs confirmed with 3PL or warehouse",
    "Refund and return policy published",
    "Legal review complete (claims, compliance)",
]


class ProductLaunchClient:
    """
    SDK for generating structured e-commerce product launch plans.
    Produces phased timelines, task checklists, and budget allocations.
    """

    def plan(
        self,
        product_name: str,
        launch_date: str,
        channels: Optional[list[str]] = None,
        budget_usd: float = 10000.0,
        team_size: int = 3,
    ) -> dict:
        """
        Generate a complete product launch plan.

        Args:
            product_name: Name of the product to launch.
            launch_date:  Target launch date (YYYY-MM-DD).
            channels:     Sales/marketing channels to include.
            budget_usd:   Total launch budget in USD.
            team_size:    Team members available.

        Returns:
            dict with: phases, total_tasks, budget_allocation, launch_checklist, summary
        """
        channels = channels or ["shopify", "email", "instagram"]
        try:
            launch = datetime.fromisoformat(launch_date).date()
        except ValueError:
            launch = date.today() + timedelta(days=60)

        phases = []
        total_tasks = 0
        for phase_key, tmpl in PHASE_TEMPLATES.items():
            start = launch + timedelta(days=tmpl["offset_start"])
            end = launch + timedelta(days=tmpl["offset_end"])
            tasks = [dict(t) for t in tmpl["tasks"]]
            # Assign owners round-robin if team is small
            owners = [f"Team Member {(i % team_size) + 1}" for i in range(len(tasks))]
            for j, task in enumerate(tasks):
                task["assigned_to"] = owners[j]
                task["due_date"] = str(end - timedelta(days=max(0, len(tasks) - j - 1)))
            phases.append({
                "phase": tmpl["name"],
                "start_date": str(start),
                "end_date": str(end),
                "task_count": len(tasks),
                "tasks": tasks,
            })
            total_tasks += len(tasks)

        budget_allocation = self._allocate_budget(budget_usd, channels)

        days_until_launch = (launch - date.today()).days
        summary = (
            f"Launch Plan for '{product_name}' | "
            f"Target: {launch_date} ({days_until_launch} days away) | "
            f"Channels: {', '.join(channels)} | "
            f"Budget: ${budget_usd:,.0f} | "
            f"Tasks: {total_tasks} across {len(phases)} phases"
        )

        return {
            "product": product_name,
            "launch_date": launch_date,
            "channels": channels,
            "phases": phases,
            "total_tasks": total_tasks,
            "budget_allocation": budget_allocation,
            "launch_checklist": PRE_LAUNCH_CHECKLIST,
            "summary": summary,
        }

    @staticmethod
    def _allocate_budget(budget: float, channels: list[str]) -> dict:
        primary = channels[0].lower() if channels else "default"
        splits = CHANNEL_BUDGET_SPLITS.get(primary, CHANNEL_BUDGET_SPLITS["default"])
        return {
            category: round(budget * pct, 2)
            for category, pct in splits.items()
        }
