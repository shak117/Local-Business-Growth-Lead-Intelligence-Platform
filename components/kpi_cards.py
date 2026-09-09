"""
KPI Card components for GrowthPilot.
Renders responsive, high-aesthetic metric cards with micro-labels, status indicators, and currency formatting.
"""

from typing import Dict, Any
import streamlit as st
from analytics import format_inr


def render_growth_kpi_cards(kpis: Dict[str, Any]):
    """Renders the top-level Growth & Operations KPI cards in a 4x2 responsive layout."""
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">
                <span>Total Leads</span>
                <span>📈</span>
            </div>
            <div class="metric-value">{kpis['total_leads']}</div>
            <div class="metric-subtext positive">
                <span>✔ {kpis['converted_leads']} Converted</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        conv_rate = kpis['conversion_rate']
        rate_class = "positive" if conv_rate >= 10 else ("warning" if conv_rate >= 5 else "critical")
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">
                <span>Conversion Rate</span>
                <span>🎯</span>
            </div>
            <div class="metric-value">{conv_rate}%</div>
            <div class="metric-subtext {rate_class}">
                <span>{'High Performing' if conv_rate >= 10 else ('Moderate' if conv_rate >= 5 else 'Needs Attention')}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">
                <span>Revenue Generated</span>
                <span>💰</span>
            </div>
            <div class="metric-value">{format_inr(kpis['total_revenue'])}</div>
            <div class="metric-subtext">
                <span>Avg Deal: {format_inr(kpis['aov'])}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">
                <span>Cost Per Lead (CPL)</span>
                <span>🏷️</span>
            </div>
            <div class="metric-value">{format_inr(kpis['cpl'])}</div>
            <div class="metric-subtext">
                <span>Total Spend: {format_inr(kpis['total_spend'])}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

    col5, col6, col7, col8 = st.columns(4)

    with col5:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">
                <span>Customer Acq. Cost (CAC)</span>
                <span>💳</span>
            </div>
            <div class="metric-value">{format_inr(kpis['cac'])}</div>
            <div class="metric-subtext positive">
                <span>{round((kpis['total_revenue'] / kpis['total_spend']), 1) if kpis['total_spend'] > 0 else 'N/A'}x Blended ROAS</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col6:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">
                <span>Top Performing Channel</span>
                <span>⭐</span>
            </div>
            <div class="metric-value" style="font-size: 1.35rem;">{kpis['best_channel']}</div>
            <div class="metric-subtext positive">
                <span>{kpis['best_channel_rate']}% Conv. Rate</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col7:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">
                <span>Lost Leads</span>
                <span>❌</span>
            </div>
            <div class="metric-value">{kpis['lost_leads']}</div>
            <div class="metric-subtext critical">
                <span>{round((kpis['lost_leads'] / kpis['total_leads'] * 100), 1) if kpis['total_leads'] > 0 else 0}% Drop-off Rate</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col8:
        overdue_cnt = kpis['follow_up_overdue']
        fu_class = "critical" if overdue_cnt > 0 else "positive"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">
                <span>Follow-up Pending</span>
                <span>⏳</span>
            </div>
            <div class="metric-value">{kpis['follow_up_pending']}</div>
            <div class="metric-subtext {fu_class}">
                <span>{'🚨 ' + str(overdue_cnt) + ' Overdue' if overdue_cnt > 0 else '✔ Zero Overdue'}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
