# Dashboard Guide

How to use and understand the Student Performance Dashboard (Milestone 3) along with design references.

---

## 1. Overview

- **App:** `src/dash/app.py`
- **Framework:** Streamlit
- **Data sources:** DuckDB (`warehouse/student_performance.duckdb`) + Parquet files for fallbacks
- **Access URL:** http://localhost:8501

Launch command:

```bash
python -m streamlit run src/dash/app.py
```

---

## 2. Core Features

- **Overview KPIs:** Average score, attendance rate, cohort summaries
- **Interactive filters:** University type, subject, semester, date range
- **Visualizations:** Attendance heatmaps, trend lines, score distributions
- **Export buttons:** Download filtered CSV snapshots
- **Responsive layout:** Designed for desktop/laptop screens

---

## 3. Usage Flow

1. **Load dataset** – ensure the DuckDB database is built (see `docs/SETUP_GUIDE.md`).
2. **Start Streamlit** – run the command above; the page opens automatically.
3. **Set filters** – choose cohort, subject, or timeframe to focus on.
4. **Inspect details** – drill down into student-level views when available.
5. **Export results** – use download widgets for CSV summaries.

---

## 4. Wireframes & Design Principles

![Dashboard Wireframes](../assets/wireframes%20for%20the%20UIUX%20design.png)

Design priorities:
- Clarity and accessibility (color-blind friendly palette)
- Highlight actionable insights with badges and contextual descriptions
- Maintain consistent typography and spacing

Screens covered:
- **Overview Dashboard** – KPIs, quick filters, high-level charts
- **Student Profile** – timeline, attendance log, performance breakdown
- **Cohort Trend Analysis** – comparative charts and heatmaps

---

## 5. Milestone 3 Deliverables

| Deliverable | Status |
|-------------|--------|
| Visualization notebook updates | ✅ |
| Streamlit dashboard | ✅ |
| Attendance heatmaps (Plotly) | ✅ |
| Score trend charts | ✅ |
| Export functionality | ✅ |

Milestone 3 is complete; improvements now focus on documentation and polishing.

---

## 6. Troubleshooting

- **Blank dashboard?** Ensure Streamlit console shows no errors and DuckDB file exists.
- **Module import error?** Run the command from the repository root so relative imports resolve.
- **Port already in use?** Run `streamlit run src/dash/app.py --server.port 8502`.
- More fixes listed in `docs/TROUBLESHOOTING.md`.

---

## 7. Related Docs

- Setup guide: `docs/SETUP_GUIDE.md`
- SQL analytics details: `docs/SQL_ANALYTICS.md`
- Validation steps: `docs/VALIDATION.md`
- Development practices: `docs/DEVELOPMENT.md`


