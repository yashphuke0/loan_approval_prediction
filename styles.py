def load_css():
    """
    Enhanced CSS styles for the Streamlit app with a modern tech aesthetic

    Returns:
        str: CSS code for the app
    """
    return """
<style>
    /* Global styling & typography */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Header and titles */
    .main-header {
        font-size: 2.8rem;
        color: #2563EB;
        font-weight: 700;
        margin-bottom: 1.5rem;
        text-shadow: 0px 0px 10px rgba(37, 99, 235, 0.1);
        background: linear-gradient(135deg, #2563EB 0%, #4F46E5 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .sub-header {
        font-size: 1.8rem;
        color: #3B82F6;
        font-weight: 600;
        border-bottom: 2px solid rgba(59, 130, 246, 0.2);
        padding-bottom: 0.5rem;
        margin-bottom: 1.5rem;
    }

    /* Card and container styling */
    .metric-card {
        background: #FFFFFF;
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        border: 1px solid rgba(226, 232, 240, 0.8);
        margin-bottom: 1.2rem;
    }

    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
    }

    /* Prediction results box with glassmorphism effect */
    .prediction-box {
        padding: 25px;
        border-radius: 16px;
        font-weight: 600;
        text-align: center;
        font-size: 1.4rem;
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.18);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        margin: 2rem 0;
    }

    /* Custom tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1px;
        background-color: #F1F5F9;
        padding: 5px;
        border-radius: 10px;
    }

    .stTabs [data-baseweb="tab"] {
        height: 56px;
        white-space: pre-wrap;
        border-radius: 8px;
        gap: 1px;
        padding: 8px 16px;
        font-weight: 500;
        color: #64748B;
        transition: all 0.2s ease;
        margin: 3px;
    }

    .stTabs [aria-selected="true"] {
        background-color: #FFFFFF;
        color: #2563EB;
        border-bottom: none;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        font-weight: 600;
    }

    .stTabs [data-baseweb="tab"]:hover {
        background-color: rgba(255, 255, 255, 0.8);
        color: #3B82F6;
    }

    /* Custom notification boxes */
    .warning-box {
        padding: 16px;
        border-radius: 12px;
        background-color: #FEF9C3;
        border-left: 5px solid #F59E0B;
        margin-bottom: 16px;
        font-weight: 500;
        color: #854D0E;
        box-shadow: 0 4px 6px rgba(245, 158, 11, 0.1);
    }

    .success-box {
        padding: 16px;
        border-radius: 12px;
        background-color: #DCFCE7;
        border-left: 5px solid #10B981;
        margin-bottom: 16px;
        font-weight: 500;
        color: #166534;
        box-shadow: 0 4px 6px rgba(16, 185, 129, 0.1);
    }

    .error-box {
        padding: 16px;
        border-radius: 12px;
        background-color: #FEE2E2;
        border-left: 5px solid #EF4444;
        margin-bottom: 16px;
        font-weight: 500;
        color: #991B1B;
        box-shadow: 0 4px 6px rgba(239, 68, 68, 0.1);
    }

    .info-box {
        padding: 16px;
        border-radius: 12px;
        background-color: #E0F2FE;
        border-left: 5px solid #0EA5E9;
        margin-bottom: 16px;
        font-weight: 500;
        color: #0C4A6E;
        box-shadow: 0 4px 6px rgba(14, 165, 233, 0.1);
    }

    /* Enhanced button styling */
    .stButton > button {
        border-radius: 8px;
        padding: 10px 24px;
        font-weight: 600;
        background: linear-gradient(135deg, #2563EB 0%, #4F46E5 100%);
        color: white;
        border: none;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2);
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(37, 99, 235, 0.3);
    }

    .stButton > button:active {
        transform: translateY(1px);
        box-shadow: 0 2px 10px rgba(37, 99, 235, 0.2);
    }

    /* Custom slider styling */
    .stSlider > div > div > div {
        background-color: #DBEAFE;
    }

    .stSlider > div > div > div > div {
        background-color: #2563EB;
    }

    /* Expander styling */
    .streamlit-expanderHeader {
        font-weight: 600;
        color: #3B82F6;
        background-color: rgba(219, 234, 254, 0.4);
        border-radius: 8px;
    }

    /* Progress bar styling */
    .stProgress > div > div {
        background-color: #2563EB;
        background: linear-gradient(90deg, #2563EB 0%, #4F46E5 100%);
    }

    /* Selectbox styling */
    .stSelectbox > div > div {
        background-color: white;
        border-radius: 8px;
        border: 1px solid #E2E8F0;
    }

    /* Custom data frame styling */
    .dataframe {
        border-collapse: separate;
        border-spacing: 0;
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    }

    .dataframe thead tr {
        background-color: #F1F5F9;
        color: #1E40AF;
        font-weight: 600;
        text-align: left;
    }

    .dataframe thead tr th {
        padding: 12px 15px;
        border-bottom: 1px solid #E2E8F0;
    }

    .dataframe tbody tr {
        border-bottom: 1px solid #E2E8F0;
    }

    .dataframe tbody tr:nth-child(even) {
        background-color: #F8FAFC;
    }

    .dataframe tbody tr:hover {
        background-color: #DBEAFE;
    }

    .dataframe tbody tr td {
        padding: 10px 15px;
    }

    /* Dashboard-like containers */
    .dashboard-container {
        background-color: white;
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        margin-bottom: 20px;
    }

    /* Key stat box styling */
    .key-stat {
        background-color: white;
        border-radius: 12px;
        padding: 16px;
        border-top: 5px solid #2563EB;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        text-align: center;
    }

    .key-stat-title {
        font-weight: 600;
        color: #64748B;
        font-size: 0.9rem;
        margin-bottom: 5px;
    }

    .key-stat-value {
        font-weight: 700;
        color: #1E40AF;
        font-size: 1.8rem;
    }

    /* Feature highlight boxes */
    .feature-box {
        background-color: white;
        border-radius: 14px;
        padding: 20px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
        border-left: 4px solid #2563EB;
        margin-bottom: 15px;
        transition: transform 0.2s ease;
    }

    .feature-box:hover {
        transform: translateX(5px);
    }

    /* Footer styling */
    .footer {
        text-align: center;
        padding: 20px;
        color: #64748B;
        font-size: 0.9rem;
        margin-top: 40px;
        border-top: 1px solid #E2E8F0;
    }
</style>
"""