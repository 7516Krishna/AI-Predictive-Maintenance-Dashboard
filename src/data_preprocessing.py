import pandas as pd

# -------------------------
# LOAD NASA DATASET
# -------------------------
def load_nasa_data(file):
    """
    Robust NASA dataset loader
    Handles extra spaces and inconsistent columns
    Works for both file path and uploaded file
    """

    # Read file (handles multiple spaces properly)
    df = pd.read_csv(file, sep=r"\s+", header=None, engine="python")

    # Drop completely empty columns
    df = df.dropna(axis=1, how='all')

    # Expected column names
    cols = ['engine_id', 'cycle'] + \
           [f'setting_{i}' for i in range(1, 4)] + \
           [f'sensor_{i}' for i in range(1, 22)]

    # Assign only available columns safely
    df.columns = cols[:df.shape[1]]

    return df


# -------------------------
# CREATE FAILURE LABEL
# -------------------------
def create_failure_label(df, threshold=30):
    """
    Convert Remaining Useful Life (RUL) into binary classification
    """

    # Max cycle per engine
    max_cycle = df.groupby('engine_id')['cycle'].transform('max')

    # Calculate RUL
    df['RUL'] = max_cycle - df['cycle']

    # Create binary label
    df['failure'] = (df['RUL'] <= threshold).astype(int)

    return df


# -------------------------
# SELECT FEATURES (FINAL FIXED VERSION 🔥)
# -------------------------
def select_features(df):
    """
    Select important sensors safely and ensure consistent column names
    """

    required_features = ['sensor_2', 'sensor_3', 'sensor_4', 'sensor_7', 'sensor_11']

    # Keep only available sensors
    available_features = [col for col in required_features if col in df.columns]

    if len(available_features) < 3:
        raise ValueError("❌ Not enough sensor columns found")

    # IMPORTANT FIX: .copy() to avoid pandas warning
    df = df[['engine_id', 'cycle'] + available_features + ['failure']].copy()

    # Fixed mapping for consistent ML input
    mapping = {
        'sensor_2': 'temperature',
        'sensor_3': 'vibration',
        'sensor_4': 'pressure',
        'sensor_7': 'flow_rate',
        'sensor_11': 'efficiency'
    }

    # Rename dynamically but safely
    df = df.rename(columns={col: mapping[col] for col in available_features})

    return df


# -------------------------
# FULL PIPELINE (ONE-CALL FUNCTION 🔥)
# -------------------------
def process_nasa_pipeline(file):
    """
    Complete preprocessing pipeline
    """

    df = load_nasa_data(file)
    df = create_failure_label(df)
    df = select_features(df)

    return df