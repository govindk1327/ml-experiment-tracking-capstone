# Capstone Project Report Template
## ML Experiment Tracking & Evaluation Toolkit

**Student Name:** [Your Name]
**Date:** [Date]
**Project:** Fraud Detection Model Selection

---

## Part 1: Reproducibility and Data Lineage

### Git Commit Hash
```
[Paste your full Git commit hash here - get it with: git log -1 --format="%H"]

Example: a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0
```

### DVC Hash
```
[Paste the output of: dvc status]

Example:
Data and pipelines are up to date.
```

### Rationale (1 sentence)
[Explain how these two hashes together guarantee reproducibility]

**Example:**
"The Git commit hash preserves the exact training code and configuration, while the DVC hash locks the dataset and model artifacts to specific versions, ensuring that any team member can reproduce the exact model training process and results."

---

## Part 2: Experiment Tracking and Comparison

### W&B Run Summary Screenshot
[Insert screenshot here showing W&B table with three runs]

**Screenshot must clearly show:**
- ✓ Run names (experiment_1, experiment_2, experiment_3)
- ✓ learning_rate column
- ✓ test_f1 column
- ✓ inference_latency_ms column

### Production Tag
**Tag applied:** `production-candidate`

**Applied to run:** [experiment_X_xxx_lr]

---

## Part 3: Model Evaluation and Selection Justification

### Selected Model
**Run name:** [experiment_X_xxx_lr]

**Key metrics:**
- Test F1 Score: [X.XXXX]
- Inference Latency: [XX.XX] ms
- Learning Rate: [X.XX]

### Trade-off Justification (3-5 sentences)

[Write your justification here. Follow this structure:]

1. State your selected model and its key metrics
2. Compare with at least one other experiment
3. Explain the trade-off you observed
4. Justify why your choice is best for production
5. Consider the business context (fraud detection needs accuracy AND speed)

**Example:**

"I selected experiment_2_medium_lr (learning_rate=0.1) which achieved a test F1 score of 0.286 with an inference latency of 17.9ms. While experiment_3_high_lr achieved a slightly better F1 of 0.313, its higher latency of 19.4ms and potential instability from the aggressive learning rate make it less suitable for production. Experiment_1_low_lr had the best latency at 17.4ms but its significantly lower F1 of 0.185 would result in missing too many fraudulent transactions. In the context of real-time fraud detection, where both accuracy and sub-20ms response times are critical, the medium learning rate model offers the optimal balance between detection capability and operational performance."

---

## Appendix: Experiment Results Summary

| Experiment | Learning Rate | Test F1 | Latency (ms) | Decision |
|------------|---------------|---------|--------------|----------|
| experiment_1 | 0.01 | [X.XXX] | [XX.X] | Not selected - Low F1 |
| experiment_2 | 0.1  | [X.XXX] | [XX.X] | **SELECTED** ✓ |
| experiment_3 | 0.5  | [X.XXX] | [XX.X] | Not selected - High latency |

---

## Grading Rubric Reference

### Part 1 (30 points)
- ✓ Git commit hash provided (10 pts)
- ✓ DVC status provided (10 pts)
- ✓ Clear rationale sentence (10 pts)

### Part 2 (30 points)
- ✓ Screenshot includes all required columns (15 pts)
- ✓ Screenshot shows all three runs (10 pts)
- ✓ Production tag clearly stated (5 pts)

### Part 3 (40 points)
- ✓ Selected model clearly identified (10 pts)
- ✓ Justification addresses trade-offs explicitly (15 pts)
- ✓ Comparison with other experiments (10 pts)
- ✓ Business context considered (5 pts)

**Total: 100 points**

---

**Submission Checklist:**
- [ ] All three sections completed
- [ ] Screenshot is clear and readable
- [ ] Git and DVC hashes are correct
- [ ] Justification is 3-5 sentences
- [ ] No spelling/grammar errors
- [ ] Saved as PDF
