import streamlit as st
import json
from datetime import datetime

# ===============================
# Streamlit Config
# ===============================
st.set_page_config(
    page_title="Bank Statement Analysis v5.0",
    page_icon="🏦",
    layout="wide"
)

# ===============================
# Utility: Company Name Resolver
# ===============================
def resolve_company_name(data: dict, default: str = "Unknown") -> str:
    if not isinstance(data, dict):
        return default

    r = data.get("report_info", {}) or {}

    candidates = [
        r.get("company_name"),
        r.get("company"),
        r.get("entity_name"),
        data.get("company_name"),
        data.get("company"),
        data.get("entity_name"),
    ]

    for c in candidates:
        if isinstance(c, str):
            s = c.strip()
            if s and s.lower() not in {
                "unknown", "n/a", "na", "company", "-", "null"
            }:
                return s
    return default


# ===============================
# Schema Detection
# ===============================
def detect_schema_version(data):
    schema_version = data.get("report_info", {}).get("schema_version", "")
    if schema_version.startswith("5."):
        return "5.0"

    if data.get("recurring_payments") or data.get("non_bank_financing"):
        return "5.0"

    accounts = data.get("accounts", [])
    if accounts:
        monthly = accounts[0].get("monthly_summary", [])
        if monthly and "highest_intraday" in monthly[0]:
            return "5.0"

    return "4.0"


# ===============================
# HTML Generator (UNCHANGED LOGIC)
# ===============================
def generate_interactive_html(data):
    schema_version = detect_schema_version(data)

    r = data.get("report_info", {})
    accounts = data.get("accounts", [])
    consolidated = data.get("consolidated", {})
    flags = data.get("flags", {})
    integrity = data.get("integrity_score", {})
    volatility = data.get("volatility", {})
    kite = data.get("kite_flying", {})
    observations = data.get("observations", {})
    recommendations = data.get("recommendations", [])

    company = resolve_company_name(data, default="Company")

    period_start = r.get("period_start", "")
    period_end = r.get("period_end", "")
    total_months = r.get("total_months", 0)

    int_score = integrity.get("score", 0)
    int_rating = integrity.get("rating", "N/A")

    vol_index = volatility.get("overall_index", 0)
    vol_level = volatility.get("overall_level", "LOW")

    kite_score = kite.get("risk_score", 0)
    kite_level = kite.get("risk_level", "LOW")

    html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Bank Statement Analysis - {company}</title>
<style>
body {{
    font-family: Arial, sans-serif;
    background: #0f172a;
    color: #e5e7eb;
    padding: 2rem;
}}
.card {{
    background: #020617;
    padding: 1.5rem;
    border-radius: 12px;
    margin-bottom: 1rem;
}}
h1,h2 {{
    color: #22c55e;
}}
</style>
</head>
<body>

<h1>{company}</h1>
<p>Period: {period_start} → {period_end} ({total_months} months)</p>

<div class="card">
<h2>Integrity Score</h2>
<p>{int_score}% — {int_rating}</p>
</div>

<div class="card">
<h2>Volatility</h2>
<p>{vol_index:.0f}% — {vol_level}</p>
</div>

<div class="card">
<h2>Kite Flying Risk</h2>
<p>{kite_score} — {kite_level}</p>
</div>

<div class="card">
<h2>Observations</h2>
<ul>
{''.join(f"<li>{o}</li>" for o in observations.get("positive", []))}
</ul>
</div>

<footer style="margin-top:3rem;color:#94a3b8;font-size:0.8rem">
Generated {datetime.now().isoformat()}
</footer>

</body>
</html>
"""
    return html


# ===============================
# MAIN STREAMLIT APP
# ===============================
st.title("🏦 Bank Statement Analysis v5.0")
st.caption("Backwards compatible with v4.0 schema")

uploaded_file = st.file_uploader(
    "Upload JSON Analysis Output",
    type=["json"]
)

data = None
if uploaded_file:
    try:
        data = json.load(uploaded_file)
    except Exception as e:
        st.error(f"Invalid JSON: {e}")

if not data:
    st.info("👆 Upload a JSON file to begin")
    st.stop()

schema_version = detect_schema_version(data)
company = resolve_company_name(data)

st.success(f"Loaded: {company} (Schema v{schema_version})")

r = data.get("report_info", {})
st.markdown(
    f"**{company}**  \n"
    f"{r.get('period_start','')} → {r.get('period_end','')}  \n"
    f"{r.get('total_months',0)} Months"
)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Integrity", f"{data.get('integrity_score',{}).get('score',0)}%")
c2.metric("Kite Risk", data.get("kite_flying",{}).get("risk_score",0))
c3.metric("Volatility", f"{data.get('volatility',{}).get('overall_index',0):.0f}%")
c4.metric("Accounts", len(data.get("accounts", [])))

st.markdown("---")

c1, c2 = st.columns(2)
with c1:
    st.download_button(
        "📄 Download JSON",
        json.dumps(data, indent=2),
        f"{company.replace(' ','_')}_analysis.json",
        "application/json"
    )

with c2:
    st.download_button(
        "🌐 Download HTML",
        generate_interactive_html(data),
        f"{company.replace(' ','_')}_analysis.html",
        "text/html"
    )
