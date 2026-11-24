# ResistMap

**An interactive web application for exploring antimicrobial-resistance (AMR) surveillance indicators.**

ResistMap presents country-level bloodstream-infection resistance indicators in an accessible visual explorer. Select an indicator, follow annual observations, compare countries, and search the underlying records.

## Explore the live application

https://anubhutigoswami125.github.io/ResistMap/

## Indicators

- **ESBL E. coli:** bloodstream infection isolates resistant to third-generation cephalosporins.
- **MRSA:** bloodstream infection isolates resistant to methicillin.

## Features

- Switch between the two resistance indicators.
- Filter observations by year and country.
- View a country-level annual trend.
- Compare the latest available country observations.
- Search and browse the source observations.

## Data and interpretation

The datasets are curated by Our World in Data from the WHO Global Antimicrobial Resistance and Use Surveillance System (GLASS).

- [E. coli indicator dataset](https://ourworldindata.org/grapher/share-of-e-coli-bloodstream-infections-due-to-antimicrobial-resistant-bacteria)
- [MRSA indicator dataset](https://ourworldindata.org/grapher/share-of-s-aureus-bloodstream-infections-that-are-resistant-to-antibiotics)

The percentages refer to the specified resistant bloodstream-infection indicator among patients seeking care whose blood sample was taken and tested. They are **not population-wide prevalence estimates**. Country coverage and testing practices may differ. ResistMap is an educational data-exploration tool, not a clinical decision system; it does not diagnose infection or recommend treatment.

## Technology

Built with HTML, CSS, and vanilla JavaScript. The application reads the included CSV files directly in the browser; no server or Python runtime is required.

## Run locally

Open `index.html` in a local static web server, or use GitHub Pages.

## Deployment

GitHub Actions publishes the repository root to GitHub Pages whenever changes are pushed to the `main` branch. The workflow is defined in `.github/workflows/pages.yml`.
