# ♻️ EAF Slag Utilization Decision Tool — (EU/Germany-focused)

A rule-based Streamlit app (no dataset required) to rank recycling/valorization routes for EAF slag using:
- Metallurgical suitability inputs
- EU/Germany-style environmental screening flags (Green/Amber/Red)

> **Note:** This is a screening/decision-support tool. For real compliance decisions, use appropriate leaching tests and the legally applicable German/EU rules and guidance.

---

## Inputs

### Metallurgical inputs
- FeO (%)
- Basicity (CaO/SiO₂)
- Free CaO expansion risk (Low/Medium/High)

### Trace metals (total content)
- Chromium (Cr) total (wt%)
- Lead (Pb) total (mg/kg)
- Zinc (Zn) total (wt%)

### Locally Available Facilities
- Cement / binder outlet
- Road construction / aggregates outlet
- Metal recovery facility
- Landfill option (fallback)

### EU/Germany screening thresholds
- Green & Amber threshold breakpoints for Cr, Pb, Zn
- Values above Amber are treated as Red
- Defaults are **illustrative placeholders**; you should enter thresholds from your chosen German reference

---

## Outputs
- EU-style screening summary: Cr/Pb/Zn flags + overall risk
- Ranked routes:
  - Road construction / aggregates (recycling route)
  - Cement / binder use (often encapsulation route)
  - Metal recovery first (beneficiation), then choose final outlet
  - Landfill / disposal (fallback)
- Required actions checklist (aging/conditioning, QA testing, leaching tests)

---

## Run locally

streamlit run app.py
