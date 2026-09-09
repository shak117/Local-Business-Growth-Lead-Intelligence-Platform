"""
Custom CSS styles and UI theme tokens for GrowthPilot dashboard.
"""

import streamlit as st


def apply_custom_styles():
    """Injects custom CSS for a polished, modern growth intelligence dashboard."""
    st.markdown("""
    <style>
        /* Import clean modern fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }

        /* Top Hero Header */
        .growth-hero {
            background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
            padding: 1.5rem 2rem;
            border-radius: 12px;
            color: #FFFFFF;
            margin-bottom: 1.5rem;
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        }

        .growth-hero h1 {
            color: #FFFFFF !important;
            font-size: 2rem !important;
            font-weight: 800 !important;
            margin: 0 !important;
            padding: 0 !important;
            letter-spacing: -0.02em;
        }

        .growth-hero p {
            color: #94A3B8 !important;
            font-size: 0.95rem !important;
            margin-top: 0.35rem !important;
            margin-bottom: 0 !important;
        }

        .hero-badge {
            background: rgba(59, 130, 246, 0.2);
            color: #60A5FA;
            border: 1px solid rgba(96, 165, 250, 0.3);
            padding: 0.25rem 0.6rem;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 600;
            display: inline-block;
            margin-bottom: 0.5rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        /* KPI Metric Cards */
        .metric-card {
            background: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 10px;
            padding: 1.1rem 1.2rem;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.02);
            transition: transform 0.15s ease, box-shadow 0.15s ease;
            height: 100%;
        }

        .metric-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.06);
            border-color: #CBD5E1;
        }

        .metric-label {
            font-size: 0.8rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.04em;
            color: #64748B;
            margin-bottom: 0.35rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .metric-value {
            font-size: 1.65rem;
            font-weight: 800;
            color: #0F172A;
            line-height: 1.2;
            letter-spacing: -0.02em;
        }

        .metric-subtext {
            font-size: 0.78rem;
            color: #94A3B8;
            margin-top: 0.35rem;
            display: flex;
            align-items: center;
            gap: 0.25rem;
        }

        .metric-subtext.positive {
            color: #10B981;
            font-weight: 600;
        }

        .metric-subtext.warning {
            color: #F59E0B;
            font-weight: 600;
        }

        .metric-subtext.critical {
            color: #EF4444;
            font-weight: 600;
        }

        /* Recommendation Cards */
        .rec-card {
            background: #FFFFFF;
            border-radius: 10px;
            padding: 1.25rem 1.4rem;
            margin-bottom: 1rem;
            border: 1px solid #E2E8F0;
            box-shadow: 0 2px 6px rgba(0,0,0,0.03);
            position: relative;
            border-left-width: 5px;
        }

        .rec-card.Critical {
            border-left-color: #EF4444;
            background: linear-gradient(90deg, rgba(239, 68, 68, 0.02) 0%, #FFFFFF 100%);
        }

        .rec-card.High_Opportunity {
            border-left-color: #F59E0B;
            background: linear-gradient(90deg, rgba(245, 158, 11, 0.02) 0%, #FFFFFF 100%);
        }

        .rec-card.Optimization {
            border-left-color: #3B82F6;
            background: linear-gradient(90deg, rgba(59, 130, 246, 0.02) 0%, #FFFFFF 100%);
        }

        .rec-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 0.5rem;
        }

        .rec-title {
            font-size: 1.05rem;
            font-weight: 700;
            color: #0F172A;
        }

        .badge-critical {
            background: #FEE2E2;
            color: #DC2626;
            font-weight: 700;
            font-size: 0.72rem;
            padding: 0.2rem 0.6rem;
            border-radius: 9999px;
            text-transform: uppercase;
        }

        .badge-opportunity {
            background: #FEF3C7;
            color: #D97706;
            font-weight: 700;
            font-size: 0.72rem;
            padding: 0.2rem 0.6rem;
            border-radius: 9999px;
            text-transform: uppercase;
        }

        .badge-opt {
            background: #DBEAFE;
            color: #2563EB;
            font-weight: 700;
            font-size: 0.72rem;
            padding: 0.2rem 0.6rem;
            border-radius: 9999px;
            text-transform: uppercase;
        }

        .rec-trigger {
            background: #F8FAFC;
            border-left: 3px solid #CBD5E1;
            padding: 0.4rem 0.75rem;
            font-size: 0.82rem;
            color: #475569;
            font-family: monospace;
            margin-bottom: 0.6rem;
            border-radius: 0 4px 4px 0;
        }

        .rec-body {
            color: #334155;
            font-size: 0.92rem;
            line-height: 1.45;
            margin-bottom: 0.6rem;
        }

        .rec-impact {
            font-size: 0.84rem;
            color: #047857;
            background: #ECFDF5;
            padding: 0.45rem 0.75rem;
            border-radius: 6px;
            font-weight: 600;
            margin-bottom: 0.6rem;
            display: inline-block;
            border: 1px solid #A7F3D0;
        }

        /* Status Pills */
        .status-pill {
            display: inline-block;
            padding: 0.2rem 0.55rem;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 600;
        }
        .status-converted { background: #D1FAE5; color: #065F46; }
        .status-followup { background: #FEF3C7; color: #92400E; }
        .status-lost { background: #FEE2E2; color: #991B1B; }
        .status-new { background: #E0E7FF; color: #3730A3; }
        .status-qualified { background: #CFFAFE; color: #155E75; }

        /* Simulator Card */
        .sim-card {
            background: #F8FAFC;
            border: 1px solid #E2E8F0;
            border-radius: 12px;
            padding: 1.5rem;
        }

        /* Streamlit clean overrides */
        div[data-testid="stMetricValue"] {
            font-size: 1.75rem !important;
            font-weight: 800 !important;
        }
    </style>
    """, unsafe_allow_html=True)
