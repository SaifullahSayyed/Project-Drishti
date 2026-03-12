import os
import logging
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def train():
    csv_path = "backend/data/raw_cases.csv"
    if not os.path.exists(csv_path):
        logger.error(f"Raw data missing at {csv_path}. Run download_njdg_data.py first.")
        return
        
    logger.info("Loading data...")
    df = pd.read_csv(csv_path)
    
    # Feature engineering for XGBoost
    # We want to predict binary outcome: petitioner_won (1 or 0)
    
    # Convert categorical to numerical
    le_district = LabelEncoder()
    le_ctype = LabelEncoder()
    
    df["district_encoded"] = le_district.fit_transform(df["district"])
    df["case_type_encoded"] = le_ctype.fit_transform(df["case_type"])
    
    # Features (X) and Target (y)
    features = ["district_encoded", "case_type_encoded", "lok_adalat_eligible"]
    X = df[features]
    y = df["petitioner_won"]
    
    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Initialize and train XGBoost
    logger.info("Training XGBoost model...")
    model = xgb.XGBClassifier(
        n_estimators=100,
        max_depth=4,
        learning_rate=0.1,
        random_state=42,
        eval_metric="logloss"
    )
    
    model.fit(X_train, y_train)
    
    # Evaluate
    logger.info("Evaluating on test set...")
    y_pred = model.predict(X_test)
    
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, zero_division=0)
    rec = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)
    
    logger.info(f"Accuracy:  {acc:.2f}")
    logger.info(f"Precision: {prec:.2f}")
    logger.info(f"Recall:    {rec:.2f}")
    logger.info(f"F1 Score:  {f1:.2f}")
    
    if acc < 0.65:
        logger.warning("Warning: Model accuracy is below 65% target.")
    else:
        logger.info("Model accuracy meets >65% target.")
        
    # Feature importance plot
    os.makedirs("backend/ml/models", exist_ok=True)
    
    logger.info("Generating feature importance chart...")
    xgb.plot_importance(model)
    plt.title("XGBoost Feature Importance")
    plt.tight_layout()
    plt.savefig("backend/ml/models/feature_importance.png")
    
    # Save model
    model_path = "backend/ml/models/outcome_model.pkl"
    joblib.dump(model, model_path)
    logger.info(f"Saved model artifact to {model_path}")
    
    # In a real scenario, also save encoders to cleanly map inference inputs
    joblib.dump(le_district, "backend/ml/models/le_district.pkl")
    joblib.dump(le_ctype, "backend/ml/models/le_ctype.pkl")

if __name__ == "__main__":
    train()
