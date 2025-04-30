import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, precision_score, recall_score, \
    f1_score


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

    # Scale Features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Split into train and test
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

    # Train SVM model with balanced class weights
    model = SVC(kernel='linear', class_weight='balanced', probability=True)
    model.fit(X_train, y_train)

    # Evaluate
    y_pred = model.predict(X_test)

    # Calculate metrics
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    conf_matrix = confusion_matrix(y_test, y_pred)

    # Get feature importance from SVM coefficients
    feature_importance = model.coef_[0]

    return model, scaler, X_test, y_test, y_pred, accuracy, precision, recall, f1, conf_matrix, feature_importance, X.columns


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
    # Scale the input data
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