"""
Plotly Chart Generators for GrowthPilot Dashboard.
Provides responsive, high-aesthetic visualizations for funnel drop-offs,
channel performance, CAC/CPL economics, and competitor positioning.
"""

from typing import Dict, Any, List
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from analytics import format_inr


# Theme palette
PALETTE = {
    "primary": "#3B82F6",
    "secondary": "#6366F1",
    "success": "#10B981",
    "warning": "#F59E0B",
    "danger": "#EF4444",
    "dark": "#0F172A",
    "grid": "#F1F5F9",
    "channels": {
        "Instagram": "#E1306C",
        "Google": "#4285F4",
        "WhatsApp": "#25D366",
        "Referral": "#8B5CF6",
        "Website": "#06B6D4",
        "Direct": "#64748B"
    }
}


def render_funnel_chart(funnel_data: Dict[str, Any]) -> go.Figure:
    """Generates an interactive conversion funnel chart with drop-off percentages."""
    stages = funnel_data.get("stages", [])
    if not stages:
        return go.Figure()

    labels = [s["stage"] for s in stages]
    values = [s["count"] for s in stages]

    fig = go.Figure(go.Funnel(
        y=labels,
        x=values,
        textinfo="value+percent previous+percent initial",
        opacity=0.9,
        marker={
            "color": ["#3B82F6", "#6366F1", "#8B5CF6", "#EC4899", "#10B981"],
            "line": {"width": 1, "color": "#FFFFFF"}
        },
        connector={"line": {"color": "#CBD5E1", "dash": "dot", "width": 2}}
    ))

    fig.update_layout(
        title={
            "text": "<b>Customer Conversion Funnel & Stage Drop-Offs</b>",
            "y": 0.95, "x": 0.5, "xanchor": "center", "yanchor": "top"
        },
        margin=dict(l=20, r=20, t=60, b=20),
        height=380,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", size=13, color="#1E293B")
    )
    return fig


def render_channel_comparison(channel_df: pd.DataFrame) -> go.Figure:
    """Renders dual-axis chart: Lead Volume (Bars) vs. Conversion Rate % (Line/Markers)."""
    if channel_df.empty:
        return go.Figure()

    df = channel_df.sort_values(by="Leads", ascending=False)

    fig = go.Figure()

    # Bar: Lead Volume
    fig.add_trace(go.Bar(
        x=df["Channel"],
        y=df["Leads"],
        name="Lead Volume",
        marker_color="#3B82F6",
        opacity=0.85,
        text=df["Leads"],
        textposition="outside",
        yaxis="y1"
    ))

    # Line/Scatter: Conversion Rate %
    fig.add_trace(go.Scatter(
        x=df["Channel"],
        y=df["Conversion Rate (%)"],
        name="Conversion Rate (%)",
        mode="lines+markers+text",
        marker=dict(size=10, color="#10B981", symbol="circle"),
        line=dict(color="#10B981", width=3),
        text=[f"{val}%" for val in df["Conversion Rate (%)"]],
        textposition="top center",
        yaxis="y2"
    ))

    fig.update_layout(
        title={
            "text": "<b>Marketing Channel Volume vs. Conversion Rate</b>",
            "y": 0.95, "x": 0.5, "xanchor": "center"
        },
        xaxis=dict(title="<b>Marketing Channel</b>"),
        yaxis=dict(
            title="<b>Total Leads</b>",
            showgrid=True,
            gridcolor=PALETTE["grid"]
        ),
        yaxis2=dict(
            title="<b>Conversion Rate (%)</b>",
            overlaying="y",
            side="right",
            range=[0, max(df["Conversion Rate (%)"].max() * 1.3, 40)],
            showgrid=False
        ),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=20, r=20, t=70, b=30),
        height=380,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", size=12, color="#1E293B")
    )
    return fig


