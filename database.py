"""
Database module for GrowthPilot.
Handles SQLite database initialization, schemas, and CRUD operations.
"""

import sqlite3
import pandas as pd
from datetime import datetime, date
from pathlib import Path
from typing import Optional, List, Dict, Any

DB_PATH = Path(__file__).parent / "growthpilot.db"


def get_connection():
    """Returns a SQLite connection with row factory enabled."""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initializes database tables if they do not exist."""
    conn = get_connection()
    cursor = conn.cursor()

    # Leads Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT,
            email TEXT,
            source TEXT NOT NULL,
            product_service TEXT NOT NULL,
            lead_status TEXT NOT NULL,
            date_created TEXT NOT NULL,
            follow_up_date TEXT,
            conversion_status TEXT NOT NULL,
            revenue REAL DEFAULT 0.0,
            loss_reason TEXT,
            notes TEXT
        );
    """)

    # Marketing Spend Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS marketing_costs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            channel TEXT NOT NULL UNIQUE,
            monthly_spend REAL NOT NULL DEFAULT 0.0,
            period TEXT
        );
    """)

    # Funnel Top-of-Funnel Tracking (e.g. Website/Ad Visitors)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS funnel_metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            period TEXT NOT NULL UNIQUE,
            visitors INTEGER NOT NULL DEFAULT 1000
        );
    """)

    # Competitors Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS competitors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            product_service TEXT,
            price REAL NOT NULL,
            google_rating REAL NOT NULL,
            website TEXT NOT NULL,
            social_presence TEXT NOT NULL,
            strengths TEXT,
            weaknesses TEXT,
            notes TEXT
        );
    """)

    conn.commit()
    conn.close()


# ==========================================
# LEAD OPERATIONS
# ==========================================

def get_leads_df(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    channels: Optional[List[str]] = None,
    statuses: Optional[List[str]] = None,
) -> pd.DataFrame:
    """Fetches leads as a Pandas DataFrame with optional filters."""
    conn = get_connection()
    query = "SELECT * FROM leads WHERE 1=1"
    params = []

    if start_date:
        query += " AND date_created >= ?"
        params.append(str(start_date))
    if end_date:
        query += " AND date_created <= ?"
        params.append(str(end_date))
    if channels:
        placeholders = ",".join(["?"] * len(channels))
        query += f" AND source IN ({placeholders})"
        params.extend(channels)
    if statuses:
        placeholders = ",".join(["?"] * len(statuses))
        query += f" AND lead_status IN ({placeholders})"
        params.extend(statuses)

    query += " ORDER BY date_created DESC, id DESC"
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df


def insert_lead(lead_data: Dict[str, Any]) -> int:
    """Inserts a single lead and returns the inserted ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO leads (
            name, phone, email, source, product_service,
            lead_status, date_created, follow_up_date,
            conversion_status, revenue, loss_reason, notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        lead_data.get("name", "").strip(),
        lead_data.get("phone", "").strip(),
        lead_data.get("email", "").strip(),
        lead_data.get("source", "Direct"),
        lead_data.get("product_service", "General"),
        lead_data.get("lead_status", "New"),
        str(lead_data.get("date_created", date.today().isoformat())),
        str(lead_data.get("follow_up_date")) if lead_data.get("follow_up_date") else None,
        lead_data.get("conversion_status", "Pending"),
        float(lead_data.get("revenue", 0.0) or 0.0),
        lead_data.get("loss_reason", None),
        lead_data.get("notes", "").strip()
    ))
    conn.commit()
    lead_id = cursor.lastrowid
    conn.close()
    return lead_id


def update_lead(lead_id: int, updates: Dict[str, Any]) -> bool:
    """Updates fields of a specific lead."""
    conn = get_connection()
    cursor = conn.cursor()
    set_clauses = []
    params = []
    for key, value in updates.items():
        set_clauses.append(f"{key} = ?")
        params.append(value)
    params.append(lead_id)

    query = f"UPDATE leads SET {', '.join(set_clauses)} WHERE id = ?"
    cursor.execute(query, params)
    conn.commit()
    affected = cursor.rowcount > 0
    conn.close()
    return affected


