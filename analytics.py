"""
Analytics engine for GrowthPilot.
Computes Growth KPIs, CAC, CPL, Funnel Drop-offs, Marketing Channel Stats, and Loss Reason diagnostics.
"""

from datetime import date, datetime
from typing import Dict, Any, List, Tuple
import pandas as pd
import numpy as np


def format_inr(number: float) -> str:
    """Formats a number into standard Indian Rupee notation (e.g. ₹1,20,000)."""
    if pd.isna(number) or number is None:
        return "₹0"
    num_int = int(round(number))
    s = str(abs(num_int))
    if len(s) <= 3:
        formatted = s
    else:
        last3 = s[-3:]
        rest = s[:-3]
        # In Indian numbering, commas are placed after every 2 digits for the rest
        chunks = []
        while len(rest) > 2:
            chunks.append(rest[-2:])
            rest = rest[:-2]
        if rest:
            chunks.append(rest)
        formatted = ",".join(reversed(chunks)) + "," + last3
    return f"-₹{formatted}" if num_int < 0 else f"₹{formatted}"


def compute_kpis(leads_df: pd.DataFrame, spend_df: pd.DataFrame) -> Dict[str, Any]:
    """Computes high-level growth and operational KPIs."""
    today_str = date.today().isoformat()
    total_leads = len(leads_df)

    if total_leads == 0:
        return {
            "total_leads": 0,
            "converted_leads": 0,
            "conversion_rate": 0.0,
            "total_revenue": 0.0,
            "total_spend": 0.0,
            "cpl": 0.0,
            "cac": 0.0,
            "lost_leads": 0,
            "follow_up_pending": 0,
            "follow_up_overdue": 0,
            "aov": 0.0,
            "best_channel": "N/A",
            "best_channel_rate": 0.0,
        }

    # Conversions
    converted_df = leads_df[leads_df["conversion_status"].str.lower() == "converted"]
    converted_count = len(converted_df)
    conversion_rate = (converted_count / total_leads * 100) if total_leads > 0 else 0.0
    total_revenue = float(converted_df["revenue"].sum())
    aov = (total_revenue / converted_count) if converted_count > 0 else 0.0

    # Lost Leads
    lost_df = leads_df[
        (leads_df["lead_status"].str.lower() == "lost") |
        (leads_df["conversion_status"].str.lower() == "lost")
    ]
    lost_count = len(lost_df)

    # Follow-ups
    pending_fu_df = leads_df[
        (leads_df["lead_status"].str.lower() == "follow-up") |
        (leads_df["conversion_status"].str.lower() == "follow-up")
    ]
    follow_up_pending = len(pending_fu_df)

    # Overdue follow-ups
    overdue_df = pending_fu_df[
        pending_fu_df["follow_up_date"].notna() &
        (pending_fu_df["follow_up_date"] < today_str)
    ]
    follow_up_overdue = len(overdue_df)

    # Marketing Spend, CPL & CAC
    total_spend = float(spend_df["monthly_spend"].sum()) if not spend_df.empty else 0.0
    cpl = (total_spend / total_leads) if total_leads > 0 else 0.0
    cac = (total_spend / converted_count) if converted_count > 0 else 0.0

    # Best Performing Channel
    channel_stats = leads_df.groupby("source").agg(
        total=("id", "count"),
        converted=("conversion_status", lambda x: (x.str.lower() == "converted").sum())
    ).reset_index()

    channel_stats["rate"] = (channel_stats["converted"] / channel_stats["total"]) * 100
    # Prefer channels with at least 3 leads to avoid 100% on 1 lead
    significant_channels = channel_stats[channel_stats["total"] >= 3]
    if not significant_channels.empty:
        best_row = significant_channels.sort_values(by=["rate", "converted"], ascending=False).iloc[0]
        best_channel = best_row["source"]
        best_channel_rate = float(best_row["rate"])
    elif not channel_stats.empty:
        best_row = channel_stats.sort_values(by=["rate", "converted"], ascending=False).iloc[0]
        best_channel = best_row["source"]
        best_channel_rate = float(best_row["rate"])
    else:
        best_channel = "N/A"
        best_channel_rate = 0.0

    return {
        "total_leads": total_leads,
        "converted_leads": converted_count,
        "conversion_rate": round(conversion_rate, 1),
        "total_revenue": total_revenue,
        "total_spend": total_spend,
        "cpl": round(cpl, 2),
        "cac": round(cac, 2),
        "lost_leads": lost_count,
        "follow_up_pending": follow_up_pending,
        "follow_up_overdue": follow_up_overdue,
        "aov": round(aov, 2),
        "best_channel": best_channel,
        "best_channel_rate": round(best_channel_rate, 1),
    }


