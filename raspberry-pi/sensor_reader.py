"""
DHT22 Temperature & Humidity Sensor Reader
Reads temperature and humidity from DHT22 sensor connected to Raspberry Pi GPIO
"""

# Uncomment when DHT22 sensor arrives:
# import Adafruit_DHT
import time
from datetime import datetime
import json

# Configuration
DHT_SENSOR = None  # Will be: Adafruit_DHT.DHT22
DHT_PIN = 4  # GPIO pin 4 (physical pin 7)

def read_sensor():
    """Read temperature and humidity from DHT22 sensor"""
    
    # PLACEHOLDER - Uncomment when sensor arrives:
    # humidity, temperature_c = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    
    # Simulated data for testing (remove when sensor is connected):
    import random
    humidity = round(45 + random.uniform(-5, 5), 2)
    temperature_c = round(20 + random.uniform(-3, 3), 2)
    
    if humidity is not None and temperature_c is not None:
        temperature_f = round(temperature_c * 9/5 + 32, 2)
        
        reading = {
            "timestamp": datetime.now().isoformat(),
            "sensor_id": "raspberry_pi_window",
            "location": "bird_window_area",
            "temperature_celsius": temperature_c,
            "temperature_fahrenheit": temperature_f,
            "humidity": humidity,
            "source": "DHT22"
        }
        
        return reading
    else:
        print("Failed to read sensor data")
        return None

def install_instructions():
    """Instructions for installing sensor library when DHT22 arrives"""
    print("""
    When DHT22 sensor arrives, install the library:
    
    sudo pip3 install Adafruit_DHT --break-system-packages
    
    Then uncomment the import and sensor reading lines in this file.
    
    Wiring:
    - DHT22 VCC (Pin 1) → Raspberry Pi 3.3V (Physical Pin 1)
    - DHT22 Data (Pin 2) → Raspberry Pi GPIO 4 (Physical Pin 7)
    - DHT22 GND (Pin 4) → Raspberry Pi GND (Physical Pin 9)
    - 10K resistor between VCC and Data pins (pull-up resistor)
    """)

if __name__ == "__main__":
    # Test with simulated data
    print("=" * 60)
    print("DHT22 Sensor Reader (Simulated Mode)")
    print("=" * 60)
    
    for i in range(5):
        data = read_sensor()
        if data:
            print(f"\nReading {i+1}:")
            print(json.dumps(data, indent=2))
        time.sleep(2)
    
    print("\n" + "=" * 60)
    install_instructions()