def delete_lead(lead_id: int) -> bool:
    """Deletes a lead by ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM leads WHERE id = ?", (lead_id,))
    conn.commit()
    affected = cursor.rowcount > 0
    conn.close()
    return affected


def batch_import_leads(df: pd.DataFrame) -> int:
    """Batch imports leads from a DataFrame."""
    conn = get_connection()
    cursor = conn.cursor()
    count = 0

    for _, row in df.iterrows():
        name = str(row.get("name", "")).strip()
        if not name or name.lower() == "nan":
            continue

        revenue = 0.0
        try:
            val = row.get("revenue", 0.0)
            if pd.notna(val):
                # Clean currency symbols if present
                clean_val = str(val).replace("₹", "").replace(",", "").strip()
                revenue = float(clean_val) if clean_val else 0.0
        except Exception:
            revenue = 0.0

        follow_up = row.get("follow_up_date", None)
        if pd.isna(follow_up) or str(follow_up).strip() in ["", "nan", "None", "—", "-"]:
            follow_up = None
        else:
            follow_up = str(follow_up).strip()

        loss_reason = row.get("loss_reason", None)
        if pd.isna(loss_reason) or str(loss_reason).strip() in ["", "nan", "None", "—", "-"]:
            loss_reason = None
        else:
            loss_reason = str(loss_reason).strip()

        cursor.execute("""
            INSERT INTO leads (
                name, phone, email, source, product_service,
                lead_status, date_created, follow_up_date,
                conversion_status, revenue, loss_reason, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            name,
            str(row.get("phone", "")).replace("nan", ""),
            str(row.get("email", "")).replace("nan", ""),
            str(row.get("source", "Direct")),
            str(row.get("product_service", "General")),
            str(row.get("lead_status", "New")),
            str(row.get("date_created", date.today().isoformat())),
            follow_up,
            str(row.get("conversion_status", "Pending")),
            revenue,
            loss_reason,
            str(row.get("notes", "")).replace("nan", "")
        ))
        count += 1

    conn.commit()
    conn.close()
    return count


# ==========================================
# MARKETING SPEND OPERATIONS
# ==========================================

def get_marketing_spend_df() -> pd.DataFrame:
    """Retrieves all marketing channel spend values."""
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM marketing_costs ORDER BY monthly_spend DESC", conn)
    conn.close()
    return df


def update_marketing_spend(channel: str, monthly_spend: float, period: str = "current") -> None:
    """Upserts monthly spend for a marketing channel."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO marketing_costs (channel, monthly_spend, period)
        VALUES (?, ?, ?)
        ON CONFLICT(channel) DO UPDATE SET
            monthly_spend = excluded.monthly_spend,
            period = excluded.period
    """, (channel, monthly_spend, period))
    conn.commit()
    conn.close()


# ==========================================
# FUNNEL METRICS OPERATIONS
# ==========================================

def get_top_funnel_visitors(period: str = "current") -> int:
    """Retrieves the visitor count for top-of-funnel calculations."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT visitors FROM funnel_metrics WHERE period = ?", (period,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return int(row["visitors"])
    return 1000


def update_top_funnel_visitors(visitors: int, period: str = "current") -> None:
    """Upserts top-of-funnel visitors."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO funnel_metrics (period, visitors)
        VALUES (?, ?)
        ON CONFLICT(period) DO UPDATE SET visitors = excluded.visitors
    """, (period, visitors))
    conn.commit()
    conn.close()


# ==========================================
# COMPETITOR OPERATIONS
# ==========================================

def get_competitors_df() -> pd.DataFrame:
    """Retrieves all competitors as a DataFrame."""
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM competitors ORDER BY price ASC", conn)
    conn.close()
    return df


def insert_competitor(comp_data: Dict[str, Any]) -> int:
    """Inserts a competitor into the database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO competitors (
            name, product_service, price, google_rating,
            website, social_presence, strengths, weaknesses, notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        comp_data.get("name", "").strip(),
        comp_data.get("product_service", "General").strip(),
        float(comp_data.get("price", 0.0)),
        float(comp_data.get("google_rating", 4.0)),
        comp_data.get("website", "Yes"),
        comp_data.get("social_presence", "Medium"),
        comp_data.get("strengths", ""),
        comp_data.get("weaknesses", ""),
        comp_data.get("notes", "")
    ))
    conn.commit()
    comp_id = cursor.lastrowid
    conn.close()
    return comp_id


def delete_competitor(comp_id: int) -> bool:
    """Deletes a competitor by ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM competitors WHERE id = ?", (comp_id,))
    conn.commit()
    affected = cursor.rowcount > 0
    conn.close()
    return affected


def reset_and_seed_database():
    """Drops and re-initializes tables with default seed data."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS leads")
    cursor.execute("DROP TABLE IF EXISTS marketing_costs")
    cursor.execute("DROP TABLE IF EXISTS funnel_metrics")
    cursor.execute("DROP TABLE IF EXISTS competitors")
    conn.commit()
    conn.close()
    init_db()
