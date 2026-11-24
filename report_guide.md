# ResistMap — report writing guide

Write the report in your own words. Replace prompts with observations from your final application run. Do not claim results the application has not produced.

## 1. Introduction
- Define antimicrobial resistance (AMR).
- Explain why resistance in bloodstream infections matters.
- Introduce the two indicators: third-generation-cephalosporin-resistant E. coli and MRSA.

## 2. Problem statement
- Public surveillance tables can be difficult for non-specialists to compare.
- Frame the problem as data access and interpretation, not clinical diagnosis.

## 3. Aim and objectives
- Build a Python-based web application for exploring AMR surveillance indicators.
- Load and combine two public datasets.
- Provide year and country filters.
- Visualise trends, country comparisons and country-level distributions.
- Allow filtered observations to be downloaded.

## 4. Dataset description
- Source: Our World in Data grapher; underlying surveillance source documented as WHO GLASS.
- E. coli download: 505 rows and 4 columns; observed years 2016–2022.
- MRSA download: 496 rows and 4 columns; observed years 2016–2022.
- Columns: Entity, Code, Year and the indicator percentage.
- Country coverage and years with observations vary.
- The denominator is tested patients seeking care whose blood sample was taken.

## 5. Methodology
- Read CSV data using Pandas.
- Identify the indicator column and rename it for analysis.
- Convert year and percentage fields to numeric types.
- Join on Entity, Code and Year.
- Preserve missing values; do not treat missing as zero.
- Use country-code rows for country-level charts.
- Generate charts with Plotly and the interface with Streamlit.

## 6. System design
- Input: two public CSV datasets.
- Processing: Pandas cleaning, type conversion and merging.
- Interface: Streamlit filters and three application tabs.
- Output: metrics, line chart, bar chart, choropleth, scatter plot and downloadable CSV.
- Add a flow diagram: CSV sources → Pandas processing → Streamlit dashboard → visualisations/download.

## 7. Implementation
- Describe app.py, requirements.txt and the data-loading function.
- Explain the year-range filter, country filter and indicator selector.
- Include screenshots of Overview, Country explorer and Data & methodology.

## 8. Results and discussion
- Record actual values displayed by your final application.
- Discuss India only after selecting India and verifying the displayed values.
- The two indicators measure different organisms/resistance phenotypes; do not treat them as interchangeable.
- Note countries/years with missing observations.
- A high percentage is not the same as a high absolute number of resistant infections.

## 9. Limitations
- Unequal country and year coverage.
- Differences in testing, sampling and reporting.
- Bloodstream-infection indicators are not representative of every infection.
- Country-level data cannot predict individual patient outcomes.
- The application is descriptive and does not recommend treatment.

## 10. Conclusion and future scope
- Summarise what the dashboard enables.
- Future additions: more organisms and antimicrobial classes, updated verified data, metadata and additional surveillance sources.

## 11. References
- Our World in Data, E. coli indicator: https://ourworldindata.org/grapher/share-of-e-coli-bloodstream-infections-due-to-antimicrobial-resistant-bacteria
- Our World in Data, MRSA indicator: https://ourworldindata.org/grapher/share-of-s-aureus-bloodstream-infections-that-are-resistant-to-antibiotics
- WHO GLASS: https://www.who.int/initiatives/glass

## 12. Appendix
- Application screenshots.
- Sample rows from both input datasets.
- Software requirements and run instructions.
