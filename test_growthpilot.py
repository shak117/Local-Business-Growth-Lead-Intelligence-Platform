"""
Automated Verification Suite for GrowthPilot.
Tests database, analytics, recommendations, and chart builders.
"""

import sys
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
import pandas as pd
from database import (
    get_leads_df,
    get_marketing_spend_df,
    get_competitors_df,
    get_top_funnel_visitors
)
from analytics import (
    compute_kpis,
    compute_channel_stats,
    compute_funnel_stages,
    compute_loss_reasons,
    format_inr
)
from recommendations import generate_recommendations

def test_all():
    print("========================================")
    print("RUNNING GROWTHPILOT VERIFICATION TESTS")
    print("========================================")

    # 1. Database tests
    leads = get_leads_df()
    spend = get_marketing_spend_df()
    comps = get_competitors_df()
    visitors = get_top_funnel_visitors()

    print(f"[TEST 1: DB] Total Leads in DB: {len(leads)}")
    assert len(leads) >= 200, f"Expected at least 200 leads, got {len(leads)}"

    # Check explicit leads
    rahul = leads[leads["name"].str.contains("Rahul Sharma", na=False)]
    assert not rahul.empty, "Rahul Sharma not found!"
    assert rahul.iloc[0]["source"] == "Instagram"
    assert rahul.iloc[0]["conversion_status"] == "Converted"
    assert rahul.iloc[0]["revenue"] == 8000.0
    print("[TEST 1: DB] Found explicit lead Rahul (Instagram, Converted, ₹8,000)")

    sneha = leads[leads["name"].str.contains("Sneha Patel", na=False)]
    assert not sneha.empty, "Sneha Patel not found!"
    assert sneha.iloc[0]["source"] == "Google"
    assert sneha.iloc[0]["lead_status"] == "Follow-up"
    print("[TEST 1: DB] Found explicit lead Sneha (Google, Follow-up)")

    amit = leads[leads["name"].str.contains("Amit Mehta", na=False)]
    assert not amit.empty, "Amit Mehta not found!"
    assert amit.iloc[0]["source"] == "Referral"
    assert amit.iloc[0]["conversion_status"] == "Converted"
    assert amit.iloc[0]["revenue"] == 12000.0
    print("[TEST 1: DB] Found explicit lead Amit (Referral, Converted, ₹12,000)")

    priya = leads[leads["name"].str.contains("Priya Singh", na=False)]
    assert not priya.empty, "Priya Singh not found!"
    assert priya.iloc[0]["source"] == "Website"
    assert priya.iloc[0]["conversion_status"] == "Lost"
    print("[TEST 1: DB] Found explicit lead Priya (Website, Lost)")

    # 2. Analytics KPIs tests
    kpis = compute_kpis(leads, spend)
    print(f"[TEST 2: KPIs] Conversion Rate: {kpis['conversion_rate']}%")
    print(f"[TEST 2: KPIs] Total Revenue: {format_inr(kpis['total_revenue'])}")
    print(f"[TEST 2: KPIs] Cost Per Lead (CPL): {format_inr(kpis['cpl'])}")
    print(f"[TEST 2: KPIs] Customer Acq Cost (CAC): {format_inr(kpis['cac'])}")
    print(f"[TEST 2: KPIs] Best Channel: {kpis['best_channel']} ({kpis['best_channel_rate']}%)")
    print(f"[TEST 2: KPIs] Follow-up Pending: {kpis['follow_up_pending']} (Overdue: {kpis['follow_up_overdue']})")
    assert kpis["total_leads"] > 0
    assert kpis["conversion_rate"] > 0
    assert kpis["cpl"] > 0
    assert kpis["cac"] > 0

    # 3. Channel statistics tests
    chan_stats = compute_channel_stats(leads, spend)
    print("[TEST 3: Channels] Channel breakdown:")
    for _, row in chan_stats.iterrows():
        print(f"   - {row['Channel']}: {row['Leads']} leads, {row['Converted']} converted ({row['Conversion Rate (%)']}%), CAC: {format_inr(row['CAC (₹)'])}")

    ig_stat = chan_stats[chan_stats["Channel"] == "Instagram"].iloc[0]
    ref_stat = chan_stats[chan_stats["Channel"] == "Referral"].iloc[0]
    assert ig_stat["Leads"] > ref_stat["Leads"], "Instagram should have more leads than Referral"
    assert ref_stat["Conversion Rate (%)"] > ig_stat["Conversion Rate (%)"], "Referral should have higher conv rate than Instagram"

    # 4. Funnel stages tests
    funnel = compute_funnel_stages(leads, visitors_count=visitors)
    print("[TEST 4: Funnel] 5-Stage Customer Funnel:")
    for s in funnel["stages"]:
        print(f"   - {s['stage']}: {s['count']}")
    largest_d = funnel["largest_drop"]
    print(f"[TEST 4: Funnel] Largest Drop-off detected: {largest_d['from']} -> {largest_d['to']} ({largest_d['drop_pct']}%)")
    assert largest_d["drop_pct"] > 0

    # 5. Competitor intelligence tests
    assert len(comps) >= 3, f"Expected >= 3 competitors, got {len(comps)}"
    comp_names = comps["name"].tolist()
    assert any("Competitor A" in n for n in comp_names)
    assert any("Competitor B" in n for n in comp_names)
    assert any("Competitor C" in n for n in comp_names)
    print(f"[TEST 5: Competitors] Verified {len(comps)} competitors (A, B, C, etc.)")

    # 6. Recommendations engine tests
    loss_reasons = compute_loss_reasons(leads)
    recs = generate_recommendations(kpis, chan_stats, funnel, loss_reasons, comps)
    print(f"[TEST 6: Recs] Generated {len(recs)} actionable growth recommendations:")
    for r in recs:
        print(f"   - [{r['priority']}] {r['title']} (Trigger: {r['trigger'][:60]}...)")
    assert len(recs) >= 3, f"Expected at least 3 recommendations, got {len(recs)}"

    print("========================================")
    print("ALL TESTS PASSED SUCCESSFULLY!")
    print("========================================")

if __name__ == "__main__":
    test_all()
