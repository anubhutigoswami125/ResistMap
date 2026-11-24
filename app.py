import pandas as pd
import plotly.express as px
import streamlit as st
from pathlib import Path

st.set_page_config(page_title="ResistMap | AMR Explorer", page_icon="🧫", layout="wide")

ECOLI_URL = "https://ourworldindata.org/grapher/share-of-e-coli-bloodstream-infections-due-to-antimicrobial-resistant-bacteria.csv?v=1&csvType=full&useColumnShortNames=false"
MRSA_URL = "https://ourworldindata.org/grapher/share-of-s-aureus-bloodstream-infections-that-are-resistant-to-antibiotics.csv?v=1&csvType=full&useColumnShortNames=false"
DATA_DIR = Path(__file__).parent / "data"

st.markdown("""
<style>
.block-container {padding-top: 2rem; padding-bottom: 3rem; max-width: 1450px;}
.hero {padding: 1.5rem 1.7rem; border-radius: 16px; background: linear-gradient(115deg,#102a43,#164e63); color: white; margin-bottom: 1rem;}
.hero h1 {font-size: 2.35rem; margin: 0 0 .35rem 0; color: white;}
.hero p {color: #d9e8f0; margin: 0; font-size: 1rem;}
div[data-testid="stMetric"] {background: #f4f7fa; border: 1px solid #e2e8f0; padding: .9rem 1rem; border-radius: 12px;}
</style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=3600, show_spinner="Loading surveillance datasets…")
def read_source(local_name, url):
    local_path = DATA_DIR / local_name
    return pd.read_csv(local_path if local_path.exists() else url)

@st.cache_data(ttl=3600, show_spinner="Preparing data…")
def load_data():
    ecoli_raw = read_source("share-of-e-coli-bloodstream-infections-due-to-antimicrobial-resistant-bacteria.csv", ECOLI_URL)
    mrsa_raw = read_source("share-of-s-aureus-bloodstream-infections-that-are-resistant-to-antibiotics.csv", MRSA_URL)
    ecoli_value = next(c for c in ecoli_raw.columns if c not in ["Entity", "Code", "Year"])
    mrsa_value = next(c for c in mrsa_raw.columns if c not in ["Entity", "Code", "Year"])
    ecoli = ecoli_raw[["Entity", "Code", "Year", ecoli_value]].rename(columns={ecoli_value: "E. coli"})
    mrsa = mrsa_raw[["Entity", "Code", "Year", mrsa_value]].rename(columns={mrsa_value: "MRSA"})
    for frame in (ecoli, mrsa):
        frame["Year"] = pd.to_numeric(frame["Year"], errors="coerce")
        frame["Code"] = frame["Code"].fillna("").astype(str)
        frame["Entity"] = frame["Entity"].astype(str)
    merged = ecoli.merge(mrsa, on=["Entity", "Code", "Year"], how="outer")
    merged = merged.dropna(subset=["Year"])
    merged["Year"] = merged["Year"].astype(int)
    merged["E. coli"] = pd.to_numeric(merged["E. coli"], errors="coerce")
    merged["MRSA"] = pd.to_numeric(merged["MRSA"], errors="coerce")
    return merged.sort_values(["Entity", "Year"]), len(ecoli_raw), len(mrsa_raw)

st.markdown("""
<div class="hero">
<h1>ResistMap</h1>
<p>Explore country-level antimicrobial-resistance surveillance indicators for bloodstream infections.</p>
</div>
""", unsafe_allow_html=True)

try:
    data, ecoli_rows, mrsa_rows = load_data()
except Exception as exc:
    st.error("The surveillance data could not be loaded. Check your internet connection or put both original CSV files in the data/ folder.")
    st.exception(exc)
    st.stop()

st.sidebar.header("Explore the data")
years = sorted(data["Year"].dropna().unique().tolist())
year_range = st.sidebar.slider("Year range", int(min(years)), int(max(years)), (int(min(years)), int(max(years))))
countries = sorted(data.loc[data["Code"].str.len() == 3, "Entity"].dropna().unique().tolist())
selected = st.sidebar.multiselect("Countries (leave empty for all)", countries, default=["India"] if "India" in countries else [])
metric = st.sidebar.radio("Indicator", ["E. coli", "MRSA"], horizontal=True)

view = data[data["Year"].between(year_range[0], year_range[1])].copy()
if selected:
    view = view[view["Entity"].isin(selected)]
country_year = view[view["Code"].str.len() == 3].copy()
values = country_year[metric].dropna()

a, b, c, d = st.columns(4)
a.metric("Countries in selection", f"{country_year['Entity'].nunique():,}")
b.metric("Year range", f"{year_range[0]}–{year_range[1]}")
c.metric(f"Mean {metric} indicator", f"{values.mean():.1f}%" if not values.empty else "—")
d.metric("Observations", f"{len(values):,}")
st.caption("Percentages refer to the specified resistant bloodstream-infection indicator among patients seeking care whose blood sample was taken and tested. They are not population-wide infection rates.")

overview, explorer, methods = st.tabs(["Overview", "Country explorer", "Data & methodology"])
with overview:
    left, right = st.columns([1.15, 1])
    with left:
        st.subheader(f"{metric} indicator over time")
        trend = country_year.groupby("Year", as_index=False)[metric].mean()
        if not trend.empty:
            fig = px.line(trend, x="Year", y=metric, markers=True, labels={metric: "Mean reported indicator (%)"}, title="Mean across available country observations")
            fig.update_layout(height=350, margin=dict(l=10, r=10, t=55, b=10))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No observations match these filters.")
    with right:
        st.subheader(f"Highest reported {metric} values")
        latest_year = int(country_year["Year"].max()) if not country_year.empty else None
        latest = country_year[country_year["Year"] == latest_year].dropna(subset=[metric]) if latest_year else pd.DataFrame()
        latest = latest.nlargest(10, metric)
        if not latest.empty:
            fig = px.bar(latest.sort_values(metric), x=metric, y="Entity", orientation="h", labels={metric: "Indicator (%)", "Entity": "Country"}, title=f"Top observations in {latest_year}")
            fig.update_layout(height=350, margin=dict(l=10, r=10, t=55, b=10))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No country observations are available.")
    st.subheader("Country-level map")
    map_data = country_year.dropna(subset=[metric]).copy()
    if not map_data.empty:
        map_year = st.select_slider("Map year", options=sorted(map_data["Year"].unique()), value=int(map_data["Year"].max()))
        map_frame = map_data[map_data["Year"] == map_year]
        fig = px.choropleth(map_frame, locations="Code", color=metric, hover_name="Entity", color_continuous_scale="YlOrRd", range_color=(0, 100), labels={metric: "Indicator (%)"}, title=f"{metric} indicator by country — {map_year}")
        fig.update_layout(height=450, margin=dict(l=0, r=0, t=55, b=0))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No map observations are available.")

with explorer:
    st.subheader("Compare the two indicators")
    paired = country_year.dropna(subset=["E. coli", "MRSA"])
    if not paired.empty:
        fig = px.scatter(paired, x="E. coli", y="MRSA", color="Year", hover_name="Entity", hover_data={"Code": True}, labels={"E. coli": "E. coli indicator (%)", "MRSA": "MRSA indicator (%)"}, title="E. coli and MRSA values in the same country-year")
        fig.update_layout(height=420)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No country-year rows contain both indicators under these filters.")
    st.subheader("Underlying observations")
    display = country_year[["Entity", "Code", "Year", "E. coli", "MRSA"]].sort_values(["Entity", "Year"])
    st.dataframe(display, use_container_width=True, hide_index=True)
    st.download_button("Download filtered observations (CSV)", display.to_csv(index=False).encode("utf-8"), file_name="resistmap_filtered_observations.csv", mime="text/csv")

with methods:
    st.subheader("Dataset and indicator definitions")
    st.markdown("""
**E. coli:** Percentage of bloodstream infections due to *Escherichia coli* resistant to third-generation cephalosporins (for example, ESBL-producing *E. coli*) among patients seeking care whose blood sample was taken and tested.

**MRSA:** Percentage of bloodstream infections due to methicillin-resistant *Staphylococcus aureus* among patients seeking care whose blood sample was taken and tested.

The data are country-year surveillance observations. The dashboard does not estimate individual risk, diagnose infection or recommend antibiotic treatment.
""")
    st.markdown("**Data sources**")
    st.write("E. coli: https://ourworldindata.org/grapher/share-of-e-coli-bloodstream-infections-due-to-antimicrobial-resistant-bacteria")
    st.write("MRSA: https://ourworldindata.org/grapher/share-of-s-aureus-bloodstream-infections-that-are-resistant-to-antibiotics")
    st.write("Underlying surveillance source: WHO GLASS, as documented by Our World in Data.")
    st.markdown("**Data handling**")
    st.write(f"Loaded {ecoli_rows:,} E. coli rows and {mrsa_rows:,} MRSA rows. The indicators are joined by entity, code and year. Missing values remain missing and are not converted to zero.")
    st.markdown("**Limitations**")
    st.write("- Country and year coverage varies; differences may reflect surveillance and testing practices as well as resistance.")
    st.write("- These indicators describe tested bloodstream-infection samples, not all infections or the general population.")
    st.write("- The dashboard is descriptive and does not establish causation or support individual clinical decisions.")

st.divider()
st.caption("ResistMap · Educational data exploration project · Not a clinical decision-support system")
