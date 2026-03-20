import requests
import time
import math

BASE_URL = "" 

gyro_Xaxis = "gyrX"
gyro_Yaxis = "gyrY"
gyro_Zaxis = "gyrZ"

accelerometer_Xaxis = "accX"
accelerometer_Yaxis = "accY"
accelerometer_Zaxis = "accZ"

class Gyroscope() :
    def get_latest(buffer_name) :
        url_final = f"{BASE_URL}/get?{buffer_name}"
        r = requests.get(url_final).json()

        try :
            # Extract value from : 
            # {"buffer": { "gyrX": { "buffer": [value] } }
            return r["buffer"][buffer_name]["buffer"][0]
        except :
            return None
        
class Accelerometer() :
    def get_latest(buffer_name) :
        url_final = f"{BASE_URL}/get?{buffer_name}" 
        r = requests.get(url_final).json

        try :
            return r["buffer"][buffer_name]["buffer"][0]
        except :
            return None


# Filters
def refine_Gyroscope_data(process_noise=0.01, measurement_noise=0.1):
    """
    Refines gyroscope data using a Kalman filter for optimal noise reduction.
    
    The Kalman filter dynamically balances between trusting the sensor and 
    trusting the prediction, resulting in smooth output that still responds 
    quickly to real movements.
    
    Args:
        process_noise (float): Expected uncertainty in the gyroscope itself (default: 0.01)
                               Lower = trust prediction more, smoother but may lag
                               Higher = trust sensor more, faster response but noisier
        measurement_noise (float): Expected sensor noise/jitter (default: 0.1)
                                   Lower = trust sensor measurements more
                                   Higher = filter out more jitter
    
    Returns:
        tuple: (refined_gyrX, refined_gyrY, refined_gyrZ) - Kalman-filtered values
    """
    
    # Get raw gyroscope data from sensor
    gyrX = Gyroscope.get_latest(gyro_Xaxis)
    gyrY = Gyroscope.get_latest(gyro_Yaxis)
    gyrZ = Gyroscope.get_latest(gyro_Zaxis)
    
    # Handle None values
    if gyrX is None or gyrY is None or gyrZ is None:
        return 0.0, 0.0, 0.0
    
    # Initialize Kalman filter state on first call
    if not hasattr(refine_Gyroscope_data, 'initialized'):
        refine_Gyroscope_data.initialized = True
        # State estimates (what we think the true value is)
        refine_Gyroscope_data.estimate_X = gyrX
        refine_Gyroscope_data.estimate_Y = gyrY
        refine_Gyroscope_data.estimate_Z = gyrZ
        # Error covariance (confidence in our estimate)
        refine_Gyroscope_data.error_X = 1.0
        refine_Gyroscope_data.error_Y = 1.0
        refine_Gyroscope_data.error_Z = 1.0
    
    # Kalman filter update for X axis
    refined_gyrX = _kalman_filter_update(
        refine_Gyroscope_data, 'X', gyrX, process_noise, measurement_noise
    )
    
    # Kalman filter update for Y axis
    refined_gyrY = _kalman_filter_update(
        refine_Gyroscope_data, 'Y', gyrY, process_noise, measurement_noise
    )
    
    # Kalman filter update for Z axis
    refined_gyrZ = _kalman_filter_update(
        refine_Gyroscope_data, 'Z', gyrZ, process_noise, measurement_noise
    )
    
    return refined_gyrX, refined_gyrY, refined_gyrZ


def _kalman_filter_update(state, axis, measurement, process_noise, measurement_noise):
    """
    Performs one iteration of the Kalman filter for a single axis.
    
    Args:
        state: Object storing Kalman state (estimate_X, error_X, etc.)
        axis: 'X', 'Y', or 'Z' axis
        measurement: Raw sensor value
        process_noise: Process noise parameter
        measurement_noise: Measurement noise parameter
    
    Returns:
        float: Filtered estimate for this axis
    """
    
    # Get current state
    estimate = getattr(state, f'estimate_{axis}')
    error = getattr(state, f'error_{axis}')
    
    # Prediction step: predict next state (assume no change)
    predicted_estimate = estimate
    predicted_error = error + process_noise
    
    # Update step: calculate Kalman gain (how much to trust the measurement)
    kalman_gain = predicted_error / (predicted_error + measurement_noise)
    
    # Correct estimate based on measurement
    new_estimate = predicted_estimate + kalman_gain * (measurement - predicted_estimate)
    
    # Update error covariance for next iteration
    new_error = (1 - kalman_gain) * predicted_error
    
    # Store updated state
    setattr(state, f'estimate_{axis}', new_estimate)
    setattr(state, f'error_{axis}', new_error)
    
    return new_estimate