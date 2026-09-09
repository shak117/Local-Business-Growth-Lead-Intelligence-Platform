"""
GrowthPilot — Business Growth & Lead Intelligence Dashboard
Main Streamlit Application
"""

import streamlit as st
import pandas as pd
from datetime import date, timedelta
from pathlib import Path

# Set page configuration
st.set_page_config(
    page_title="GrowthPilot — Business Growth Dashboard",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Imports from project modules
from database import (
    init_db,
    get_leads_df,
    insert_lead,
    update_lead,
    delete_lead,
    batch_import_leads,
    get_marketing_spend_df,
    update_marketing_spend,
    get_competitors_df,
    insert_competitor,
    delete_competitor,
    get_top_funnel_visitors,
    update_top_funnel_visitors,
    reset_and_seed_database
)
from seed_data import seed_database
from analytics import (
    compute_kpis,
    compute_channel_stats,
    compute_funnel_stages,
    compute_loss_reasons,
    format_inr
)
from recommendations import generate_recommendations
from components.styles import apply_custom_styles
from components.kpi_cards import render_growth_kpi_cards
from components.charts import (
    render_funnel_chart,
    render_channel_comparison,
    render_cpl_cac_chart,
    render_revenue_donut,
    render_lead_timeline,
    render_competitor_matrix,
    render_loss_reasons_chart
)

# Apply UI styles
apply_custom_styles()

# Initialize DB and auto-seed on fresh start
init_db()
if get_leads_df().empty:
    seed_database()

# ==========================================
# SIDEBAR CONTROLS & NAVIGATION
# ==========================================

with st.sidebar:
    st.markdown("""
    <div style="text-align: left; padding: 0.5rem 0 1rem 0;">
        <span style="font-size: 1.8rem;">🚀</span>
        <span style="font-size: 1.4rem; font-weight: 800; color: #0F172A; letter-spacing: -0.02em;">GrowthPilot</span>
        <div style="font-size: 0.78rem; color: #64748B; font-weight: 500;">Lead Intelligence & Operations</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("🔍 Filter Leads")

    # Date Range Filter
    today = date.today()
    default_start = today - timedelta(days=60)
    date_range = st.date_input(
        "Date Range",
        value=(default_start, today),
        max_value=today + timedelta(days=30)
    )

    start_date = date_range[0].isoformat() if len(date_range) > 0 else None
    end_date = date_range[1].isoformat() if len(date_range) > 1 else None

    # Channels Filter
    all_channels = ["Instagram", "Google", "WhatsApp", "Referral", "Website", "Direct"]
    selected_channels = st.multiselect(
        "Marketing Channels",
        options=all_channels,
        default=all_channels
    )

    # Lead Status Filter
    all_statuses = ["New", "Contacted", "Qualified", "Follow-up", "Converted", "Lost"]
    selected_statuses = st.multiselect(
        "Lead Status",
        options=all_statuses,
        default=all_statuses
    )

    st.markdown("---")
    st.subheader("⚙️ Database Operations")

    if st.button("🔄 Reset to Default Seed Data", use_container_width=True):
        seed_database()
        st.success("Database re-seeded with realistic sample data!")
        st.rerun()

    st.caption("GrowthPilot v1.0 • Built for Modern Growth Generalists")


# ==========================================
# FETCH FILTERED DATA
# ==========================================

leads_df = get_leads_df(
    start_date=start_date,
    end_date=end_date,
    channels=selected_channels if selected_channels else None,
    statuses=selected_statuses if selected_statuses else None
)
spend_df = get_marketing_spend_df()
competitors_df = get_competitors_df()
visitors_count = get_top_funnel_visitors()

# Run Analytics Engine
kpis = compute_kpis(leads_df, spend_df)
channel_stats = compute_channel_stats(leads_df, spend_df)
funnel_data = compute_funnel_stages(leads_df, visitors_count=visitors_count)
loss_reasons = compute_loss_reasons(leads_df)
recommendations = generate_recommendations(kpis, channel_stats, funnel_data, loss_reasons, competitors_df)


# ==========================================
# HEADER HERO SECTION
# ==========================================

st.markdown(f"""
<div class="growth-hero">
    <div class="hero-badge">Mini Growth Team Dashboard</div>
    <h1>GrowthPilot — Business Growth & Lead Intelligence</h1>
    <p>Real-time lead attribution, channel conversion analytics, customer funnel bottlenecks, competitor benchmarking, and automated growth recommendations.</p>
</div>
""", unsafe_allow_html=True)


# ==========================================
# MAIN TABS NAVIGATION
# ==========================================

tab_overview, tab_crm, tab_channels, tab_funnel, tab_competitors, tab_recommendations, tab_simulator = st.tabs([
    "📊 Growth Overview",
    "👥 Lead Management (CRM)",
    "📣 Marketing Channels",
    "🔻 Customer Funnel",
    "⚔️ Competitor Analysis",
    "🤖 Growth Recommendations",
    "💡 Ask GrowthPilot (Simulator)"
])


# =============================================================================
# TAB 1: GROWTH OVERVIEW
# =============================================================================
with tab_overview:
    st.markdown("### 📈 Executive Growth Scorecard")
    render_growth_kpi_cards(kpis)

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    col_trend, col_chan_summary = st.columns([1.6, 1.4])

    with col_trend:
        st.plotly_chart(render_lead_timeline(leads_df), use_container_width=True)

    with col_chan_summary:
        st.plotly_chart(render_revenue_donut(channel_stats), use_container_width=True)

    # Highlight Action Cards
    st.markdown("### ⚡ Operational Growth Snapshot")
    snap1, snap2, snap3 = st.columns(3)

    with snap1:
        st.info(f"""
        **Top Converting Channel: {kpis['best_channel']}**  
        Converts at **{kpis['best_channel_rate']}%**, delivering the highest sales efficiency.
        """)

    with snap2:
        largest_d = funnel_data.get("largest_drop", {})
        st.warning(f"""
        **Funnel Bottleneck: {largest_d.get('from', 'Contacted')} → {largest_d.get('to', 'Qualified')}**  
        Largest drop-off is **{largest_d.get('drop_pct', 0)}%**, causing lead disqualification.
        """)

    with snap3:
        if kpis['follow_up_overdue'] > 0:
            st.error(f"""
            **Follow-up Alert: {kpis['follow_up_overdue']} Leads Overdue**  
            Overdue leads risk losing interest to competitors. Prioritize immediate outreach.
            """)
        else:
            st.success("""
            **Follow-up Hygiene: Clear**  
            All active follow-up schedules are up-to-date.
            """)


# =============================================================================
# TAB 2: LEAD MANAGEMENT (CRM)
# =============================================================================
with tab_crm:
    st.markdown("### 👥 Lead Management & Pipeline")

    # Follow-up Alert Banner
    pending_fu = leads_df[
        (leads_df["lead_status"].str.lower() == "follow-up") |
        (leads_df["conversion_status"].str.lower() == "follow-up")
    ]
    if not pending_fu.empty:
        today_str = date.today().isoformat()
        overdue_leads = pending_fu[pending_fu["follow_up_date"] < today_str]
        if not overdue_leads.empty:
            st.error(f"🚨 **Action Required**: You have **{len(overdue_leads)} overdue follow-up leads** that need attention today!")

    # Action Accordions: Add Lead & Update Status
    col_act1, col_act2 = st.columns(2)

    with col_act1:
        with st.expander("➕ Add New Inbound Lead", expanded=False):
            with st.form("new_lead_form", clear_on_submit=True):
                nl_name = st.text_input("Lead Name *", placeholder="e.g. Rahul Sharma")
                col_c1, col_c2 = st.columns(2)
                with col_c1:
                    nl_phone = st.text_input("Phone Number", placeholder="+91 98765 43210")
                    nl_source = st.selectbox("Lead Source *", options=all_channels)
                    nl_status = st.selectbox("Initial Status *", options=["New", "Contacted", "Qualified", "Follow-up", "Converted", "Lost"])
                with col_c2:
                    nl_email = st.text_input("Email", placeholder="rahul@example.com")
                    nl_product = st.text_input("Product / Service *", value="Growth Consulting Package")
                    nl_conv_status = st.selectbox("Conversion Status *", options=["Pending", "Follow-up", "Converted", "Lost"])

                col_c3, col_c4 = st.columns(2)
                with col_c3:
                    nl_date = st.date_input("Date Created", value=date.today())
                    nl_revenue = st.number_input("Revenue (₹) if Converted", min_value=0.0, step=1000.0, value=0.0)
                with col_c4:
                    nl_fu_date = st.date_input("Follow-up Date (Optional)", value=None)
                    nl_loss = st.selectbox("Loss Reason (if Lost)", options=["None", "Price too high", "Chose competitor", "No response after call", "Timing not right", "Other"])

                nl_notes = st.text_area("Notes", placeholder="Specific client pain points, requirements, or conversation context...")
                submitted = st.form_submit_button("Save Lead to CRM", use_container_width=True)

                if submitted:
                    if not nl_name.strip():
                        st.error("Lead name is required.")
                    else:
                        new_data = {
                            "name": nl_name,
                            "phone": nl_phone,
                            "email": nl_email,
                            "source": nl_source,
                            "product_service": nl_product,
                            "lead_status": nl_status,
                            "date_created": nl_date.isoformat(),
                            "follow_up_date": nl_fu_date.isoformat() if nl_fu_date else None,
                            "conversion_status": nl_conv_status,
                            "revenue": nl_revenue if nl_conv_status == "Converted" else 0.0,
                            "loss_reason": None if nl_loss == "None" else nl_loss,
                            "notes": nl_notes
                        }
                        lead_id = insert_lead(new_data)
                        st.success(f"Lead '{nl_name}' created successfully (ID: #{lead_id})!")
                        st.rerun()

    with col_act2:
        with st.expander("⚡ Quick Update Lead Status", expanded=False):
            if not leads_df.empty:
                lead_options = {f"#{row['id']} - {row['name']} ({row['source']}, {row['lead_status']})": row['id'] for _, row in leads_df.iterrows()}
                selected_lead_label = st.selectbox("Select Lead to Update", options=list(lead_options.keys()))
                sel_id = lead_options[selected_lead_label]
                sel_row = leads_df[leads_df["id"] == sel_id].iloc[0]

                with st.form("update_lead_form"):
                    col_u1, col_u2 = st.columns(2)
                    with col_u1:
                        up_status = st.selectbox("New Lead Status", options=all_statuses, index=all_statuses.index(sel_row["lead_status"]) if sel_row["lead_status"] in all_statuses else 0)
                        up_conv = st.selectbox("New Conversion Status", options=["Pending", "Follow-up", "Converted", "Lost"], index=["Pending", "Follow-up", "Converted", "Lost"].index(sel_row["conversion_status"]) if sel_row["conversion_status"] in ["Pending", "Follow-up", "Converted", "Lost"] else 0)
                        up_rev = st.number_input("Revenue (₹)", value=float(sel_row["revenue"] or 0.0), step=1000.0)
                    with col_u2:
                        up_fu = st.date_input("Follow-up Date", value=pd.to_datetime(sel_row["follow_up_date"]).date() if pd.notna(sel_row["follow_up_date"]) and sel_row["follow_up_date"] else None)
                        loss_options = ["None", "Price too high", "Chose competitor", "No response after 3 follow-ups", "Timing not right", "Feature mismatch"]
                        curr_loss = sel_row.get("loss_reason") or "None"
                        up_loss = st.selectbox("Loss Reason", options=loss_options, index=loss_options.index(curr_loss) if curr_loss in loss_options else 0)
                    up_notes = st.text_area("Update Notes", value=str(sel_row.get("notes") or ""))

                    up_submitted = st.form_submit_button("Update Lead", use_container_width=True)
                    if up_submitted:
                        updates = {
                            "lead_status": up_status,
                            "conversion_status": up_conv,
                            "revenue": up_rev if up_conv == "Converted" else 0.0,
                            "follow_up_date": up_fu.isoformat() if up_fu else None,
                            "loss_reason": None if up_loss == "None" else up_loss,
                            "notes": up_notes
                        }
                        update_lead(sel_id, updates)
                        st.success(f"Lead #{sel_id} updated successfully!")
                        st.rerun()

    # Search and Filter
    st.markdown("#### 📋 Lead Records")
    search_query = st.text_input("Search Leads by Name, Phone, Email, or Notes", placeholder="e.g. Rahul, Instagram, Gym...").strip().lower()

    filtered_table_df = leads_df.copy()
    if search_query:
        mask = (
            filtered_table_df["name"].str.lower().str.contains(search_query) |
            filtered_table_df["source"].str.lower().str.contains(search_query) |
            filtered_table_df["product_service"].str.lower().str.contains(search_query) |
            filtered_table_df["notes"].fillna("").str.lower().str.contains(search_query)
        )
        filtered_table_df = filtered_table_df[mask]

    # Format dataframe for display
    display_df = filtered_table_df[[
        "id", "name", "source", "product_service", "lead_status",
        "conversion_status", "date_created", "follow_up_date", "revenue", "loss_reason", "notes"
    ]].copy()
    display_df["revenue"] = display_df["revenue"].apply(format_inr)

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "id": st.column_config.NumberColumn("ID", width="small"),
            "name": st.column_config.TextColumn("Lead Name", width="medium"),
            "source": st.column_config.TextColumn("Source", width="small"),
            "product_service": st.column_config.TextColumn("Product / Service", width="medium"),
            "lead_status": st.column_config.TextColumn("Status", width="small"),
            "conversion_status": st.column_config.TextColumn("Conversion", width="small"),
            "date_created": st.column_config.TextColumn("Created Date", width="small"),
            "follow_up_date": st.column_config.TextColumn("Follow-up", width="small"),
            "revenue": st.column_config.TextColumn("Revenue", width="small"),
            "loss_reason": st.column_config.TextColumn("Loss Reason", width="medium"),
            "notes": st.column_config.TextColumn("Notes", width="large")
        }
    )
    st.caption(f"Showing {len(filtered_table_df)} of {len(leads_df)} leads")

    # CSV Export and Import section
    st.markdown("---")
    st.markdown("#### 📁 Import & Export Leads")
    col_exp, col_imp = st.columns(2)

    with col_exp:
        csv_data = filtered_table_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Export Filtered Leads as CSV",
            data=csv_data,
            file_name=f"growthpilot_leads_{date.today().isoformat()}.csv",
            mime="text/csv",
            use_container_width=True
        )

    with col_imp:
        uploaded_file = st.file_uploader("📤 Import Leads from CSV", type=["csv"])
        if uploaded_file is not None:
            try:
                imp_df = pd.read_csv(uploaded_file)
                st.write("Preview of leads to import:")
                st.dataframe(imp_df.head(3), use_container_width=True)
                if st.button("Confirm and Import Leads", key="btn_confirm_import", use_container_width=True):
                    count = batch_import_leads(imp_df)
                    st.success(f"Successfully imported {count} leads!")
                    st.rerun()
            except Exception as e:
                st.error(f"Error reading CSV: {e}")


# =============================================================================
# TAB 3: MARKETING CHANNELS
# =============================================================================
with tab_channels:
    st.markdown("### 📣 Marketing Channel Analysis")
    st.markdown("Compare acquisition volume, conversion rates, customer acquisition costs (CAC), and return on ad spend (ROAS) across all channels.")

    # Channel comparison cards
    st.plotly_chart(render_channel_comparison(channel_stats), use_container_width=True)

    col_cpl_cac, col_spend_editor = st.columns([1.6, 1.4])

    with col_cpl_cac:
        st.plotly_chart(render_cpl_cac_chart(channel_stats), use_container_width=True)

    with col_spend_editor:
        st.markdown("#### 💳 Monthly Marketing Spend (₹)")
        st.caption("Adjust your monthly channel budgets to recalculate CPL and CAC in real-time.")

        curr_spend_df = get_marketing_spend_df()
        with st.form("update_spend_form"):
            new_spends = {}
            for ch in all_channels:
                current_val = 0.0
                match = curr_spend_df[curr_spend_df["channel"] == ch]
                if not match.empty:
                    current_val = float(match.iloc[0]["monthly_spend"])
                new_spends[ch] = st.number_input(f"{ch} Monthly Spend (₹)", value=current_val, step=1000.0)

            if st.form_submit_button("Save Marketing Spend", use_container_width=True):
                for ch, sp in new_spends.items():
                    update_marketing_spend(ch, sp)
                st.success("Marketing spend updated!")
                st.rerun()

    # Detailed Channel Table
    st.markdown("#### 📊 Channel Economics Benchmark Table")
    formatted_ch_df = channel_stats.copy()
    formatted_ch_df["Revenue (₹)"] = formatted_ch_df["Revenue (₹)"].apply(format_inr)
    formatted_ch_df["Monthly Spend (₹)"] = formatted_ch_df["Monthly Spend (₹)"].apply(format_inr)
    formatted_ch_df["CPL (₹)"] = formatted_ch_df["CPL (₹)"].apply(format_inr)
    formatted_ch_df["CAC (₹)"] = formatted_ch_df["CAC (₹)"].apply(format_inr)

    st.dataframe(formatted_ch_df, use_container_width=True, hide_index=True)

    # Automated Channel Insights
    st.markdown("#### 💡 Growth Takeaways by Channel")
    ig_row = channel_stats[channel_stats["Channel"].str.lower() == "instagram"]
    ref_row = channel_stats[channel_stats["Channel"].str.lower() == "referral"]
    goog_row = channel_stats[channel_stats["Channel"].str.lower() == "google"]

    c_take1, c_take2 = st.columns(2)

    with c_take1:
        if not ig_row.empty:
            ig_leads = ig_row.iloc[0]["Leads"]
            ig_rate = ig_row.iloc[0]["Conversion Rate (%)"]
            st.markdown(f"""
            <div style="background:#FFF1F2; border-left:4px solid #E11D48; padding:1rem; border-radius:6px;">
                <b style="color:#9F1239;">Instagram: High Volume, Low Conversion ({ig_leads} leads @ {ig_rate}%)</b><br>
                <span style="font-size:0.88rem; color:#4C0519;">
                Instagram produces high curiosity but lower purchase readiness. Pre-qualify leads with instant automated WhatsApp questions before spending sales team call time.
                </span>
            </div>
            """, unsafe_allow_html=True)

    with c_take2:
        if not ref_row.empty:
            ref_leads = ref_row.iloc[0]["Leads"]
            ref_rate = ref_row.iloc[0]["Conversion Rate (%)"]
            st.markdown(f"""
            <div style="background:#ECFDF5; border-left:4px solid #10B981; padding:1rem; border-radius:6px;">
                <b style="color:#065F46;">Referrals: High Efficiency Channel ({ref_leads} leads @ {ref_rate}%)</b><br>
                <span style="font-size:0.88rem; color:#064E3B;">
                Referral leads convert significantly higher than paid channels with near-zero CAC. Systematize a formal customer referral reward to scale this organic channel.
                </span>
            </div>
            """, unsafe_allow_html=True)


# =============================================================================
# TAB 4: CUSTOMER FUNNEL
# =============================================================================
with tab_funnel:
    st.markdown("### 🔻 Customer Conversion Funnel & Drop-Off Diagnostics")
    st.markdown("Track prospects through the 5 key lifecycle stages: **Visitors → Leads → Contacted → Qualified → Converted**.")

    col_funnel_viz, col_funnel_stats = st.columns([1.6, 1.4])

    with col_funnel_viz:
        st.plotly_chart(render_funnel_chart(funnel_data), use_container_width=True)

    with col_funnel_stats:
        st.markdown("#### 🎯 Top-of-Funnel Configuration")
        curr_visitors = get_top_funnel_visitors()
        new_visitors = st.number_input("Estimated Monthly Website & Ad Visitors", value=curr_visitors, step=250, min_value=100)
        if new_visitors != curr_visitors:
            update_top_funnel_visitors(new_visitors)
            st.rerun()

        st.markdown("#### ⚠️ Funnel Bottleneck Identification")
        largest = funnel_data.get("largest_drop", {})
        if largest:
            st.error(f"""
            **Largest Drop-off Identified:**  
            **{largest.get('from')} ➔ {largest.get('to')}**  
            - **Drop-off Volume**: {largest.get('drop_count')} prospects lost  
            - **Drop-off Rate**: **{largest.get('drop_pct')}%** drop at this transition  
            """)

    # Stage-by-Stage Drop-Off Breakdown Table
    st.markdown("#### 📉 Step-by-Step Transition & Drop-off Analysis")
    drop_df = pd.DataFrame(funnel_data.get("drop_offs", []))
    if not drop_df.empty:
        drop_df_display = drop_df[[
            "from_stage", "to_stage", "from_count", "to_count",
            "drop_count", "drop_pct", "conversion_pct"
        ]].copy()
        drop_df_display.columns = [
            "Stage From", "Stage To", "Entering Count", "Passing Count",
            "Lost Count", "Drop-Off %", "Passing Conversion %"
        ]
        drop_df_display["Drop-Off %"] = drop_df_display["Drop-Off %"].apply(lambda x: f"{x}%")
        drop_df_display["Passing Conversion %"] = drop_df_display["Passing Conversion %"].apply(lambda x: f"{x}%")
        st.dataframe(drop_df_display, use_container_width=True, hide_index=True)

    st.markdown("---")
    col_loss_chart, col_loss_rec = st.columns([1.5, 1.5])

    with col_loss_chart:
        st.plotly_chart(render_loss_reasons_chart(loss_reasons), use_container_width=True)

    with col_loss_rec:
        st.markdown("#### 🔍 Root-Cause Investigation: Why Are We Losing Deals?")
        if not loss_reasons.empty:
            top_reason = loss_reasons.iloc[0]["Reason"]
            top_cnt = loss_reasons.iloc[0]["Count"]
            top_pct = loss_reasons.iloc[0]["Percentage (%)"]
            st.warning(f"""
            **Primary Failure Mode: {top_reason}**  
            Responsible for **{top_cnt} lost deals ({top_pct}%)**.
            
            **Growth Generalist Diagnostic Checklist:**
            1. **If Price:** Offer entry-level pricing tiers or split payments rather than discounting your core package.
            2. **If Competitor:** Create a 1-page battlecard highlighting specific differentiators (guarantees, turnaround, reviews).
            3. **If Response Delay:** Implement 5-minute WhatsApp instant response. Lead conversion drops 8x if not contacted within 1 hour.
            """)


# =============================================================================
# TAB 5: COMPETITOR ANALYSIS
# =============================================================================
with tab_competitors:
    st.markdown("### ⚔️ Competitor Intelligence & Benchmarking")
    st.markdown("Monitor pricing, customer sentiment (Google Ratings), digital presence, and identify strategic gaps to capture market share.")

    # Competitor positioning chart
    st.plotly_chart(render_competitor_matrix(competitors_df), use_container_width=True)

    # Opportunity Highlight
    comp_c = competitors_df[competitors_df["name"].str.contains("Competitor C", case=False, na=False)]
    if not comp_c.empty:
        st.success("""
        💡 **Strategic Opportunity Detected:**  
        **Competitor C** has strong customer ratings (★4.7) but **NO website** and **low social presence**.  
        *Opportunity:* Run Google Search Ads targeting their brand name and local service keywords. Local customers seeking them online will find your instant booking portal first!
        """)

    # Competitor Table
    st.markdown("#### 📋 Competitor Benchmark Matrix")
    display_comp = competitors_df[[
        "id", "name", "price", "google_rating", "website",
        "social_presence", "strengths", "weaknesses", "notes"
    ]].copy()
    display_comp["price"] = display_comp["price"].apply(format_inr)
    display_comp["google_rating"] = display_comp["google_rating"].apply(lambda x: f"★{x}")
    st.dataframe(display_comp, use_container_width=True, hide_index=True)

    # Add Competitor Form
    with st.expander("➕ Add New Competitor to Benchmark", expanded=False):
        with st.form("new_comp_form", clear_on_submit=True):
            col_cp1, col_cp2 = st.columns(2)
            with col_cp1:
                cp_name = st.text_input("Competitor Name *", placeholder="e.g. Acme Agency")
                cp_price = st.number_input("Base Price (₹) *", min_value=0.0, step=100.0, value=899.0)
                cp_rating = st.number_input("Google Rating (1.0 - 5.0) *", min_value=1.0, max_value=5.0, step=0.1, value=4.5)
            with col_cp2:
                cp_web = st.selectbox("Has Active Website?", options=["Yes", "No"])
                cp_soc = st.selectbox("Social Media Presence", options=["High", "Medium", "Low"])
                cp_prod = st.text_input("Service Offered", value="Growth Consulting")

            cp_str = st.text_input("Key Strengths", placeholder="e.g. Strong brand reputation, low pricing")
            cp_weak = st.text_input("Key Weaknesses", placeholder="e.g. Poor customer support, no online booking")
            cp_notes = st.text_area("Strategic Notes", placeholder="e.g. Heavy Meta ad spender in Q3")

            if st.form_submit_button("Add Competitor", use_container_width=True):
                if not cp_name.strip():
                    st.error("Competitor name is required.")
                else:
                    insert_competitor({
                        "name": cp_name,
                        "product_service": cp_prod,
                        "price": cp_price,
                        "google_rating": cp_rating,
                        "website": cp_web,
                        "social_presence": cp_soc,
                        "strengths": cp_str,
                        "weaknesses": cp_weak,
                        "notes": cp_notes
                    })
                    st.success(f"Competitor '{cp_name}' added successfully!")
                    st.rerun()


# =============================================================================
# TAB 6: GROWTH RECOMMENDATIONS
# =============================================================================
with tab_recommendations:
    st.markdown("### 🤖 Rule-Based Growth Recommendation Engine")
    st.markdown("Actionable, data-backed interventions generated by analyzing lead flow, conversion ratios, sales bottlenecks, and competitor positioning.")

    # Filter recommendations by priority
    col_rf1, col_rf2 = st.columns([1, 3])
    with col_rf1:
        p_filter = st.selectbox("Filter Priority", options=["All Priorities", "Critical", "High Opportunity", "Optimization"])

    filtered_recs = recommendations
    if p_filter != "All Priorities":
        filtered_recs = [r for r in recommendations if r["priority"].lower() == p_filter.lower()]

    if not filtered_recs:
        st.info("No recommendations match the selected priority filter.")

    for rec in filtered_recs:
        p = rec["priority"]
        badge_class = "badge-critical" if p == "Critical" else ("badge-opportunity" if p == "High Opportunity" else "badge-opt")
        card_class = "Critical" if p == "Critical" else ("High_Opportunity" if p == "High Opportunity" else "Optimization")

        playbook_html = "".join([f"<li>{step}</li>" for step in rec.get("action_playbook", [])])

        st.markdown(f"""
        <div class="rec-card {card_class}">
            <div class="rec-header">
                <span class="rec-title">{rec['title']}</span>
                <span class="{badge_class}">{rec['priority']}</span>
            </div>
            <div class="rec-trigger">⚡ <b>Trigger:</b> {rec['trigger']}</div>
            <div class="rec-body"><b>Recommendation:</b> {rec['recommendation']}</div>
            <div class="rec-impact">🎯 <b>Expected Impact:</b> {rec['expected_impact']}</div>
            <div style="margin-top: 0.6rem; font-size: 0.88rem; color: #334155;">
                <b>Tactical Action Playbook:</b>
                <ul style="margin-top: 0.3rem; padding-left: 1.2rem;">
                    {playbook_html}
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)


# =============================================================================
# TAB 7: ASK GROWTHPILOT (SIMULATOR & Q&A)
# =============================================================================
with tab_simulator:
    st.markdown("### 💡 Ask GrowthPilot: Interactive Growth Scenario Simulator")
    st.markdown("Test growth hypotheses: See how changes in conversion rates or ad budget shifts impact revenue, customer count, and blended CAC.")

    sim_col1, sim_col2 = st.columns(2)

    with sim_col1:
        st.markdown("""
        <div class="sim-card">
            <h4>🧪 Scenario 1: Conversion Rate Optimization</h4>
            <p style="font-size:0.85rem; color:#64748B;">Simulate the business impact of lifting overall lead conversion.</p>
        </div>
        """, unsafe_allow_html=True)

        current_rate = kpis["conversion_rate"]
        target_rate = st.slider(
            "Target Conversion Rate (%)",
            min_value=1.0,
            max_value=35.0,
            value=max(12.0, current_rate + 4.0),
            step=0.5
        )

        total_l = kpis["total_leads"]
        curr_cust = kpis["converted_leads"]
        sim_cust = round(total_l * (target_rate / 100))
        delta_cust = sim_cust - curr_cust
        aov = kpis["aov"] if kpis["aov"] > 0 else 10000.0
        delta_rev = delta_cust * aov

        st.metric(
            label="Projected Total Customers",
            value=f"{sim_cust}",
            delta=f"{'+' if delta_cust >= 0 else ''}{delta_cust} customers"
        )
        st.metric(
            label="Projected Revenue Impact",
            value=format_inr(kpis["total_revenue"] + delta_rev),
            delta=f"{'+' if delta_rev >= 0 else ''}{format_inr(delta_rev)} added revenue"
        )
        sim_cac = (kpis["total_spend"] / sim_cust) if sim_cust > 0 else 0.0
        st.metric(
            label="Projected CAC Reduction",
            value=format_inr(sim_cac),
            delta=f"-{format_inr(max(0, kpis['cac'] - sim_cac))} cheaper CAC" if kpis['cac'] > sim_cac else "0"
        )

    with sim_col2:
        st.markdown("""
        <div class="sim-card">
            <h4>🔄 Scenario 2: Budget Reallocation (Meta ➔ Google/Referral)</h4>
            <p style="font-size:0.85rem; color:#64748B;">Shift budget from low-conversion Instagram ads into high-intent Google Search.</p>
        </div>
        """, unsafe_allow_html=True)

        shift_amount = st.slider(
            "Shift Ad Budget from Instagram to Google (₹)",
            min_value=0,
            max_value=15000,
            value=5000,
            step=1000
        )

        ig_cpl = 150.0  # Approx baseline
        g_cpl = 360.0
        ig_rate = 0.08
        g_rate = 0.16

        # Lost IG leads vs Gained Google leads
        lost_ig_leads = shift_amount / ig_cpl if ig_cpl > 0 else 0
        gained_g_leads = shift_amount / g_cpl if g_cpl > 0 else 0

        lost_ig_cust = lost_ig_leads * ig_rate
        gained_g_cust = gained_g_leads * g_rate
        net_cust = gained_g_cust - lost_ig_cust
        net_rev = net_cust * aov

        st.metric(
            label="Net Converted Customer Change",
            value=f"{round(net_cust, 1)}",
            delta=f"{'+' if net_cust >= 0 else ''}{round(net_cust, 1)} net new customers"
        )
        st.metric(
            label="Net Projected Revenue Change",
            value=format_inr(net_rev),
            delta=f"{'+' if net_rev >= 0 else ''}{format_inr(net_rev)} without extra ad spend"
        )

    # Preset Growth Intelligence Q&A
    st.markdown("---")
    st.markdown("#### 💬 Ask GrowthPilot: Instant Business Insights")
    q_choice = st.selectbox(
        "Choose a key strategic growth question:",
        options=[
            "Why are we losing leads?",
            "Which marketing channel delivers the highest ROI?",
            "Where is the biggest bottleneck in our funnel?",
            "What should the growth team focus on this week?"
        ]
    )

    if q_choice == "Why are we losing leads?":
        if not loss_reasons.empty:
            top = loss_reasons.iloc[0]
            st.info(f"""
            **Lead Loss Analysis:**  
            The #1 reason is **'{top['Reason']}'**, representing **{top['Percentage (%)']}%** of all lost leads ({top['Count']} total leads).  
            **Recommendation:** Address this objection directly in your sales collateral. If price-driven, introduce 2-stage milestone payments or an entry-level tier.
            """)
        else:
            st.info("No lost leads recorded yet.")

    elif q_choice == "Which marketing channel delivers the highest ROI?":
        st.success(f"""
        **Channel ROI Analysis:**  
        **{kpis['best_channel']}** is your best performing channel with a **{kpis['best_channel_rate']}% conversion rate**.  
        Referral and direct organic channels have the lowest Customer Acquisition Cost (CAC), whereas Instagram provides scale but requires stricter pre-qualification.
        """)

    elif q_choice == "Where is the biggest bottleneck in our funnel?":
        largest = funnel_data.get("largest_drop", {})
        st.warning(f"""
        **Funnel Bottleneck Analysis:**  
        Your largest drop occurs at **{largest.get('from')} ➔ {largest.get('to')}** with a **{largest.get('drop_pct')}% drop-off** ({largest.get('drop_count')} prospects).  
        **Recommendation:** Shorten response times to under 15 minutes and refine the initial discovery script.
        """)

    elif q_choice == "What should the growth team focus on this week?":
        st.markdown(f"""
        **Top 3 Weekly Growth Priorities:**
        1. **Follow-up Sprint:** Clear the **{kpis['follow_up_pending']} pending follow-ups** (especially the {kpis['follow_up_overdue']} overdue leads).
        2. **Referral Program:** Double down on **Referrals** ({kpis['best_channel_rate']}% conversion rate) by asking recent converted clients for 1 peer introduction.
        3. **Instagram Lead Form:** Add 1-2 qualification filter questions to Instagram ads to stop unqualified leads from wasting sales call time.
        """)
