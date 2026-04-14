import pandas as pd
from difflib import get_close_matches
from sklearn.ensemble import IsolationForest

# -------------------------
# MAIN RESPONSE FUNCTION
# -------------------------
def generate_response(query, df):
    if df is None:
        return "⚠️ Please upload a dataset first to start analysis."

    query = query.lower()

    # -------------------------
    # Smart Column Matching 🔥
    # -------------------------
    def find_column(user_query):
        cols = df.columns.tolist()
        matches = get_close_matches(user_query, cols, n=1, cutoff=0.5)
        return matches[0] if matches else None

    # -------------------------
    # Basic Info
    # -------------------------
    if "columns" in query:
        return f"📌 Columns:\n{list(df.columns)}"

    if "shape" in query or "size" in query:
        return f"📊 Rows: {df.shape[0]}, Columns: {df.shape[1]}"

    # -------------------------
    # Summary
    # -------------------------
    if "summary" in query or "describe" in query:
        return f"📊 Summary:\n{df.describe().to_string()}"

    # -------------------------
    # Missing Values
    # -------------------------
    if "missing" in query or "null" in query:
        return f"❗ Missing Values:\n{df.isnull().sum().to_string()}"

    # -------------------------
    # Correlation
    # -------------------------
    if "correlation" in query:
        return f"🔗 Correlation:\n{df.corr(numeric_only=True).to_string()}"

    # -------------------------
    # Column-based Queries (SMART)
    # -------------------------
    for col in df.columns:
        if col.lower() in query:
            return column_operations(query, df, col)

    # Try fuzzy match 🔥
    guessed_col = find_column(query)
    if guessed_col:
        return f"🤖 I think you meant '{guessed_col}'\n" + column_operations(query, df, guessed_col)

    # -------------------------
    # Anomaly Detection (🔥 INDUSTRY FEATURE)
    # -------------------------
    if "anomaly" in query or "outlier" in query:
        return detect_anomalies(df)

    # -------------------------
    # Insights
    # -------------------------
    if "insight" in query or "analyze" in query:
        return generate_auto_insight(df)

    if "suggest" in query or "what next" in query:
        return suggest_questions(df)

    # -------------------------
    # Default
    # -------------------------
    return f"""
🤖 Here's what I found:

{generate_auto_insight(df)}

👉 Try:
- anomaly detection
- correlation
- mean of column_name
"""


# -------------------------
# COLUMN OPERATIONS
# -------------------------
def column_operations(query, df, col):
    try:
        if "mean" in query:
            return f"📈 Mean of {col}: {df[col].mean():.2f}"

        if "max" in query:
            return f"🔺 Max of {col}: {df[col].max()}"

        if "min" in query:
            return f"🔻 Min of {col}: {df[col].min()}"

        if "unique" in query:
            return f"🔢 Unique values in {col}: {df[col].nunique()}"

        if "distribution" in query:
            skew = df[col].skew()
            return f"📊 {col} distribution is {'skewed' if skew > 0 else 'balanced'}"

    except:
        return f"⚠️ Cannot analyze {col}. Might be non-numeric."

    return f"ℹ️ Try asking: mean/max/min of {col}"


# -------------------------
# 🔥 ANOMALY DETECTION
# -------------------------
def detect_anomalies(df):
    numeric_df = df.select_dtypes(include=['int64', 'float64'])

    if numeric_df.shape[1] == 0:
        return "⚠️ No numeric data available for anomaly detection."

    model = IsolationForest(contamination=0.05)
    preds = model.fit_predict(numeric_df)

    anomalies = (preds == -1).sum()

    return f"""
🚨 Anomaly Detection Result:

- Total records: {len(df)}
- Anomalies detected: {anomalies}

👉 These are unusual patterns in your data.
"""


# -------------------------
# AUTO INSIGHTS
# -------------------------
def generate_auto_insight(df):
    insights = []

    if df.isnull().sum().sum() > 0:
        insights.append("⚠️ Missing values detected.")

    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns

    if len(numeric_cols) > 0:
        insights.append(f"📊 {len(numeric_cols)} numeric features found.")

        for col in numeric_cols[:2]:
            insights.append(
                f"{col}: mean={df[col].mean():.2f}, std={df[col].std():.2f}"
            )

    return "\n".join(insights)


# -------------------------
# SUGGESTIONS
# -------------------------
def suggest_questions(df):
    questions = [
        "📊 show summary",
        "❗ missing values",
        "🔗 correlation",
        "🚨 anomaly detection"
    ]

    for col in df.columns[:2]:
        questions.append(f"📈 mean of {col}")

    return "💡 Try:\n\n" + "\n".join(questions)