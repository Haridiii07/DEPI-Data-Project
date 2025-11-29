# 🚀 Deployment Guide

## Live Deployment

**Production URL:** https://depi-data-project-sxczyh8wks5x4bdwjznwgw.streamlit.app/

The app is deployed on **Streamlit Cloud** (free tier) and automatically redeploys on every push to the `main` branch.

---

## Cloud vs Local Differences

| Feature | Cloud (Streamlit) | Local Development |
|---------|------------------|-------------------|
| **Students** | 10,000 random | 1,000,000 full dataset |
| **Data Size** | 0.78 MB | ~72 MB |
| **Load Time** | ~5-10 seconds | ~30-60 seconds |
| **Search Range** | Student #1-10,000 | All 1M students |
| **Memory** | Optimized for free tier | No limits |

---

## Cloud Deployment Strategy

### 1. Data Optimization

We use a **10K student sample** (`sample_50K_students.parquet`) for cloud deployment:

```python
# Created with create_10k_students.py
- 10,000 random students
- All their course records (~100K rows)
- Student numbers 1-10,000 for easy search
- Only 0.78 MB file size
```

### 2. Smart Data Detection

The app automatically detects which environment it's running in:

```python
# In app.py
sample_50k = base_dir / 'data' / 'sample_50K_students.parquet'
if sample_50k.exists():
    # Cloud deployment - use 10K sample
else:
    # Local development - use full 1M dataset
```

### 3. Star Schema Generation

Star schema files are generated on first load (not stored in Git):
- `fact_student_performance.parquet`
- `dim_student.parquet` (includes `student_number` column)
- `dim_university.parquet`
- `dim_course.parquet`
- `dim_date.parquet`

---

## Local Setup for Full Dataset

### Step 1: Clone Repository
```bash
git clone https://github.com/Haridiii07/DEPI-Data-Project.git
cd DEPI-Data-Project
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Prepare Data
The full dataset is split into parts for Git:
```bash
# Parts are automatically stitched on first run
# Or manually combine:
cat data/cleaned_students.parquet.part* > data/cleaned_students.parquet
```

### Step 4: Run App
```bash
streamlit run src/dash/app.py
```

---

## Data Split Strategy

Due to GitHub file size limits (100 MB), we split the 72 MB dataset:

- `cleaned_students.parquet.part1` (35 MB) ✅ In Git
- `cleaned_students.parquet.part2` (37 MB) ✅ In Git  
- `cleaned_students.parquet` (72 MB) ❌ Not in Git (stitched locally)

---

## CI/CD Pipeline

The GitHub Actions workflow (`streamlit_deploy.yml`) runs on every push:

1. **Install dependencies** from `requirements.txt`
2. **Upload sample data** (`sample_50K_students.parquet`)
3. **Deploy to Streamlit Cloud**
4. **Generate star schema** on first load

---

## Memory Optimization

Streamlit Cloud free tier has memory limits. Our optimizations:

✅ **10K sample instead of 1M** - 100x smaller  
✅ **Parquet columnar format** - Efficient compression  
✅ **Star schema on-demand** - Generated once, cached  
✅ **DuckDB views not tables** - Lower memory footprint  
✅ **Silent data loading** - No verbose messages

---

## Troubleshooting Cloud Issues

### TypeError: Failed to fetch
**Cause:** Browser cache issue  
**Fix:** Clear cache or hard refresh (Ctrl+Shift+R)

### Memory Limit Exceeded
**Cause:** Sample too large  
**Fix:** Reduce sample size in `create_10k_students.py`

### Student Number Not Found
**Cause:** Old star schema without `student_number` column  
**Fix:** App auto-detects and regenerates schema

### Slow Loading
**Cause:** Star schema regeneration on first load  
**Fix:** Normal - subsequent loads are fast (<5s)

---

## Deployment Checklist

Before deploying:
- [ ] Run local tests: `pytest`
- [ ] Test with 10K sample locally
- [ ] Verify student search works (1-10,000)
- [ ] Check all tabs load correctly
- [ ] Update CHANGELOG.md
- [ ] Push to main branch

---

## Links

- **Live App:** https://depi-data-project-sxczyh8wks5x4bdwjznwgw.streamlit.app/
- **GitHub:** https://github.com/Haridiii07/DEPI-Data-Project
- **Streamlit Cloud:** https://streamlit.io/cloud