def render_cpl_cac_chart(channel_df: pd.DataFrame) -> go.Figure:
    """Renders grouped bar chart comparing Cost Per Lead (CPL) vs Customer Acquisition Cost (CAC)."""
    if channel_df.empty:
        return go.Figure()

    df = channel_df[channel_df["Monthly Spend (₹)"] > 0].copy()
    if df.empty:
        return go.Figure()

    fig = go.Figure()

    fig.add_trace(go.Bar(
        name="Cost Per Lead (CPL)",
        x=df["Channel"],
        y=df["CPL (₹)"],
        marker_color="#93C5FD",
        text=[f"₹{int(val)}" for val in df["CPL (₹)"]],
        textposition="auto"
    ))

    fig.add_trace(go.Bar(
        name="Customer Acquisition Cost (CAC)",
        x=df["Channel"],
        y=df["CAC (₹)"],
        marker_color="#3B82F6",
        text=[f"₹{int(val)}" for val in df["CAC (₹)"]],
        textposition="auto"
    ))

    fig.update_layout(
        title={
            "text": "<b>Acquisition Unit Economics: CPL vs. CAC (₹)</b>",
            "y": 0.95, "x": 0.5, "xanchor": "center"
        },
        barmode="group",
        xaxis=dict(title="<b>Marketing Channel</b>"),
        yaxis=dict(title="<b>Cost (₹)</b>", showgrid=True, gridcolor=PALETTE["grid"]),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=20, r=20, t=70, b=30),
        height=360,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", size=12, color="#1E293B")
    )
    return fig


def render_revenue_donut(channel_df: pd.DataFrame) -> go.Figure:
    """Renders a donut chart illustrating revenue contribution by channel."""
    if channel_df.empty or channel_df["Revenue (₹)"].sum() == 0:
        return go.Figure()

    df = channel_df[channel_df["Revenue (₹)"] > 0]

    colors = [PALETTE["channels"].get(ch, "#64748B") for ch in df["Channel"]]

    fig = go.Figure(data=[go.Pie(
        labels=df["Channel"],
        values=df["Revenue (₹)"],
        hole=0.55,
        marker=dict(colors=colors, line=dict(color="#FFFFFF", width=2)),
        textinfo="label+percent",
        hovertemplate="<b>%{label}</b><br>Revenue: ₹%{value:,.0f}<br>Share: %{percent}<extra></extra>"
    )])

    fig.update_layout(
        title={
            "text": "<b>Revenue Share by Channel</b>",
            "y": 0.95, "x": 0.5, "xanchor": "center"
        },
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5),
        margin=dict(l=20, r=20, t=50, b=50),
        height=360,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", size=12, color="#1E293B")
    )
    return fig


def render_lead_timeline(leads_df: pd.DataFrame) -> go.Figure:
    """Renders daily lead creation timeline with converted leads overlay."""
    if leads_df.empty:
        return go.Figure()

    df = leads_df.copy()
    df["date_created"] = pd.to_datetime(df["date_created"])
    daily = df.groupby(df["date_created"].dt.date).agg(
        total_leads=("id", "count"),
        conversions=("conversion_status", lambda x: (x.str.lower() == "converted").sum())
    ).reset_index()

    daily = daily.sort_values("date_created")

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=daily["date_created"],
        y=daily["total_leads"],
        name="New Leads",
        marker_color="#CBD5E1",
        opacity=0.75
    ))

    fig.add_trace(go.Scatter(
        x=daily["date_created"],
        y=daily["conversions"],
        name="Conversions",
        mode="lines+markers",
        line=dict(color="#10B981", width=3),
        marker=dict(size=7, color="#10B981")
    ))

    fig.update_layout(
        title={
            "text": "<b>Lead Acquisition & Conversion Trend</b>",
            "y": 0.95, "x": 0.5, "xanchor": "center"
        },
        xaxis=dict(title="<b>Date</b>"),
        yaxis=dict(title="<b>Count</b>", showgrid=True, gridcolor=PALETTE["grid"]),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=20, r=20, t=70, b=30),
        height=320,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", size=12, color="#1E293B")
    )
    return fig


