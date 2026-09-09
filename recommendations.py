"""
Growth Intelligence Recommendation Engine for GrowthPilot.
Implements rule-based business logic to deliver actionable growth strategies,
channel optimizations, sales operations alerts, and competitor counter-plays.
"""

from typing import List, Dict, Any
import pandas as pd
from analytics import format_inr


def generate_recommendations(
    kpis: Dict[str, Any],
    channel_df: pd.DataFrame,
    funnel_data: Dict[str, Any],
    loss_df: pd.DataFrame,
    competitors_df: pd.DataFrame
) -> List[Dict[str, Any]]:
    """
    Evaluates business data against Growth Generalist operational rules
    and returns prioritized, actionable growth recommendations.
    """
    recs = []

    if kpis["total_leads"] == 0:
        return [{
            "id": "REC_NO_DATA",
            "category": "Initial Setup",
            "priority": "Critical",
            "title": "No Lead Data Detected",
            "trigger": "Total leads in current filter is 0.",
            "recommendation": "Import or add initial leads to activate GrowthPilot intelligence.",
            "expected_impact": "Establish lead baseline and channel attribution.",
            "action_playbook": [
                "Import your current leads via CSV or use the Add Lead form.",
                "Verify marketing channel tracking tags (UTM parameters).",
                "Review baseline lead volume weekly."
            ]
        }]

    # =========================================================================
    # RULE 1: OVERALL CONVERSION RATE HEALTH CHECK
    # IF conversion_rate < 5% -> Review lead quality and landing page
    # =========================================================================
    conv_rate = kpis["conversion_rate"]
    if conv_rate < 5.0:
        recs.append({
            "id": "REC_LOW_CONV",
            "category": "Funnel Conversion",
            "priority": "Critical",
            "title": "Low Overall Conversion Rate Alert (< 5%)",
            "trigger": f"Current overall conversion rate is {conv_rate}%, below healthy local service benchmark of 8-15%.",
            "recommendation": "Conduct an immediate audit of your landing page copy, lead capture form friction, and lead qualification process.",
            "expected_impact": "Lifting conversion from " + f"{conv_rate}% to 8% would generate roughly {round((kpis['total_leads'] * 0.08) - kpis['converted_leads'])} additional paying customers without increasing ad spend.",
            "action_playbook": [
                "Review landing page headline clarity and reduce form fields to Name, Phone, and Need.",
                "Introduce an irresistible initial offer (e.g. Free Consultation, First Visit Diagnostic).",
                "Ensure speed-to-lead: Call new leads within 15 minutes of form submission."
            ]
        })
    elif conv_rate >= 15.0:
        recs.append({
            "id": "REC_HIGH_CONV_SCALE",
            "category": "Growth Scaling",
            "priority": "High Opportunity",
            "title": "Strong Conversion Velocity (> 15%): Ready to Scale",
            "trigger": f"Conversion rate is performing at an exceptional {conv_rate}%.",
            "recommendation": "Your offer and sales conversion are highly dialed in. Safely increase top-of-funnel ad spend by 20-30% on top channels.",
            "expected_impact": "Scale revenue proportionally while maintaining strong unit economics.",
            "action_playbook": [
                "Identify which ad creatives and search keywords produce the highest intent.",
                "Increase monthly budget on top 2 performing channels by 20%.",
                "Monitor CAC closely to ensure it does not rise by more than 15%."
            ]
        })

    # =========================================================================
    # RULE 2: INSTAGRAM VS GOOGLE EFFICIENCY MISMATCH
    # IF Instagram leads > Google leads AND Instagram conversion rate < Google
    # -> Improve Instagram lead qualification
    # =========================================================================
    if not channel_df.empty:
        ch_dict = {row["Channel"].lower(): row for _, row in channel_df.iterrows()}
        ig = ch_dict.get("instagram")
        google = ch_dict.get("google")

        if ig is not None and google is not None:
            ig_leads = ig["Leads"]
            google_leads = google["Leads"]
            ig_rate = ig["Conversion Rate (%)"]
            google_rate = google["Conversion Rate (%)"]

            if ig_leads > google_leads and ig_rate < google_rate:
                recs.append({
                    "id": "REC_IG_GOOGLE_MISMATCH",
                    "category": "Channel Optimization",
                    "priority": "High Opportunity",
                    "title": "Instagram Volume vs. Google Conversion Mismatch",
                    "trigger": f"Instagram generated {ig_leads} leads at {ig_rate}% conversion, whereas Google generated {google_leads} leads at {google_rate}% conversion.",
                    "recommendation": "Instagram is driving high casual volume with low intent. Filter Instagram leads with multi-step qualification forms or WhatsApp automation, and reallocate 15-25% of ad budget toward high-intent Google Search campaigns.",
                    "expected_impact": f"Higher qualification reduces wasted sales effort on low-intent Instagram leads, while scaling Google leads could add ~₹{format_inr(round(google_leads * 0.25 * kpis['aov']))[1:]} in qualified revenue.",
                    "action_playbook": [
                        "Add a 2-question qualification filter to Instagram Lead Ads (e.g. 'Looking to start: Within 7 days / This month').",
                        "Set up an automated WhatsApp instant response to qualify Instagram DMs within 60 seconds.",
                        "Shift ₹3,000–₹5,000/month from Meta Ads to high-intent Google Search keywords."
                    ]
                })

    # =========================================================================
    # RULE 3: REFERRAL CHANNEL SUPERPOWER
    # IF referral conversion rate > other channels
    # -> Increase referral campaigns
    # =========================================================================
    if not channel_df.empty:
        ref = ch_dict.get("referral")
        if ref is not None and ref["Leads"] >= 2:
            ref_rate = ref["Conversion Rate (%)"]
            other_rates = [
                row["Conversion Rate (%)"]
                for _, row in channel_df.iterrows()
                if row["Channel"].lower() != "referral" and row["Leads"] >= 2
            ]
            avg_other = (sum(other_rates) / len(other_rates)) if other_rates else 0.0

            if ref_rate > avg_other:
                recs.append({
                    "id": "REC_REFERRAL_BOOST",
                    "category": "Customer Advocacy",
                    "priority": "High Opportunity",
                    "title": "Amplify Referral Engine (Highest Conversion Channel)",
                    "trigger": f"Referral leads convert at {ref_rate}% (vs {round(avg_other, 1)}% across other channels) with a CAC of {format_inr(ref['CAC (₹)'])}.",
                    "recommendation": "Referrals are your most profitable acquisition channel. Systematize a formal customer referral reward program and prompt happy clients at the 'moment of delight'.",
                    "expected_impact": f"Doubling referral volume from {ref['Leads']} to {ref['Leads'] * 2} leads could yield ~{round(ref['Converted'])} additional customers at near-zero incremental ad cost.",
                    "action_playbook": [
                        "Launch a simple 2-sided incentive (e.g. 'Give ₹1,000 credit to a friend, get ₹1,000 service credit').",
                        "Send a personalized WhatsApp referral request 7 days after a successful customer milestone.",
                        "Train frontline sales staff to ask every converted client for 1-2 peers who could benefit."
                    ]
                })

    # =========================================================================
    # RULE 4: SALES OPERATIONS & FOLLOW-UP HYGIENE
    # IF follow-up pending > 20 -> Prioritize follow-up workflow
    # =========================================================================
    fu_pending = kpis["follow_up_pending"]
    fu_overdue = kpis["follow_up_overdue"]
    if fu_pending > 20 or fu_overdue > 0:
        urgency = "Critical" if (fu_overdue > 5 or fu_pending > 30) else "High Opportunity"
        recs.append({
            "id": "REC_FOLLOW_UP_HYGIENE",
            "category": "Sales Operations",
            "priority": urgency,
            "title": f"Follow-up Bottleneck: {fu_pending} Leads Pending ({fu_overdue} Overdue)",
            "trigger": f"{fu_pending} leads are stuck in 'Follow-up' status, including {fu_overdue} overdue follow-up dates.",
            "recommendation": "Lead conversion decays by 50% after 48 hours without contact. Institute a dedicated daily 'Follow-up Sprint' and deploy automated WhatsApp follow-up cadence.",
            "expected_impact": f"Re-engaging pending follow-ups typically recovers 10-15% of stalling deals (potential to recover ~{round(fu_pending * 0.12)} conversions worth ~{format_inr(round(fu_pending * 0.12 * kpis['aov']))}).",
            "action_playbook": [
                "Schedule a non-negotiable 45-minute daily sales sprint at 10:00 AM specifically for pending follow-ups.",
                "Use a 3-touch WhatsApp template sequence: Day 1 (Proposal recap), Day 3 (Case study/Proof), Day 7 (Break-up / Final offer).",
                "Mark uncontactable leads as 'Lost' after 3 unsuccessful attempts to keep the pipeline clean."
            ]
        })

    # =========================================================================
    # RULE 5: FUNNEL DROP-OFF BOTTLENECK INTERVENTION
    # Identifies the specific largest drop-off stage and provides tactical play
    # =========================================================================
    largest = funnel_data.get("largest_drop", {})
    if largest and largest.get("drop_pct", 0) > 30:
        f_stage = largest["from"]
        t_stage = largest["to"]
        drop_p = largest["drop_pct"]

        if "contacted" in f_stage.lower() and "qualified" in t_stage.lower():
            recs.append({
                "id": "REC_DROP_CONTACTED_QUALIFIED",
                "category": "Funnel Optimization",
                "priority": "Critical",
                "title": f"Funnel Bottleneck: Contacted → Qualified Drop-off ({drop_p}%)",
                "trigger": f"The largest drop in your funnel occurs between {f_stage} and {t_stage} ({drop_p}% drop-off).",
                "recommendation": "Leads are being contacted, but disqualifying or losing interest before a demo/consultation. Streamline your initial pitch and shorten response time.",
                "expected_impact": "Plugging this qualification leak could increase downstream customers by 20-35%.",
                "action_playbook": [
                    "Audit the first phone call or WhatsApp message: Is it value-first or overly aggressive sales?",
                    "Deploy an instant booking link (e.g. Calendly / WhatsApp catalog) during first contact.",
                    "Review buyer criteria to stop sales reps from chasing unqualified inbound leads."
                ]
            })
        elif "qualified" in f_stage.lower() and "converted" in t_stage.lower():
            recs.append({
                "id": "REC_DROP_QUALIFIED_CONVERTED",
                "category": "Closing Operations",
                "priority": "Critical",
                "title": f"Funnel Bottleneck: Qualified → Converted Drop-off ({drop_p}%)",
                "trigger": f"{drop_p}% of qualified prospects fail to convert into paying customers.",
                "recommendation": "Qualified leads are stalling at the decision/pricing stage. Address common objections upfront with payment plans and social proof.",
                "expected_impact": "Improving closing rate by 10% directly boosts top-line revenue without ad cost.",
                "action_playbook": [
                    "Introduce a limited-time incentive or fast-action bonus to create urgency.",
                    "Offer split-payment milestones (e.g. 50% upfront, 50% upon completion).",
                    "Send customer video testimonials or verifiable case studies right after the proposal."
                ]
            })

    # =========================================================================
    # RULE 6: COMPETITOR GAP & OPPORTUNITY ENGINE
    # Scans competitors for strategic digital or pricing weaknesses
    # =========================================================================
    if not competitors_df.empty:
        # Check for competitors with high ratings but weak digital presence (e.g. Competitor C)
        weak_digital = competitors_df[
            (competitors_df["google_rating"] >= 4.5) &
            ((competitors_df["website"].str.lower() == "no") | (competitors_df["social_presence"].str.lower() == "low"))
        ]
        if not weak_digital.empty:
            comp_names = ", ".join(weak_digital["name"].tolist())
            recs.append({
                "id": "REC_COMPETITOR_DIGITAL_GAP",
                "category": "Competitor Strategy",
                "priority": "High Opportunity",
                "title": f"Competitive Digital Arbitrage Opportunity ({comp_names})",
                "trigger": f"{comp_names} has stellar customer ratings (4.7+), but weak or nonexistent website and social presence.",
                "recommendation": "Their satisfied customers recommend them, but prospects looking for them online cannot easily book. Target competitor keyword search terms and highlight your instant online booking advantage.",
                "expected_impact": "Capture 10-20 high-intent local prospects monthly searching for alternatives to these competitors.",
                "action_playbook": [
                    "Run Google Search ads targeting searches for competitor brand terms and service keywords.",
                    "Emphasize 'Instant Online Booking & 24/7 Support' prominently on your landing page.",
                    "Build dedicated comparison landing pages showing your transparent pricing and digital convenience."
                ]
            })

        # Check pricing positioning
        avg_comp_price = competitors_df["price"].mean()
        recs.append({
            "id": "REC_COMPETITOR_PRICING_POSITION",
            "category": "Pricing Strategy",
            "priority": "Optimization",
            "title": "Value-Add Positioning Against Competitor Price Points",
            "trigger": f"Average competitor base pricing is {format_inr(avg_comp_price)}. Competitor B undercuts at {format_inr(competitors_df['price'].min())}.",
            "recommendation": "Avoid competing in a race to the bottom on price against budget competitors. Position your brand on reliability, guarantees, and premium customer experience.",
            "expected_impact": "Protects gross margin while attracting higher lifetime-value customers.",
            "action_playbook": [
                "Bundle higher-margin perks (e.g. 30-day post-service warranty or priority access) rather than discounting.",
                "Display trust badges, certifications, and Google review counters on all sales collateral.",
                "Train sales reps to ask 'What did you find lacking with cheaper alternatives?' during discovery calls."
            ]
        })

    # =========================================================================
    # RULE 7: LOST LEAD ROOT-CAUSE INTERVENTION
    # Analyzes top loss reason from lost leads
    # =========================================================================
    if not loss_df.empty:
        top_loss = loss_df.iloc[0]
        top_reason = top_loss["Reason"]
        top_pct = top_loss["Percentage (%)"]

        if "price" in top_reason.lower() and top_pct >= 25:
            recs.append({
                "id": "REC_LOSS_PRICE_OBJECTION",
                "category": "Offer Refinement",
                "priority": "Optimization",
                "title": f"Price Objection Friction ({top_pct}% of Lost Leads)",
                "trigger": f"'{top_reason}' accounts for {top_pct}% of all lost leads.",
                "recommendation": "Your core package price exceeds the cash-on-hand threshold for a segment of inbound leads. Introduce a tiered entry-level package or flexible financing.",
                "expected_impact": "Recovers 15-20% of leads who drop off due to price sensitivity.",
                "action_playbook": [
                    "Create a 'Starter Package' priced at 50% of the flagship package to secure the relationship.",
                    "Provide 2-part milestone payments or 0% EMI financing options.",
                    "Reflect ROI calculations in proposals (e.g. 'This ₹12,000 investment pays for itself with 2 clients')."
                ]
            })

    return recs
