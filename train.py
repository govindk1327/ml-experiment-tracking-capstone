"""
Fraud Detection Model Training Script
Capstone Project - ML Experiment Tracking & Evaluation

This script trains a fraud detection model and tracks experiments with W&B.

Usage:
    python train.py --learning_rate 0.001 --experiment_name "experiment_1"
"""
import argparse
import time
import pickle
import pandas as pd
import numpy as np
import wandb
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import f1_score, precision_score, recall_score, accuracy_score

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Train fraud detection model')
    parser.add_argument('--learning_rate', type=float, default=0.1,
                        help='Learning rate for gradient boosting (default: 0.1)')
    parser.add_argument('--experiment_name', type=str, required=True,
                        help='Name for this experiment run')
    parser.add_argument('--n_estimators', type=int, default=100,
                        help='Number of boosting stages (default: 100)')
    parser.add_argument('--max_depth', type=int, default=5,
                        help='Maximum depth of trees (default: 5)')
    return parser.parse_args()

def load_data():
    """Load and prepare the fraud detection dataset"""
    print("\n[1/5] Loading data...")
    df = pd.read_csv('fraud_transactions.csv')
    
    # Separate features and target
    X = df.drop('is_fraud', axis=1)
    y = df['is_fraud']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    print(f"  ✓ Train samples: {len(X_train)}")
    print(f"  ✓ Test samples: {len(X_test)}")
    print(f"  ✓ Fraud rate: {100*y_train.mean():.2f}%")
    
    return X_train_scaled, X_test_scaled, y_train, y_test, scaler

def train_model(X_train, y_train, learning_rate, n_estimators, max_depth):
    """Train the fraud detection model"""
    print("\n[2/5] Training model...")
    
    model = GradientBoostingClassifier(
        learning_rate=learning_rate,
        n_estimators=n_estimators,
        max_depth=max_depth,
        random_state=42,
        verbose=0
    )
    
    start_time = time.time()
    model.fit(X_train, y_train)
    training_time = time.time() - start_time
    
    print(f"  ✓ Training completed in {training_time:.2f} seconds")
    
    return model, training_time

def evaluate_model(model, X_train, X_test, y_train, y_test):
    """Evaluate model performance"""
    print("\n[3/5] Evaluating model...")
    
    # Predictions
    y_train_pred = model.predict(X_train)
    y_test_pred = model.predict(X_test)
    
    # Calculate predictive metrics
    metrics = {
        'train_accuracy': accuracy_score(y_train, y_train_pred),
        'test_accuracy': accuracy_score(y_test, y_test_pred),
        'train_f1': f1_score(y_train, y_train_pred, zero_division=0),
        'test_f1': f1_score(y_test, y_test_pred, zero_division=0),
        'precision': precision_score(y_test, y_test_pred, zero_division=0),
        'recall': recall_score(y_test, y_test_pred, zero_division=0)
    }
    
    # Measure inference latency (operational metric)
    latencies = []
    for _ in range(100):
        start = time.time()
        _ = model.predict(X_test[:10])
        latencies.append((time.time() - start) * 1000)  # Convert to ms
    
    metrics['inference_latency_ms'] = np.mean(latencies)
    metrics['inference_latency_p95'] = np.percentile(latencies, 95)
    
    print(f"  ✓ Test F1 Score: {metrics['test_f1']:.4f}")
    print(f"  ✓ Test Accuracy: {metrics['test_accuracy']:.4f}")
    print(f"  ✓ Precision: {metrics['precision']:.4f}")
    print(f"  ✓ Recall: {metrics['recall']:.4f}")
    print(f"  ✓ Inference Latency (avg): {metrics['inference_latency_ms']:.2f} ms")
    print(f"  ✓ Inference Latency (p95): {metrics['inference_latency_p95']:.2f} ms")
    
    return metrics

def save_model(model, scaler, experiment_name):
    """Save model and scaler to disk"""
    print("\n[4/5] Saving model...")
    
    model_path = f'models/{experiment_name}_model.pkl'
    scaler_path = f'models/{experiment_name}_scaler.pkl'
    
    # Save model
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    
    # Save scaler
    with open(scaler_path, 'wb') as f:
        pickle.dump(scaler, f)
    
    print(f"  ✓ Model saved: {model_path}")
    print(f"  ✓ Scaler saved: {scaler_path}")
    
    return model_path, scaler_path

def main():
    """Main training pipeline"""
    args = parse_args()
    
    print("="*70)
    print("FRAUD DETECTION MODEL TRAINING")
    print("="*70)
    print(f"Experiment: {args.experiment_name}")
    print(f"Learning Rate: {args.learning_rate}")
    print(f"N Estimators: {args.n_estimators}")
    print(f"Max Depth: {args.max_depth}")
    
    # Initialize W&B
    run = wandb.init(
        project="fraud-detection-capstone",
        name=args.experiment_name,
        config={
            "learning_rate": args.learning_rate,
            "n_estimators": args.n_estimators,
            "max_depth": args.max_depth,
            "model_type": "GradientBoostingClassifier"
        }
    )
    
    # Load data
    X_train, X_test, y_train, y_test, scaler = load_data()
    
    # Train model
    model, training_time = train_model(
        X_train, y_train, 
        args.learning_rate,
        args.n_estimators,
        args.max_depth
    )
    
    # Evaluate model
    metrics = evaluate_model(model, X_train, X_test, y_train, y_test)
    
    # Add training time to metrics
    metrics['training_time_sec'] = training_time
    
    # Log all metrics to W&B
    wandb.log(metrics)
    
    # Update summary for easy comparison
    wandb.run.summary.update({
        "test_f1": metrics['test_f1'],
        "test_accuracy": metrics['test_accuracy'],
        "inference_latency_ms": metrics['inference_latency_ms'],
        "learning_rate": args.learning_rate
    })
    
    # Save model artifacts
    model_path, scaler_path = save_model(model, scaler, args.experiment_name)
    
    # Log model as W&B artifact
    print("\n[5/5] Logging artifacts to W&B...")
    artifact = wandb.Artifact(
        name=f"{args.experiment_name}_model",
        type="model",
        description=f"Fraud detection model with learning_rate={args.learning_rate}"
    )
    artifact.add_file(model_path)
    artifact.add_file(scaler_path)
    run.log_artifact(artifact)
    print("  ✓ Model artifacts logged to W&B")
    
    # Finish W&B run
    run.finish()
    
    print("\n" + "="*70)
    print("✓ TRAINING COMPLETE")
    print("="*70)
    print(f"\nKey Results:")
    print(f"  Test F1 Score: {metrics['test_f1']:.4f}")
    print(f"  Inference Latency: {metrics['inference_latency_ms']:.2f} ms")
    print(f"\nView results: https://wandb.ai/<your-username>/fraud-detection-capstone")

if __name__ == "__main__":
    main()
