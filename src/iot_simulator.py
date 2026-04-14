import pandas as pd
import numpy as np
import time
from datetime import datetime

# -------------------------
# SENSOR DATA GENERATOR
# -------------------------
def generate_sensor_data(device_id=1):
    return {
        "timestamp": datetime.now(),
        "device_id": device_id,
        "temperature": np.random.normal(70, 5),
        "vibration": np.random.normal(0.3, 0.1),
        "pressure": np.random.normal(30, 3),
        "failure": 0
    }


# -------------------------
# REAL-TIME STREAM
# -------------------------
def stream_data(num_points=100, delay=0.5):
    data = []

    for i in range(num_points):

        # Simulate multiple devices 🔥
        device_id = np.random.randint(1, 4)

        sensor = generate_sensor_data(device_id)

        # -------------------------
        # Inject anomalies 🔥
        # -------------------------
        if np.random.rand() < 0.15:
            sensor["temperature"] += np.random.randint(15, 25)
            sensor["vibration"] += np.random.uniform(0.3, 0.6)
            sensor["pressure"] += np.random.randint(10, 20)
            sensor["failure"] = 1

        data.append(sensor)

        df = pd.DataFrame(data)

        yield df

        time.sleep(delay)