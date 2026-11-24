# ResistMap

A Python-based interactive explorer for antimicrobial-resistance surveillance indicators.

ResistMap presents two country-level bloodstream-infection indicators:
- Third-generation-cephalosporin-resistant Escherichia coli.
- Methicillin-resistant Staphylococcus aureus (MRSA).

Features include year and country filters, indicator selection, trend and ranked-country charts, a choropleth map, paired-indicator scatter plot, observation table and CSV export.

## Run locally

1. Install Python 3.10 or later.
2. Clone or download this repository.
3. Open a terminal in the project folder.
4. Install dependencies with: python -m pip install -r requirements.txt
5. Start the app with: python -m streamlit run app.py

The app downloads public CSV data from Our World in Data on first load and caches it for one hour. An internet connection is required. For offline use, place the two original CSV files in a folder named data beside app.py, retaining their original filenames.

## Data sources and interpretation

- E. coli indicator: https://ourworldindata.org/grapher/share-of-e-coli-bloodstream-infections-due-to-antimicrobial-resistant-bacteria
- MRSA indicator: https://ourworldindata.org/grapher/share-of-s-aureus-bloodstream-infections-that-are-resistant-to-antibiotics
- Underlying surveillance source: WHO GLASS, as documented by Our World in Data.

The percentages refer to the specified resistant bloodstream-infection indicator among patients seeking care whose blood sample was taken and tested. They are not population-wide prevalence estimates and must not be used for individual treatment decisions. Country coverage and testing practices may differ.

## Project files

- app.py — Streamlit application and data-processing pipeline.
- requirements.txt — Python dependencies.
- report_guide.md — report headings and factual prompts.

ResistMap is a descriptive educational data-exploration application. It does not diagnose infection, predict individual risk, establish causation or recommend antibiotic treatment.
