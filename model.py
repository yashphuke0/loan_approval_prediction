import numpy as np
import pandas as pd
import joblib
from pathlib import Path
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score


MODEL_ARTIFACT_PATH = Path("saved_models/loan_model.joblib")


def train_model(df):
    """
    Train the loan approval prediction model

    Args:
        df (pandas.DataFrame): Preprocessed dataframe with features and target

    Returns:
        tuple: (model, scaler, X_test, y_test, y_pred, accuracy, precision, recall, f1, conf_matrix, feature_importance, feature_names)
    """
    # Prepare features and target
    X = df.drop("Loan_Status", axis=1)
    y = df["Loan_Status"]

    # Split into train and test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Scale features using train-only fit to prevent leakage
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train.values)
    X_test_scaled = scaler.transform(X_test.values)

    # Tune linear SVM hyperparameters while keeping coefficient-based explainability
    param_grid = {
        "C": [0.1, 1, 3, 5, 10],
        "class_weight": [None, "balanced"]
    }
    base_model = SVC(kernel="linear", probability=True, random_state=42)
    grid_search = GridSearchCV(base_model, param_grid=param_grid, scoring="f1", cv=5, n_jobs=-1)
    grid_search.fit(X_train_scaled, y_train)
    model = grid_search.best_estimator_

    # Evaluate
    y_pred = model.predict(X_test_scaled)

    # Calculate metrics
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    conf_matrix = confusion_matrix(y_test, y_pred)

    # Get feature importance from SVM coefficients (linear kernel)
    feature_importance = model.coef_[0].copy()
    feature_names = X.columns.tolist()

    return (
        model,
        scaler,
        X_test_scaled,
        y_test,
        y_pred,
        accuracy,
        precision,
        recall,
        f1,
        conf_matrix,
        feature_importance,
        feature_names,
    )


def save_model_artifact(model_bundle, artifact_path=MODEL_ARTIFACT_PATH):
    """Persist trained model bundle to disk."""
    artifact_path = Path(artifact_path)
    artifact_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model_bundle, artifact_path)


def load_model_artifact(artifact_path=MODEL_ARTIFACT_PATH):
    """Load persisted model bundle if available."""
    artifact_path = Path(artifact_path)
    if not artifact_path.exists():
        return None
    return joblib.load(artifact_path)


def get_or_train_model(df, artifact_path=MODEL_ARTIFACT_PATH):
    """
    Load a saved model bundle from disk. Train and save if missing or stale.
    """
    expected_features = df.drop("Loan_Status", axis=1).columns.tolist()
    model_bundle = load_model_artifact(artifact_path)
    if model_bundle is not None:
        saved_feature_names = model_bundle[-1]
        if list(saved_feature_names) == expected_features:
            return model_bundle

    model_bundle = train_model(df)
    save_model_artifact(model_bundle, artifact_path)
    return model_bundle


def predict_loan_approval(model, scaler, input_data):
    """
    Predict loan approval using the trained model

    Args:
        model: Trained SVM model
        scaler: Fitted StandardScaler
        input_data (numpy.ndarray): Applicant data encoded as numpy array

    Returns:
        tuple: (prediction, probability)
    """
    # Scale the input data with feature names when available.
    if hasattr(scaler, "feature_names_in_"):
        input_frame = pd.DataFrame(input_data, columns=scaler.feature_names_in_)
        scaled_input = scaler.transform(input_frame)
    else:
        scaled_input = scaler.transform(input_data)

    # Get prediction and probability
    prediction = model.predict(scaled_input)[0]
    probability = model.predict_proba(scaled_input)[0]

    return prediction, probability, scaled_input


def analyze_feature_impact(feature_names, feature_importance, scaled_input):
    """
    Analyze the impact of features on the prediction

    Args:
        feature_names (list): List of feature names
        feature_importance (numpy.ndarray): Feature importance from model
        scaled_input (numpy.ndarray): Scaled input data

    Returns:
        pandas.DataFrame: DataFrame with feature impact analysis
    """
    input_features = pd.DataFrame(scaled_input, columns=feature_names)
    feature_impact = input_features.iloc[0] * feature_importance

    feature_impact_df = pd.DataFrame({
        'Feature': feature_names,
        'Impact': feature_impact,
        'Absolute Impact': np.abs(feature_impact)
    }).sort_values(by='Absolute Impact', ascending=False)

    return feature_impact_df