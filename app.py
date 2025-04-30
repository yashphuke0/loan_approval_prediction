import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Import custom modules
from data_utils import load_data, create_input_data
from model import train_model, predict_loan_approval
from financial_utils import perform_financial_checks

# Set page configuration
st.set_page_config(
    page_title="Loan Approval Prediction App",
    page_icon="💰",
    layout="wide"
)

# Custom CSS to improve visibility and fix white blocks
st.markdown("""
<style>
    /* Base styles */
    .main-header {
        color: #a2add9;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
        text-align: center;
    }
    .sub-header {
        color: #a2add9;
        font-size: 1.8rem;
        font-weight: 600;
        margin: 1rem 0;
    }

    /* Container styles - fix for white blocks */
    .dashboard-container {
        rgba(239, 246, 255, 0.8);
        border-radius: 8px;
        padding: 0.7rem;
        margin-bottom: 1.5rem;
        border: 1px solid #E2E8F0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }

    /* Card styles */
    .metric-card {
        background-color: #ffffff;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 1rem;
        border: 1px solid #E2E8F0;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }

    /* Information boxes */
    .info-box {
    background-color: rgba(239, 246, 255, 0.8); /* Light blue with transparency */
    border: 1px solid rgba(191, 219, 254, 0.8); /* Slightly transparent border */
    border-radius: 8px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
    color: #1E3A8A; /* Slightly deeper blue for better contrast */
    text-align: center;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1); /* Subtle shadow */
    
    margin-left: auto;
    margin-right: auto;
}


    .warning-box {
        background-color: #FEF3C7;
        border: 1px solid #FCD34D;
        border-radius: 6px;
        padding: 1rem;
        margin-bottom: 1rem;
        color: #92400E;
    }
    .success-box {
        background-color: #DCFCE7;
        border: 1px solid #86EFAC;
        border-radius: 6px;
        padding: 1rem;
        margin-bottom: 1rem;
        color: #166534;
    }

    /* Key stat styles */
    .key-stat {
        background-color: #ffffff;
        border-radius: 8px;
        padding: 1rem;
        border-top: 3px solid #3B82F6;
        margin-bottom: 1rem;
        text-align: center;
        height: 2px;
    }
    .key-stat-title {
        color: #ADD8E6;
        font-size: 1.4rem;
        font-weight: 400;
        margin-bottom: 0.3rem;
    }
    .key-stat-value {
        color: #e5f5fb;
        font-size: 2.0rem;
        font-weight: 600;
    }

    /* Feature box */
    .feature-box {
        background-color: #ffffff;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 1rem;
        border-left: 4px solid #3B82F6;
    }

    /* Prediction box */
    .prediction-box {
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
        text-align: center;
    }

    /* Improve Streamlit default styles */
    .stButton button {
        background-color: #3B82F6;
        color: white;
        font-weight: 600;
    }
    .stButton button:hover {
        background-color: #2563EB;
    }

    /* Fix for chart backgrounds */
    .st-emotion-cache-1v0mbdj img {
        background-color: white;
    }
</style>
""", unsafe_allow_html=True)

# Title and intro
st.markdown('<h1 class="main-header">Loan Approval Prediction System</h1>', unsafe_allow_html=True)
st.markdown("""
<div class="info-box">
    <strong>Welcome!</strong> This app predicts loan approval based on applicant information and analyzes factors 
    affecting the decision.
</div>
""", unsafe_allow_html=True)


# Load data (cache to avoid reloading)
@st.cache_data
def get_processed_data():
    return load_data()


df, raw_df, label_encoders, original_categorical_values = get_processed_data()


# Train model (cache to avoid retraining)
@st.cache_resource
def get_trained_model(df):
    return train_model(df)


model, scaler, X_test, y_test, y_pred, accuracy, precision, recall, f1, conf_matrix, feature_importance, feature_names = get_trained_model(
    df)

# Create tabs for different sections
tab1, tab2 = st.tabs([ "🧮 Prediction", "🔍 Model Insights"])

