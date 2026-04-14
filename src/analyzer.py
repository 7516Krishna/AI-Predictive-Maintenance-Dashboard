import pandas as pd
import numpy as np

# -------------------------
# MAIN FUNCTION (IMPORTANT FIX 🔥)
# -------------------------
def analyze_data(df):
    """
    Main function used by app.py
    """
    return f"""
📊 DATA ANALYSIS REPORT

{generate_insights(df)}

----------------------------
📌 BASIC INFO:
Rows: {df.shape[0]}
Columns: {df.shape[1]}

----------------------------
❗ MISSING VALUES:
{get_missing_values(df)}

----------------------------
📊 HEALTH CHECK:
{data_health_check(df)}
"""

# -------------------------
# BASIC DATA SUMMARY
# -------------------------
def get_basic_info(df):
    return {
        "rows": df.shape[0],
        "columns": df.shape[1],
        "column_names": list(df.columns)
    }

# -------------------------
# STATISTICAL SUMMARY
# -------------------------
def get_statistical_summary(df):
    try:
        return df.describe(include='all').to_string()
    except Exception as e:
        return f"⚠️ Unable to generate summary: {e}"

# -------------------------
# MISSING VALUES
# -------------------------
def get_missing_values(df):
    missing = df.isnull().sum()
    total_missing = missing.sum()

    if total_missing == 0:
        return "✅ No missing values found."

    return f"{missing[missing > 0].to_string()}\nTotal Missing: {total_missing}"

# -------------------------
# COLUMN TYPES
# -------------------------
def get_column_types(df):
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    datetime_cols = df.select_dtypes(include=['datetime', 'datetimetz']).columns.tolist()

    return {
        "numeric": numeric_cols,
        "categorical": categorical_cols,
        "datetime": datetime_cols
    }

# -------------------------
# CORRELATION MATRIX
# -------------------------
def get_correlation(df):
    numeric_df = df.select_dtypes(include=['number'])

    if numeric_df.shape[1] < 2:
        return "⚠️ Not enough numeric columns for correlation."

    return numeric_df.corr().round(2).to_string()

# -------------------------
# COLUMN ANALYSIS
# -------------------------
def analyze_column(df, col):
    if col not in df.columns:
        return f"⚠️ Column '{col}' not found."

    try:
        if pd.api.types.is_numeric_dtype(df[col]):
            return f"""
📊 {col}:
Mean: {df[col].mean():.2f}
Std: {df[col].std():.2f}
Min: {df[col].min()}
Max: {df[col].max()}
"""
        else:
            mode_val = df[col].mode()
            most_freq = mode_val[0] if not mode_val.empty else "N/A"

            return f"""
🧾 {col}:
Unique: {df[col].nunique()}
Most Frequent: {most_freq}
"""
    except Exception as e:
        return f"⚠️ Error analyzing column: {e}"

# -------------------------
# AUTO INSIGHTS
# -------------------------
def generate_insights(df):
    insights = []

    total_missing = df.isnull().sum().sum()
    if total_missing > 0:
        insights.append(f"⚠️ Missing values: {total_missing}")

    col_types = get_column_types(df)

    if col_types["numeric"]:
        insights.append(f"📊 Numeric columns: {len(col_types['numeric'])}")

        for col in col_types["numeric"][:2]:
            insights.append(
                f"{col}: mean={df[col].mean():.2f}, std={df[col].std():.2f}"
            )

    if col_types["categorical"]:
        insights.append(f"🧾 Categorical columns: {len(col_types['categorical'])}")

    if col_types["datetime"]:
        insights.append(f"⏱ Datetime columns: {len(col_types['datetime'])}")

    return "\n".join(insights)

# -------------------------
# DATA HEALTH CHECK
# -------------------------
def data_health_check(df):
    report = []

    if df.isnull().sum().sum() > 0:
        report.append("⚠️ Missing values present.")

    duplicates = df.duplicated().sum()
    if duplicates > 0:
        report.append(f"⚠️ Duplicate rows: {duplicates}")

    numeric_cols = df.select_dtypes(include=['number']).columns
    if len(numeric_cols) > 0:
        report.append(f"📊 Numeric columns: {len(numeric_cols)}")

    constant_cols = [col for col in df.columns if df[col].nunique(dropna=False) <= 1]
    if constant_cols:
        report.append(f"⚠️ Constant columns: {constant_cols}")

    if not report:
        return "✅ Dataset looks clean and ready."

    return "\n".join(report)