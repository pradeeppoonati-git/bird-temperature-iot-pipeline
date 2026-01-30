"""
Ecobee Temperature Reader
Reads current temperature and humidity from Ecobee via Home Assistant API
"""

import requests
import json
from datetime import datetime

# Configuration
HOME_ASSISTANT_URL = "http://10.20.27.40:8123"
HOME_ASSISTANT_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiI2ODUzNWVhZWRmYWY0NGJlOGVjODViMmI2ZTIxNWY5NyIsImlhdCI6MTc2OTc0MjQwNywiZXhwIjoyMDg1MTAyNDA3fQ.QF5Yf4jRrqq5KijgrZdeK7CyKY6iiXcJ6NXBQDXWUyg"

def get_ecobee_data():
    """Fetch current Ecobee temperature and humidity"""
    
    headers = {
        "Authorization": f"Bearer {HOME_ASSISTANT_TOKEN}",
        "Content-Type": "application/json"
    }
    
    try:
        # Get temperature
        temp_response = requests.get(
            f"{HOME_ASSISTANT_URL}/api/states/sensor.my_ecobee_current_temperature",
            headers=headers
        )
        temp_data = temp_response.json()
        
        # Get humidity
        humidity_response = requests.get(
            f"{HOME_ASSISTANT_URL}/api/states/sensor.my_ecobee_current_humidity",
            headers=headers
        )
        humidity_data = humidity_response.json()
        
        # Get HVAC status
        hvac_response = requests.get(
            f"{HOME_ASSISTANT_URL}/api/states/climate.my_ecobee",
            headers=headers
        )
        hvac_data = hvac_response.json()
        
        # Format data
        reading = {
            "timestamp": datetime.now().isoformat(),
            "sensor_id": "ecobee_thermostat",
            "location": "whole_house",
            "temperature_fahrenheit": float(temp_data['state']),
            "temperature_celsius": round((float(temp_data['state']) - 32) * 5/9, 2),
            "humidity": float(humidity_data['state']),
            "hvac_mode": hvac_data['state'],
            "hvac_action": hvac_data['attributes']['hvac_action'],
            "target_temperature": hvac_data['attributes']['temperature']
        }
        
        return reading
        
    except Exception as e:
        print(f"Error reading Ecobee data: {e}")
        return None

if __name__ == "__main__":
    # Test the function
    data = get_ecobee_data()
    if data:
        print("=" * 60)
        print("Ecobee Reading:")
        print(json.dumps(data, indent=2))
        print("=" * 60)
    else:
        print("Failed to read Ecobee data")