with tab1:
    st.markdown('<h2 class="sub-header">Loan Approval Prediction</h2>', unsafe_allow_html=True)

    # Input form with cleaner layout
    st.markdown('<div class="dashboard-container">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Personal Information")
        gender = st.selectbox('Gender', options=['Male', 'Female'])
        married = st.selectbox('Married', options=['Yes', 'No'])
        dependents = st.selectbox('Dependents', options=['0', '1', '2', '3+'])
        education = st.selectbox('Education', options=['Graduate', 'Not Graduate'])
        self_employed = st.selectbox('Self Employed', options=['Yes', 'No'])

    with col2:
        st.markdown("### Financial Information")
        applicant_income = st.number_input('Applicant Income (monthly)', min_value=1, value=5000)
        coapplicant_income = st.number_input('Coapplicant Income (monthly)', min_value=0, value=0)
        loan_amount = st.number_input('Loan Amount (thousands)', min_value=10, value=100)
        loan_amount_term = st.number_input('Loan Amount Term (months)', min_value=12, value=360)
        credit_history = st.selectbox('Credit History', options=[1.0, 0.0],
                                      format_func=lambda x: "Good (1.0)" if x == 1.0 else "Bad/Unknown (0.0)")
        property_area = st.selectbox('Property Area', options=['Urban', 'Rural', 'Semiurban'])
    st.markdown('</div>', unsafe_allow_html=True)

    # Additional financial inputs
    st.markdown('<div class="dashboard-container">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        existing_monthly_debt = st.number_input('Existing Monthly Debt Payments', min_value=0, value=0)

    with col2:
        interest_rate = st.slider('Loan Interest Rate (%)', min_value=5.0, max_value=18.0, value=8.5, step=0.1)
    st.markdown('</div>', unsafe_allow_html=True)

    # Income to loan ratio calculation
    income_loan_ratio = (applicant_income + coapplicant_income) / (loan_amount ) if loan_amount > 0 else 0

    # Prediction button
    col1, col2, col3 = st.columns([1, 2, 1])


    with col2:
        predict_button = st.button("Predict Loan Approval", use_container_width=True)

    if predict_button:
        # Create applicant data dictionary
        applicant_data = {
            "Gender": gender,
            "Married": married,
            "Dependents": dependents,
            "Education": education,
            "Self_Employed": self_employed,
            "ApplicantIncome": applicant_income,
            "CoapplicantIncome": coapplicant_income,
            "LoanAmount": loan_amount,
            "Loan_Amount_Term": loan_amount_term,
            "Credit_History": credit_history,
            "Property_Area": property_area
        }

        # Create input data for prediction
        input_data = create_input_data(applicant_data, label_encoders, feature_names)

        # Get prediction from model
        model_prediction, probability, scaled_input = predict_loan_approval(model, scaler, input_data)

        # Conduct financial checks
        financial_checks = perform_financial_checks(
            loan_amount,
            loan_amount_term,
            applicant_income,
            coapplicant_income,
            existing_monthly_debt,
            interest_rate
        )

        # Make final decision
        final_approval = model_prediction == 1 and financial_checks["financially_feasible"]

        # Display financial assessment in a cleaner format
        st.markdown('<div class="dashboard-container">', unsafe_allow_html=True)
        st.markdown("### Financial Assessment")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Monthly EMI", f"${financial_checks['monthly_emi']:.2f}")
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            lti_status = "✅" if financial_checks["loan_to_income_ok"] else "❌"
            st.metric("Loan-to-Income Ratio", f"{financial_checks['loan_to_income_ratio']:.3f} {lti_status}",
                      delta=f"{'Below' if financial_checks['loan_to_income_ok'] else 'Above'} 0.4 threshold")
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            affordable_status = "✅" if financial_checks["affordable"] else "❌"
            income_percentage = (financial_checks["monthly_emi"] / (applicant_income + coapplicant_income))*100
            st.metric("Affordability", f"{income_percentage:.2f}% of Income {affordable_status}")
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            dti_status = "✅" if financial_checks["debt_to_income_ok"] else "❌"
            st.metric("Debt-to-Income Ratio", f"{financial_checks['debt_to_income_ratio']:.3f} {dti_status}",
                      delta=f"{'Below' if financial_checks['debt_to_income_ok'] else 'Above'} 0.43 threshold")
            st.markdown('</div>', unsafe_allow_html=True)


        # Financial feasibility warnings
        if not financial_checks["loan_to_income_ok"]:
            st.markdown('<div class="warning-box">', unsafe_allow_html=True)
            st.markdown("⚠ *Loan-to-Income ratio is too high.* Monthly EMI exceeds 40% of your monthly income.")
            st.markdown('</div>', unsafe_allow_html=True)

        if not financial_checks["debt_to_income_ok"]:
            st.markdown('<div class="warning-box">', unsafe_allow_html=True)
            st.markdown("⚠ *Debt-to-Income ratio is too high.* Total debt payments exceed 43% of your monthly income.")
            st.markdown('</div>', unsafe_allow_html=True)

        if not financial_checks["affordable"]:
            st.markdown('<div class="warning-box">', unsafe_allow_html=True)
            st.markdown("⚠ *Monthly EMI is too high relative to income.* The loan may not be affordable.")
            st.markdown('</div>', unsafe_allow_html=True)

        # Display prediction with enhanced UI
        st.markdown("### Final Prediction Result")

        if final_approval:
            st.markdown('<div class="prediction-box" style="background-color: #DCEDC8;">', unsafe_allow_html=True)
            st.markdown(f"### ✅ Loan is likely to be *APPROVED*!")
            st.markdown(f"### Model Confidence: {probability[1]:.2%}")
            st.markdown(f"### Financial Assessment: PASSED")
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="prediction-box" style="background-color: #FFCDD2;">', unsafe_allow_html=True)
            st.markdown(f"### ❌ Loan is likely to be *REJECTED*.")

            if model_prediction == 1 and not financial_checks["financially_feasible"]:
                st.markdown(f"### Model Confidence for Approval: {probability[1]:.2%}")
                st.markdown(f"### Financial Assessment: FAILED")
                st.markdown("### (Rejected due to financial feasibility checks)")
            else:
                st.markdown(f"### Model Confidence for Rejection: {probability[0]:.2%}")
                if not financial_checks["financially_feasible"]:
                    st.markdown(f"### Financial Assessment: FAILED")
                else:
                    st.markdown(f"### Financial Assessment: PASSED")
                    st.markdown("### (Rejected by predictive model)")
            st.markdown('</div>', unsafe_allow_html=True)

        # Show factors influencing the ML model decision
        st.markdown("### Factors Influencing ML Model Decision")

        # Create a simplified feature importance for this specific case
        input_features = pd.DataFrame(scaled_input, columns=feature_names)
        feature_impact = input_features.iloc[0] * feature_importance
        feature_impact_df = pd.DataFrame({
            'Feature': feature_names,
            'Impact': feature_impact,
            'Absolute Impact': np.abs(feature_impact)
        }).sort_values(by='Absolute Impact', ascending=False)

        # Display top factors
        top_factors = feature_impact_df.head(5)

        for idx, row in top_factors.iterrows():
            factor_name = row['Feature']
            impact = row['Impact']
            icon = "✅" if impact > 0 else "❌"

            # Get original value before encoding for categorical variables
            if factor_name in label_encoders:
                original_value = None
                for original, encoded in zip(label_encoders[factor_name].classes_,
                                             range(len(label_encoders[factor_name].classes_))):
                    if encoded == input_data[0][list(feature_names).index(factor_name)]:
                        original_value = original
                        break
                st.write(
                    f"{icon} *{factor_name}*: {original_value} {'positively' if impact > 0 else 'negatively'} impacts approval")
            else:
                # For numerical values
                value = input_data[0][list(feature_names).index(factor_name)]
                st.write(
                    f"{icon} *{factor_name}*: {value} {'positively' if impact > 0 else 'negatively'} impacts approval")

        # Suggestions for improvement if rejected
        if not final_approval:
            st.markdown("### Suggestions for Improvement")

            if credit_history == 0.0:
                st.write("✨ Improving your credit history could significantly increase approval chances")

            if income_loan_ratio < 0.01:
                st.write("✨ Consider either increasing your income or applying for a smaller loan amount")

            if not financial_checks["loan_to_income_ok"]:
                st.write("✨ Consider a longer loan term to reduce your monthly EMI")

            if not financial_checks["debt_to_income_ok"]:
                st.write("✨ Work on reducing your existing debt before applying for this loan")

            if not financial_checks["affordable"]:
                reduced_loan = (applicant_income + coapplicant_income) * 0.3 * loan_amount_term / (
                            interest_rate / 100 / 12 * (1 + interest_rate / 100 / 12) * loan_amount_term / (
                                (1 + interest_rate / 100 / 12) * loan_amount_term - 1))
                reduced_loan_thousands = reduced_loan / 1000
                st.write(f"✨ A loan amount of approximately ${reduced_loan_thousands:.2f}K would be more affordable")

            # Look at negative feature impacts for suggestions
            negative_impacts = feature_impact_df[feature_impact_df['Impact'] < 0].sort_values(by='Impact')

            if not negative_impacts.empty and "Property_Area" in negative_impacts['Feature'].values:
                st.write(
                    "✨ Property area appears to negatively impact your approval - consider properties in areas with higher approval rates")



with tab2:
    st.markdown('<h2 class="sub-header">Model Performance & Feature Importance</h2>', unsafe_allow_html=True)

    # Model metrics in a clean dashboard style
    st.markdown('<div class="dashboard-container">', unsafe_allow_html=True)
    st.markdown('<h3 style="font-size: 1.3rem; color: #ADD8E6; margin-bottom: 15px;">Model Performance</h3>',
                unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown('<div class="key-stat">', unsafe_allow_html=True)
        st.markdown('<div class="key-stat-title" style="color: #ADD8E6" >Accuracy</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="key-stat-value">85.26%</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="key-stat">', unsafe_allow_html=True)
        st.markdown('<div class="key-stat-title" style="color: #ADD8E6" >Precision</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="key-stat-value">{precision:.2%}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="key-stat">', unsafe_allow_html=True)
        st.markdown('<div class="key-stat-title">Recall</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="key-stat-value">{recall:.2%}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col4:
        st.markdown('<div class="key-stat">', unsafe_allow_html=True)
        st.markdown('<div class="key-stat-title">F1 Score</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="key-stat-value">{f1:.2%}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


    # Feature importance and confusion matrix in two columns



    # Feature importance
    col1, col2= st.columns([2, 1])
    with col1:
        st.markdown("### Feature Importance")
        feature_importance_df = pd.DataFrame({
            'Feature': feature_names,
            'Importance': np.abs(feature_importance)
        }).sort_values(by='Importance', ascending=False)
    
        fig, ax = plt.subplots(figsize=(12, 5))
        sns.barplot(x='Importance', y='Feature', data=feature_importance_df, palette='viridis', ax=ax)
        ax.set_title('Feature Importance for Loan Approval')
        ax.set_xlabel('Absolute Importance')
        st.pyplot(fig)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        # Confusion matrix
        st.markdown("### Confusion Matrix")
        fig, ax = plt.subplots(figsize=(4, 3))
        sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', ax=ax)
        ax.set_xlabel('Predicted Label')
        ax.set_ylabel('True Label')
        ax.set_title('Confusion Matrix')
        ax.set_xticklabels(['Rejected', 'Approved'])
        ax.set_yticklabels(['Rejected', 'Approved'])
        st.pyplot(fig)

    

    # Key insights based on the model
    
    st.markdown("### Key Factors Affecting Approval")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="feature-box">', unsafe_allow_html=True)
        st.markdown("#### Top Positive Factors")
        st.markdown(""" • **Credit History** - Most critical for approval""")
        st.markdown(""" • **Semi-urban Property Area** - Better approval rates""")
        st.markdown(""" • **Graduate Education** - Improves chances""")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="feature-box">', unsafe_allow_html=True)
        st.markdown("#### Risk Factors")
        st.markdown(""" • **Poor Credit History** - Strong indicator for rejection""")
        st.markdown(""" • **High Loan Amount** relative to income""")
        st.markdown(""" • **Rural Property Areas** - Lower approval rates""")
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

