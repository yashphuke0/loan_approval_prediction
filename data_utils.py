import pandas as pd
from sklearn.preprocessing import LabelEncoder


def load_data():
    """
    Load and preprocess the dataset for loan approval prediction

    Returns:
        tuple: (processed_df, raw_df, label_encoders, original_categorical_values)
    """
    df = pd.read_csv("train_u6lujuX_CVtuZ9i.csv")

    # Make a copy of the dataframe before preprocessing
    raw_df = df.copy()

    # Drop Loan_ID if present
    if 'Loan_ID' in df.columns:
        df.drop("Loan_ID", axis=1, inplace=True)

    # Fill missing values
    df.fillna({
        "Gender": df["Gender"].mode()[0],
        "Married": df["Married"].mode()[0],
        "Dependents": df["Dependents"].mode()[0],
        "Self_Employed": df["Self_Employed"].mode()[0],
        "LoanAmount": df["LoanAmount"].median(),
        "Loan_Amount_Term": df["Loan_Amount_Term"].median(),
        "Credit_History": df["Credit_History"].mode()[0],
    }, inplace=True)

    # Store original values for categorical columns before encoding
    original_categorical_values = {}
    categorical_cols = ["Gender", "Married", "Dependents", "Education", "Self_Employed", "Property_Area"]
    for col in categorical_cols:
        original_categorical_values[col] = df[col].unique()

    # Encode categorical columns
    label_encoders = {}
    for col in categorical_cols:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        label_encoders[col] = le

    # Convert Loan_Status from 'Y'/'N' to 1/0
    df['Loan_Status'] = df['Loan_Status'].map({'Y': 1, 'N': 0})

    return df, raw_df, label_encoders, original_categorical_values


def create_input_data(applicant_data, label_encoders, feature_names):
    """
    Create encoded input data from user input for prediction

    Args:
        applicant_data (dict): Dictionary containing applicant information
        label_encoders (dict): Dictionary of label encoders for categorical features
        feature_names (list): List of feature names

    Returns:
        numpy.ndarray: Encoded input data array
    """
    import numpy as np

    # Extract values from the applicant_data dictionary
    input_data = {
        "Gender": label_encoders["Gender"].transform([applicant_data["Gender"]])[0],
        "Married": label_encoders["Married"].transform([applicant_data["Married"]])[0],
        "Dependents": label_encoders["Dependents"].transform([applicant_data["Dependents"]])[0],
        "Education": label_encoders["Education"].transform([applicant_data["Education"]])[0],
        "Self_Employed": label_encoders["Self_Employed"].transform([applicant_data["Self_Employed"]])[0],
        "ApplicantIncome": applicant_data["ApplicantIncome"],
        "CoapplicantIncome": applicant_data["CoapplicantIncome"],
        "LoanAmount": applicant_data["LoanAmount"],
        "Loan_Amount_Term": applicant_data["Loan_Amount_Term"],
        "Credit_History": applicant_data["Credit_History"],
        "Property_Area": label_encoders["Property_Area"].transform([applicant_data["Property_Area"]])[0]
    }

    return np.array(list(input_data.values())).reshape(1, -1)