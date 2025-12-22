# DVC Setup Guide for Capstone Project

## What is DVC?

DVC (Data Version Control) is like Git, but for data and model files. It lets you:
- Version large datasets without storing them in Git
- Track model artifacts
- Ensure reproducibility
- Collaborate on ML projects

## Initial Setup (Instructor/Setup Phase)

If you're preparing the project for distribution:

```bash
cd capstone-project

# Initialize DVC (only once)
dvc init

# This creates:
# - .dvc/config (DVC settings)
# - .dvcignore (what DVC ignores)
```

## Student Workflow

### Step 1: Verify DVC is Initialized

```bash
# Check if .dvc directory exists
ls -la .dvc

# Should see:
# .dvc/
# .dvc/config
# .dvcignore
```

If not initialized, run:
```bash
dvc init
```

### Step 2: Track the Dataset

```bash
# Add dataset to DVC tracking
dvc add fraud_transactions.csv

# This creates:
# - fraud_transactions.csv.dvc (metadata file - COMMIT THIS)
# - Adds fraud_transactions.csv to .gitignore

# Commit the .dvc file to Git
git add fraud_transactions.csv.dvc .gitignore
git commit -m "Add dataset to DVC tracking"
```

### Step 3: Track Model Artifacts

After running experiments and selecting your production model:

```bash
# Example: tracking experiment_2_medium_lr model
dvc add models/experiment_2_medium_lr_model.pkl
dvc add models/experiment_2_medium_lr_scaler.pkl

# This creates:
# - models/experiment_2_medium_lr_model.pkl.dvc
# - models/experiment_2_medium_lr_scaler.pkl.dvc

# Commit these .dvc files
git add models/*.dvc .gitignore
git commit -m "Add production candidate model to DVC"
```

### Step 4: Check DVC Status

```bash
# Check if everything is tracked
dvc status

# Expected output if everything is up to date:
# Data and pipelines are up to date.
```

## What Gets Tracked Where?

### Git Tracks (Small Files):
- ✅ `.dvc` files (metadata)
- ✅ Python code (`.py` files)
- ✅ README, documentation
- ✅ `.gitignore`
- ✅ `requirements.txt`

### DVC Tracks (Large Files):
- ✅ `fraud_transactions.csv` (dataset)
- ✅ `*.pkl` files (models and scalers)
- ✅ Any other large data files

### Neither Tracks (Gitignored):
- ❌ `wandb/` (W&B local cache)
- ❌ `__pycache__/` (Python cache)
- ❌ `.DS_Store` (Mac system files)

## Understanding .dvc Files

When you run `dvc add fraud_transactions.csv`, it creates `fraud_transactions.csv.dvc`:

```yaml
outs:
- md5: 1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p
  size: 1234567
  path: fraud_transactions.csv
```

This file contains:
- **md5**: Hash of the data (like a fingerprint)
- **size**: File size in bytes
- **path**: Location of the file

## For Your Report

### Getting the DVC Hash:

```bash
# Option 1: Check status
dvc status

# Option 2: View the .dvc file
cat fraud_transactions.csv.dvc

# Option 3: List all tracked files
dvc list . --dvc-only
```

Copy the entire output for your report.

## Common DVC Commands

```bash
# Check what's tracked
dvc status

# Add a file to tracking
dvc add <filename>

# Remove a file from tracking (but keep the file)
dvc remove <filename>.dvc

# Get file info
dvc get-url <filename>
```

## Troubleshooting

### "dvc: command not found"
```bash
pip install dvc
```

### "DVC not initialized"
```bash
dvc init
```

### "File not tracked"
```bash
# Make sure you ran dvc add
dvc add fraud_transactions.csv
git add fraud_transactions.csv.dvc
```

### "Changes not detected"
```bash
# Force recompute hash
dvc add --force fraud_transactions.csv
```

## Why This Matters for Reproducibility

**Scenario:** Your teammate wants to reproduce your model

**Without DVC:**
- "Which dataset version did you use?"
- "I think it was the one from last Tuesday?"
- "My results are different..."

**With DVC:**
```bash
# They check your Git commit
git checkout a1b2c3d4...

# DVC automatically knows which data version
dvc checkout

# Exact reproduction guaranteed!
```

## Advanced (Optional)

### Remote Storage

In production, you'd store data on cloud storage:

```bash
# Configure remote (e.g., S3, GCS, Azure)
dvc remote add -d myremote s3://mybucket/dvcstore

# Push data to remote
dvc push

# Others can pull
dvc pull
```

For this capstone, local storage is sufficient.

---

**Key Takeaway:** DVC + Git = Complete Reproducibility
- Git tracks code and configuration
- DVC tracks data and models
- Together = Anyone can recreate your exact results
