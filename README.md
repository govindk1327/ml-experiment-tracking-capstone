# ML Experiment Tracking & Evaluation Toolkit - Capstone Project

## 🎯 Project Overview

You are an ML Engineer at a fast-growing tech company, tasked with finalizing a fraud detection model. Your mission is to run three experiments, track them with W&B, select the best model, and version everything with Git and DVC to ensure complete reproducibility.

## 📋 Prerequisites

Before starting, ensure you have:
- Python 3.8 or higher
- Git installed
- A W&B account (free at https://wandb.ai)
- DVC installed (`pip install dvc`)

## 🚀 Setup Instructions

### Step 1: Clone and Setup

```bash
# Clone this repository (your instructor will provide the URL)
git clone <repository-url>
cd fraud-detection-capstone

# Install dependencies
pip install -r requirements.txt

# Login to W&B
wandb login
# Paste your API key from https://wandb.ai/settings

# Initialize DVC
dvc init
```

### Step 2: Version the Dataset with DVC

```bash
# Add the dataset to DVC tracking
dvc add fraud_transactions.csv

# Commit the .dvc file to Git
git add fraud_transactions.csv.dvc .gitignore
git commit -m "Add dataset to DVC tracking"
```

## 🧪 Running the Three Experiments

You will train the same fraud detection model **three times**, changing only the `learning_rate` parameter. This simulates a real hyperparameter tuning process.

### Experiment 1: Low Learning Rate

```bash
python train.py --learning_rate 0.01 --experiment_name "experiment_1_low_lr"
```

**Expected behavior**: Slower learning, potentially underfitting, but very stable.

### Experiment 2: Medium Learning Rate (Baseline)

```bash
python train.py --learning_rate 0.1 --experiment_name "experiment_2_medium_lr"
```

**Expected behavior**: Balanced learning, likely good performance.

### Experiment 3: High Learning Rate

```bash
python train.py --learning_rate 0.5 --experiment_name "experiment_3_high_lr"
```

**Expected behavior**: Faster learning, potentially better F1 but may overfit or be unstable.

### 📊 What Gets Tracked

Each run automatically logs to W&B:

**Predictive Metrics:**
- Test F1 Score (primary metric for model quality)
- Test Accuracy
- Precision
- Recall

**Operational Metrics:**
- Inference Latency (average, in milliseconds)
- Inference Latency P95
- Training Time

## 🔍 Analysis and Model Selection

### Step 3: Compare Experiments in W&B

1. Go to https://wandb.ai and open your `fraud-detection-capstone` project
2. View the **Table** tab to see all three runs side-by-side
3. Look at the columns:
   - `learning_rate` (the hyperparameter you changed)
   - `test_f1` (predictive metric - **higher is better**)
   - `inference_latency_ms` (operational metric - **lower is better**)

### Step 4: Evaluate Trade-offs

You will likely see a **trade-off**:
- Higher learning rates → Better F1 scores but potentially higher latency or less stability
- Lower learning rates → More stable but potentially lower F1 scores

**Your job**: Select the model that offers the **best balance** for production deployment.

### Step 5: Tag Your Selected Model

Once you've decided which experiment is best:

1. In W&B, click on your chosen run
2. Click the "Edit" button (pencil icon)
3. Add a tag: `production-candidate`
4. Save

## 📦 Versioning the Selected Model

### Step 6: Version Model with DVC

After selecting your best model (e.g., `experiment_2_medium_lr`):

```bash
# Add the selected model to DVC tracking
dvc add models/experiment_2_medium_lr_model.pkl
dvc add models/experiment_2_medium_lr_scaler.pkl

# Commit the .dvc files
git add models/*.dvc .gitignore
git commit -m "Add production candidate model to DVC"
```

### Step 7: Commit Final Code

```bash
# Make sure all code changes are committed
git add train.py
git commit -m "Final model training code for production candidate"

# Get your final commit hash (you'll need this for the report)
git log -1 --format="%H"
```

### Step 8: Get DVC Status

```bash
# Get DVC status (you'll need this for the report)
dvc status
```

This should show "Data and pipelines are up to date."

## 📄 Submission Requirements

Create a **single PDF document** with three sections:

### Part 1: Reproducibility and Data Lineage

**Include:**
1. **Git Commit Hash**: The full hash from `git log -1 --format="%H"`
2. **DVC Hash**: Output from `dvc status`
3. **Rationale** (1 sentence): Explain how these two hashes together guarantee reproducibility

**Example:**
> "The Git commit hash ensures the exact training code is preserved, while the DVC hash locks the dataset version, together allowing any teammate to recreate the model identically."

### Part 2: Experiment Tracking and Comparison

**Include:**
1. **W&B Screenshot**: Table view showing all three experiments with columns:
   - Run name
   - `learning_rate`
   - `test_f1`
   - `inference_latency_ms`
2. **Production Tag**: State the exact tag you applied (e.g., "production-candidate")

**How to take screenshot:**
- Go to W&B project → Table tab
- Make sure all required columns are visible
- Take a clear screenshot

### Part 3: Model Evaluation and Selection Justification

**Include:**
1. **Selected Model**: Name of the run (e.g., "experiment_2_medium_lr")
2. **Trade-off Justification** (3-5 sentences): 
   - State the F1 score and latency of your chosen model
   - Compare with at least one other experiment
   - Explain why you chose this balance
   - Consider the business context (fraud detection needs both accuracy AND speed)

**Example structure:**
> "I selected experiment_2_medium_lr (learning_rate=0.1) which achieved an F1 score of 0.78 with 12ms latency. While experiment_3_high_lr had a slightly better F1 of 0.80, its 25ms latency makes it unsuitable for real-time fraud detection where sub-20ms response is critical. Experiment_1_low_lr was fast (8ms) but its F1 of 0.72 would miss too many fraudulent transactions. The medium learning rate offers the best balance of detection quality and operational feasibility."

## ✅ Submission Checklist

Before submitting, verify:

- [ ] All three experiments completed successfully
- [ ] All runs visible in W&B with correct names
- [ ] Production candidate tagged in W&B
- [ ] Dataset tracked with DVC (`fraud_transactions.csv.dvc` exists)
- [ ] Selected model tracked with DVC (`.dvc` files for model and scaler)
- [ ] Final code committed to Git
- [ ] Git commit hash obtained
- [ ] DVC status checked
- [ ] PDF report created with all three sections
- [ ] Screenshot clearly shows all required columns
- [ ] Justification paragraph addresses trade-offs explicitly

## 🆘 Troubleshooting

### "wandb: ERROR - API key not configured"
**Solution**: Run `wandb login` and paste your API key from https://wandb.ai/settings

### "ModuleNotFoundError: No module named 'wandb'"
**Solution**: Run `pip install -r requirements.txt`

### "FileNotFoundError: fraud_transactions.csv"
**Solution**: Make sure you're in the project directory. The CSV should be in the root folder.

### "dvc: command not found"
**Solution**: Install DVC with `pip install dvc`

### Model training is very slow
**Solution**: This is normal for the first epoch. The model will speed up. Total training should take 30-60 seconds per experiment.

### Can't see all columns in W&B table
**Solution**: Click the "eye" icon in the table to show/hide columns. Make sure `learning_rate`, `test_f1`, and `inference_latency_ms` are visible.

## 📚 Additional Resources

- W&B Documentation: https://docs.wandb.ai
- DVC Documentation: https://dvc.org/doc
- Git Documentation: https://git-scm.com/doc

## 💡 Tips for Success

1. **Run experiments in order** - Don't skip experiment_1 or experiment_2
2. **Wait for completion** - Each experiment takes ~1 minute, let it finish before starting the next
3. **Check W&B immediately** - Verify each run appears in your dashboard
4. **Take notes** - Record F1 scores and latencies as you go
5. **Think about business context** - Fraud detection needs BOTH accuracy and speed
6. **Be specific in justification** - Use exact numbers from your experiments
7. **Proofread your report** - Grammar and clarity matter

## 🎓 Learning Objectives

By completing this project, you will demonstrate:
- ✅ Running and tracking ML experiments systematically
- ✅ Analyzing trade-offs between predictive and operational metrics
- ✅ Making data-driven model selection decisions
- ✅ Versioning datasets and models with DVC
- ✅ Maintaining code history with Git
- ✅ Creating comprehensive, professional technical reports

Good luck! 🚀