def render_competitor_matrix(competitors_df: pd.DataFrame) -> go.Figure:
    """
    Renders Competitor Positioning Matrix:
    X: Price (₹)
    Y: Google Rating (1.0 - 5.0)
    Color/Size: Social Presence & Website
    """
    if competitors_df.empty:
        return go.Figure()

    df = competitors_df.copy()

    # Convert social presence to bubble size
    size_map = {"Low": 18, "Medium": 26, "High": 36}
    df["bubble_size"] = df["social_presence"].map(size_map).fillna(20)

    color_map = {"Yes": "#10B981", "No": "#EF4444"}
    df["website_color"] = df["website"].map(color_map).fillna("#64748B")

    fig = go.Figure()

    for _, row in df.iterrows():
        fig.add_trace(go.Scatter(
            x=[row["price"]],
            y=[row["google_rating"]],
            mode="markers+text",
            name=row["name"],
            text=[f"<b>{row['name']}</b><br>₹{int(row['price'])} | ★{row['google_rating']}"],
            textposition="top center",
            marker=dict(
                size=row["bubble_size"],
                color="#10B981" if row["website"] == "Yes" else "#EF4444",
                opacity=0.85,
                line=dict(width=2, color="#0F172A")
            ),
            hovertemplate=(
                f"<b>{row['name']}</b><br>"
                f"Price: ₹{row['price']:,.0f}<br>"
                f"Google Rating: ★{row['google_rating']}<br>"
                f"Website: {row['website']}<br>"
                f"Social Presence: {row['social_presence']}<br>"
                f"Strengths: {row.get('strengths', 'N/A')}<br>"
                "<extra></extra>"
            )
        ))

    # Add quadrant reference lines
    avg_price = df["price"].mean()
    fig.add_vline(x=avg_price, line_dash="dash", line_color="#94A3B8", annotation_text="Avg Price")
    fig.add_hline(y=4.4, line_dash="dash", line_color="#94A3B8", annotation_text="High Rating (4.4+)")

    fig.update_layout(
        title={
            "text": "<b>Competitor Landscape: Price vs. Google Rating</b><br><span style='font-size:11px;color:#64748B'>Green: Has Website | Red: No Website | Bubble Size: Social Presence</span>",
            "y": 0.95, "x": 0.5, "xanchor": "center"
        },
        xaxis=dict(
            title="<b>Price (₹)</b>",
            showgrid=True,
            gridcolor=PALETTE["grid"],
            range=[df["price"].min() * 0.85, df["price"].max() * 1.15]
        ),
        yaxis=dict(
            title="<b>Google Rating (★)</b>",
            showgrid=True,
            gridcolor=PALETTE["grid"],
            range=[3.8, 5.0]
        ),
        showlegend=False,
        margin=dict(l=20, r=20, t=80, b=30),
        height=420,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", size=12, color="#1E293B")
    )
    return fig


def render_loss_reasons_chart(loss_df: pd.DataFrame) -> go.Figure:
    """Renders a horizontal bar chart of lost lead reasons."""
    if loss_df.empty:
        return go.Figure()

    df = loss_df.sort_values(by="Count", ascending=True)

    fig = go.Figure(go.Bar(
        x=df["Count"],
        y=df["Reason"],
        orientation="h",
        marker_color="#F87171",
        text=[f"{c} ({p}%)" for c, p in zip(df["Count"], df["Percentage (%)"])],
        textposition="outside"
    ))

    fig.update_layout(
        title={
            "text": "<b>Primary Reasons Why Leads Were Lost</b>",
            "y": 0.95, "x": 0.5, "xanchor": "center"
        },
        xaxis=dict(title="<b>Number of Lost Leads</b>", showgrid=True, gridcolor=PALETTE["grid"]),
        yaxis=dict(title=""),
        margin=dict(l=20, r=40, t=50, b=30),
        height=320,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", size=12, color="#1E293B")
    )
    return fig
