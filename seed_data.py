"""
Seed data generator for GrowthPilot.
Populates SQLite with realistic business data reflecting Indian local market context.
Also generates a sample CSV for testing the import functionality.
"""

import random
from datetime import datetime, timedelta, date
from pathlib import Path
import pandas as pd
from database import (
    init_db,
    insert_lead,
    update_marketing_spend,
    update_top_funnel_visitors,
    insert_competitor,
    reset_and_seed_database
)

FIRST_NAMES = [
    "Rahul", "Sneha", "Amit", "Priya", "Rohan", "Ananya", "Vikram", "Pooja",
    "Karan", "Divya", "Arjun", "Neha", "Aditya", "Meera", "Siddharth", "Tanvi",
    "Manish", "Rhea", "Nikhil", "Shreya", "Deepak", "Aarav", "Simran", "Varun",
    "Ishita", "Gaurav", "Sanya", "Harsh", "Kavya", "Akash", "Ritu", "Mohit",
    "Tara", "Yash", "Bhavna", "Rajesh", "Sunita", "Alok", "Nandini", "Kunal"
]

LAST_NAMES = [
    "Sharma", "Verma", "Patel", "Mehta", "Singh", "Gupta", "Deshmukh", "Chopra",
    "Reddy", "Nair", "Kapoor", "Joshi", "Iyer", "Bhatia", "Malhotra", "Agarwal"
]

PRODUCTS = [
    "Growth Consulting Package",
    "Premium Dental Plan",
    "Annual Gym Membership",
    "Local SEO & Website Revamp",
    "Executive Coaching Session",
    "Digital Marketing Accelerator"
]

SERVICES_BY_PRICE = {
    "Growth Consulting Package": 15000,
    "Premium Dental Plan": 8000,
    "Annual Gym Membership": 12000,
    "Local SEO & Website Revamp": 18000,
    "Executive Coaching Session": 6000,
    "Digital Marketing Accelerator": 22000,
}

CHANNELS = ["Instagram", "Google", "WhatsApp", "Referral", "Website"]

LOSS_REASONS = [
    "Price too high",
    "Chose competitor",
    "No response after 3 follow-ups",
    "Timing not right",
    "Looking for cheaper alternatives",
    "Feature mismatch / Needs out of scope"
]