def compute_channel_stats(leads_df: pd.DataFrame, spend_df: pd.DataFrame) -> pd.DataFrame:
    """Calculates comprehensive marketing channel metrics and comparative analysis."""
    if leads_df.empty:
        return pd.DataFrame(columns=[
            "Channel", "Leads", "Converted", "Lost", "Follow-up",
            "Conversion Rate (%)", "Revenue (₹)", "Monthly Spend (₹)",
            "CPL (₹)", "CAC (₹)", "ROAS"
        ])

    channels = leads_df["source"].unique()
    spend_map = dict(zip(spend_df["channel"], spend_df["monthly_spend"])) if not spend_df.empty else {}

    rows = []
    for ch in channels:
        ch_leads = leads_df[leads_df["source"] == ch]
        total_l = len(ch_leads)
        conv_l = len(ch_leads[ch_leads["conversion_status"].str.lower() == "converted"])
        lost_l = len(ch_leads[ch_leads["conversion_status"].str.lower() == "lost"])
        fu_l = len(ch_leads[ch_leads["conversion_status"].str.lower() == "follow-up"])

        rev = float(ch_leads[ch_leads["conversion_status"].str.lower() == "converted"]["revenue"].sum())
        spend = float(spend_map.get(ch, 0.0))

        rate = (conv_l / total_l * 100) if total_l > 0 else 0.0
        cpl = (spend / total_l) if total_l > 0 else 0.0
        cac = (spend / conv_l) if conv_l > 0 else 0.0
        roas = (rev / spend) if spend > 0 else (np.inf if rev > 0 else 0.0)

        rows.append({
            "Channel": ch,
            "Leads": total_l,
            "Converted": conv_l,
            "Lost": lost_l,
            "Follow-up": fu_l,
            "Conversion Rate (%)": round(rate, 1),
            "Revenue (₹)": rev,
            "Monthly Spend (₹)": spend,
            "CPL (₹)": round(cpl, 2),
            "CAC (₹)": round(cac, 2),
            "ROAS": round(roas, 2) if roas != np.inf else "N/A"
        })

    result_df = pd.DataFrame(rows)
    return result_df.sort_values(by="Leads", ascending=False).reset_index(drop=True)


def compute_funnel_stages(leads_df: pd.DataFrame, visitors_count: int = 1000) -> Dict[str, Any]:
    """
    Computes 5-stage customer conversion funnel:
    Visitors → Leads → Contacted → Qualified → Converted
    And computes drop-off percentages and isolates the largest drop-off bottleneck.
    """
    total_leads = len(leads_df)

    # Leads who reached at least Contacted stage (everyone except raw 'New' leads who haven't been contacted yet)
    contacted_count = len(leads_df[leads_df["lead_status"].str.lower() != "new"])

    # Leads who reached Qualified stage (Qualified, Follow-up, or Converted)
    qualified_count = len(leads_df[
        leads_df["lead_status"].str.lower().isin(["qualified", "follow-up", "converted"]) |
        leads_df["conversion_status"].str.lower().isin(["follow-up", "converted"])
    ])

    # Converted customers
    converted_count = len(leads_df[leads_df["conversion_status"].str.lower() == "converted"])

    stages = [
        {"stage": "1. Visitors", "count": visitors_count},
        {"stage": "2. Leads", "count": total_leads},
        {"stage": "3. Contacted", "count": contacted_count},
        {"stage": "4. Qualified", "count": qualified_count},
        {"stage": "5. Converted", "count": converted_count},
    ]

    # Calculate step-by-step drop-offs
    drop_offs = []
    largest_drop = {"from": "", "to": "", "drop_count": -1, "drop_pct": -1.0}

    for i in range(len(stages) - 1):
        from_stage = stages[i]["stage"]
        to_stage = stages[i + 1]["stage"]
        from_count = stages[i]["count"]
        to_count = stages[i + 1]["count"]

        diff = from_count - to_count
        drop_pct = (diff / from_count * 100) if from_count > 0 else 0.0
        conversion_pct = (to_count / from_count * 100) if from_count > 0 else 0.0

        drop_offs.append({
            "from_stage": from_stage,
            "to_stage": to_stage,
            "from_count": from_count,
            "to_count": to_count,
            "drop_count": max(0, diff),
            "drop_pct": round(drop_pct, 1),
            "conversion_pct": round(conversion_pct, 1)
        })

    # Find the largest operational drop-off within the sales pipeline (from Leads onward)
    pipeline_drop_offs = drop_offs[1:] if len(drop_offs) > 1 else drop_offs
    if pipeline_drop_offs:
        # Sort by drop count or drop percentage; the stage where most leads drop off
        largest_candidate = max(pipeline_drop_offs, key=lambda x: (x["drop_count"], x["drop_pct"]))
        largest_drop = {
            "from": largest_candidate["from_stage"],
            "to": largest_candidate["to_stage"],
            "drop_count": largest_candidate["drop_count"],
            "drop_pct": largest_candidate["drop_pct"]
        }

    return {
        "stages": stages,
        "drop_offs": drop_offs,
        "largest_drop": largest_drop,
        "overall_conversion_pct": round((converted_count / visitors_count * 100), 2) if visitors_count > 0 else 0.0
    }


def compute_loss_reasons(leads_df: pd.DataFrame) -> pd.DataFrame:
    """Analyzes lost lead reasons to uncover why leads are not converting."""
    lost_df = leads_df[
        (leads_df["lead_status"].str.lower() == "lost") |
        (leads_df["conversion_status"].str.lower() == "lost")
    ]
    if lost_df.empty:
        return pd.DataFrame(columns=["Reason", "Count", "Percentage (%)"])

    reasons = lost_df["loss_reason"].fillna("Unspecified / Other").value_counts().reset_index()
    reasons.columns = ["Reason", "Count"]
    total = len(lost_df)
    reasons["Percentage (%)"] = (reasons["Count"] / total * 100).round(1)
    return reasons
