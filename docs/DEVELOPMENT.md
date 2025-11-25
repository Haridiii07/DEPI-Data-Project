# Development Guide

Practices for contributors: repository layout, coding standards, testing, and workflow expectations.

---

## 1. Repository Structure (Quick Reference)

```
Data Project/
├── data/                   # Parquet + sample datasets (large files ignored via .gitignore)
├── scripts/                # Python scripts & notebooks
├── dashboard/              # Streamlit app + prototypes
├── docs/                   # All documentation (this folder)
├── assets/                 # ERD, wireframes, timeline images
├── output/                 # Generated analytics (CSV)
├── warehouse/              # DuckDB database location
└── README.md
```

See `README.md` for a simplified tree and `docs/PROJECT_STRUCTURE.md` (future) for deep dives.

---

## 2. Scripts Catalogue

| Script | Purpose |
|--------|---------|
| `scripts/real_data_milestone1.py` | Generate raw batch CSVs from IPEDS inputs |
| `scripts/clean_students_batches.py` | Clean each 100K batch, normalize fields |
| `scripts/create_sample_dataset.py` | Build 100K sample across batches |
| `scripts/verify_sample.py` | Validate sample statistics |
| `scripts/convert_to_parquet.py` | Convert all CSV batches to Parquet |
| `scripts/assemble_dataset.py` | Assemble batches → full dataset + optional sample |
| `scripts/build_database.py` | Create DuckDB star schema tables |
| `scripts/Milestone2_3_SQL_and_Visualizations.ipynb` | Combined SQL + visualization notebook |

---

## 3. Coding Standards

- Follow PEP 8 (enforced via `.flake8`)
- Use type hints for new Python functions
- Prefer pathlib/forward slashes for paths
- Document scripts with module docstrings and CLI usage examples
- Keep notebooks clean: restart kernel, run all cells before committing

---

## 4. Git Workflow

1. Create a feature branch (`git checkout -b docs/cleanup-readme`)
2. Make changes + run relevant tests or lint checks
3. Stage only necessary files (`git add path/to/file`)
4. Craft descriptive commit messages (“docs: add setup guide”)
5. Open PR referencing milestone/task IDs

Large data artifacts should not be committed unless specifically approved (sample Parquet is the exception).

---

## 5. Testing & Validation

- Run automated tests:

```bash
pytest
```

- Verify data integrity using commands in `docs/VALIDATION.md`
- For documentation-only PRs, preview Markdown in VS Code or GitHub web UI

---

## 6. Repository Hygiene

- `.gitignore` excludes large CSVs, DuckDB files, and OS cruft
- Commit Parquet files only when small (e.g., sample datasets)
- Keep `requirements.txt` synchronized with actual dependencies; use `pip freeze --exclude-editable` sparingly
- Maintain `docs/CHANGELOG.md` with notable updates

---

## 7. Contribution Expectations

- **Code changes:** include doc updates when behavior changes
- **Docs:** cross-link new files; keep README concise
- **Issues/PRs:** describe reproduction steps, include screenshots for UI tweaks
- **Reviews:** prioritize data correctness, performance, and UX clarity

---

## 8. Contacts

- Maintainers: Group 4 (DEPI Project)
- Primary email: listed in proposal PDF (`docs/Proposal_ Student Performance Dashboard.md`)

---

## 9. Related References

- Setup instructions: `docs/SETUP_GUIDE.md`
- Troubleshooting: `docs/TROUBLESHOOTING.md`
- Validation: `docs/VALIDATION.md`
- Changelog: `docs/CHANGELOG.md`