def seed_database():
    """Seeds the database with prompt-accurate sample data."""
    print("Initializing database...")
    reset_and_seed_database()

    # 1. Marketing Costs (Monthly Spend)
    spend_data = {
        "Instagram": 18000.0,
        "Google": 16000.0,
        "WhatsApp": 3500.0,
        "Referral": 2500.0,
        "Website": 6000.0
    }
    for channel, spend in spend_data.items():
        update_marketing_spend(channel, spend)

    # 2. Top-of-Funnel Visitors (1,000 Visitors baseline as per prompt)
    update_top_funnel_visitors(1000)

    # 3. Competitor Benchmarking (Matching prompt specifications)
    competitors = [
        {
            "name": "Competitor A",
            "product_service": "Growth & Marketing Services",
            "price": 999.0,
            "google_rating": 4.5,
            "website": "Yes",
            "social_presence": "High",
            "strengths": "Aggressive social media ads, large existing brand awareness.",
            "weaknesses": "Slower onboarding, generic customer support.",
            "notes": "Spends heavily on Instagram reels and paid Meta influencers."
        },
        {
            "name": "Competitor B",
            "product_service": "Growth & Marketing Services",
            "price": 799.0,
            "google_rating": 4.2,
            "website": "Yes",
            "social_presence": "Medium",
            "strengths": "Discount pricing leader, quick sign-up flow.",
            "weaknesses": "Lowest retention and lower customer satisfaction rating.",
            "notes": "Undercuts pricing but struggles with lead conversion quality."
        },
        {
            "name": "Competitor C",
            "product_service": "Growth & Marketing Services",
            "price": 899.0,
            "google_rating": 4.7,
            "website": "No",
            "social_presence": "Low",
            "strengths": "Highest customer satisfaction, strong offline word-of-mouth.",
            "weaknesses": "No dedicated website, virtually no digital or search presence.",
            "notes": "Strong customer ratings but weak digital presence, creating an opportunity to capture their search demand."
        },
        {
            "name": "Competitor D (Local Studio)",
            "product_service": "Premium Specialized Services",
            "price": 1299.0,
            "google_rating": 4.8,
            "website": "Yes",
            "social_presence": "Medium",
            "strengths": "High-end bespoke positioning, luxury client base.",
            "weaknesses": "High price barrier, limited package options for small businesses.",
            "notes": "Targets high-ticket corporate accounts."
        }
    ]
    for comp in competitors:
        insert_competitor(comp)

    # 4. Core Explicit Leads from Prompt
    explicit_leads = [
        {
            "name": "Rahul Sharma",
            "phone": "+91 98201 11223",
            "email": "rahul.sharma@example.com",
            "source": "Instagram",
            "product_service": "Premium Dental Plan",
            "lead_status": "Converted",
            "date_created": (date.today() - timedelta(days=2)).isoformat(),
            "follow_up_date": None,
            "conversion_status": "Converted",
            "revenue": 8000.0,
            "loss_reason": None,
            "notes": "Inquired via Instagram DM, interested in comprehensive package."
        },
        {
            "name": "Sneha Patel",
            "phone": "+91 98334 55667",
            "email": "sneha.p@example.com",
            "source": "Google",
            "product_service": "Growth Consulting Package",
            "lead_status": "Follow-up",
            "date_created": (date.today() - timedelta(days=1)).isoformat(),
            "follow_up_date": (date.today() + timedelta(days=1)).isoformat(),
            "conversion_status": "Follow-up",
            "revenue": 0.0,
            "loss_reason": None,
            "notes": "Requested price proposal via Google Search ad landing page."
        },
        {
            "name": "Amit Mehta",
            "phone": "+91 98112 44990",
            "email": "amit.mehta@example.com",
            "source": "Referral",
            "product_service": "Annual Gym Membership",
            "lead_status": "Converted",
            "date_created": (date.today() - timedelta(days=5)).isoformat(),
            "follow_up_date": None,
            "conversion_status": "Converted",
            "revenue": 12000.0,
            "loss_reason": None,
            "notes": "Referred by Dr. Verma. Paid full upfront after initial walkthrough."
        },
        {
            "name": "Priya Singh",
            "phone": "+91 99220 33881",
            "email": "priya.singh@example.com",
            "source": "Website",
            "product_service": "Local SEO & Website Revamp",
            "lead_status": "Lost",
            "date_created": (date.today() - timedelta(days=7)).isoformat(),
            "follow_up_date": None,
            "conversion_status": "Lost",
            "revenue": 0.0,
            "loss_reason": "Price too high",
            "notes": "Stated current marketing budget is too small for full revamp."
        }
    ]

    for lead in explicit_leads:
        insert_lead(lead)

    # 5. Generate realistic statistical distribution
    # Total funnel: ~250 Leads total (matching prompt funnel: 1000 Visitors -> 250 Leads -> 180 Contacted -> 80 Qualified -> 32 Converted)
    # Channel distribution matching prompt dynamics:
    # Instagram: ~120 leads, ~8% conversion rate (~10 converted)
    # Google: ~45 leads, ~16% conversion (~7 converted)
    # Referral: ~35 leads, ~31% conversion (~11 converted)
    # WhatsApp: ~25 leads, ~20% conversion (~5 converted)
    # Website: ~21 leads, ~14% conversion (~3 converted)
    # Total converted: ~36 converted (close to 32)
    # Funnel status counts across 250 leads:
    # Converted: ~32-36
    # Qualified (not yet converted or lost in qualification): ~44
    # Contacted (contacted but dropped before qualified): ~100
    # New (leads not yet contacted): ~70

    target_channel_configs = {
        "Instagram": {"total": 116, "conv_prob": 0.08, "contacted_prob": 0.70, "qualified_prob": 0.25},
        "Google": {"total": 44, "conv_prob": 0.16, "contacted_prob": 0.80, "qualified_prob": 0.40},
        "Referral": {"total": 34, "conv_prob": 0.32, "contacted_prob": 0.95, "qualified_prob": 0.70},
        "WhatsApp": {"total": 25, "conv_prob": 0.20, "contacted_prob": 0.85, "qualified_prob": 0.45},
        "Website": {"total": 27, "conv_prob": 0.12, "contacted_prob": 0.75, "qualified_prob": 0.30}
    }

    random.seed(42)  # Deterministic seed for reproducible testing
    all_seeded_records = []

    for channel, cfg in target_channel_configs.items():
        total_channel_leads = cfg["total"]
        conv_target = round(total_channel_leads * cfg["conv_prob"])
        conv_count = 0

        for i in range(total_channel_leads):
            first = random.choice(FIRST_NAMES)
            last = random.choice(LAST_NAMES)
            name = f"{first} {last}"
            phone = f"+91 9{random.randint(100000000, 999999999)}"
            email = f"{first.lower()}.{last.lower()}{random.randint(1, 99)}@gmail.com"
            prod = random.choice(PRODUCTS)
            base_price = SERVICES_BY_PRICE[prod]

            days_ago = random.randint(1, 45)
            created_dt = date.today() - timedelta(days=days_ago)

            # Target status assignment to match prompt funnel:
            # 250 Leads -> 180 Contacted -> 80 Qualified -> 32 Converted
            roll = random.random()
            if conv_count < conv_target and (roll < (conv_target / total_channel_leads) * 1.4 or i >= total_channel_leads - (conv_target - conv_count)):
                status = "Converted"
                conv_status = "Converted"
                revenue = float(base_price + random.choice([-1000, 0, 1000, 2000]))
                loss_reason = None
                follow_up = None
                notes = f"Converted via {channel}. Active client."
                conv_count += 1
            else:
                # Assign non-converted statuses:
                # ~28% New (uncontacted -> leaves ~180 contacted)
                # ~40% Contacted or Lost-at-contact (drops before qualification)
                # ~19% Follow-up or Qualified (qualified pipeline)
                sub_roll = random.random()
                if sub_roll < 0.28:
                    status = "New"
                    conv_status = "Pending"
                    revenue = 0.0
                    loss_reason = None
                    follow_up = None
                    notes = "New inbound lead. Needs first contact."
                elif sub_roll < 0.48:
                    status = "Contacted"
                    conv_status = "Pending"
                    revenue = 0.0
                    loss_reason = None
                    follow_up = (date.today() + timedelta(days=random.randint(0, 2))).isoformat()
                    notes = "Reached out via phone/WhatsApp, awaiting reply."
                elif sub_roll < 0.68:
                    status = "Lost"
                    conv_status = "Lost"
                    revenue = 0.0
                    loss_reason = random.choice(LOSS_REASONS)
                    follow_up = None
                    notes = f"Lost during initial contact. Reason: {loss_reason}."
                elif sub_roll < 0.88:
                    status = "Follow-up"
                    conv_status = "Follow-up"
                    revenue = 0.0
                    loss_reason = None
                    f_offset = random.choice([-3, -1, 0, 1, 2, 4])
                    follow_up = (date.today() + timedelta(days=f_offset)).isoformat()
                    notes = "Follow-up scheduled. Needs customized proposal."
                else:
                    status = "Qualified"
                    conv_status = "Pending"
                    revenue = 0.0
                    loss_reason = None
                    follow_up = (date.today() + timedelta(days=random.randint(1, 3))).isoformat()
                    notes = "Lead qualified. Demo / initial consult scheduled."

            lead_data = {
                "name": name,
                "phone": phone,
                "email": email,
                "source": channel,
                "product_service": prod,
                "lead_status": status,
                "date_created": created_dt.isoformat(),
                "follow_up_date": follow_up,
                "conversion_status": conv_status,
                "revenue": revenue,
                "loss_reason": loss_reason,
                "notes": notes
            }
            insert_lead(lead_data)
            all_seeded_records.append(lead_data)

    # 6. Generate data/sample_leads.csv for manual upload testing
    data_dir = Path(__file__).parent / "data"
    data_dir.mkdir(exist_ok=True)
    sample_csv_path = data_dir / "sample_leads.csv"
    
    # Save a clean 15-lead CSV sample
    sample_df = pd.DataFrame(all_seeded_records[:15])
    sample_df.to_csv(str(sample_csv_path), index=False)
    print(f"Database seeded successfully! Created sample CSV at {sample_csv_path}")


if __name__ == "__main__":
    seed_database()
