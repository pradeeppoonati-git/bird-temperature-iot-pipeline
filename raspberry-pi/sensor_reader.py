"""
DHT22 Temperature & Humidity Sensor Reader
Reads temperature and humidity from DHT22 sensor connected to Raspberry Pi GPIO
"""

import time
import board
import adafruit_dht
from datetime import datetime
import json

# Configuration
DHT_PIN = board.D4  # GPIO 4

def read_sensor():
    """Read temperature and humidity from DHT22 sensor"""
    
    # Initialize sensor
    dht_device = adafruit_dht.DHT22(DHT_PIN, use_pulseio=False)
    
    try:
        # Read sensor data
        temperature_c = dht_device.temperature
        humidity = dht_device.humidity
        
        if temperature_c is not None and humidity is not None:
            temperature_f = round(temperature_c * 9/5 + 32, 2)
            
            reading = {
                "timestamp": datetime.now().isoformat(),
                "sensor_id": "raspberry_pi_dht22",
                "location": "bird_cage_window_area",
                "temperature_celsius": round(temperature_c, 2),
                "temperature_fahrenheit": temperature_f,
                "humidity": round(humidity, 2),
                "source": "DHT22"
            }
            
            return reading
        else:
            print("Failed to read sensor data")
            return None
            
    except RuntimeError as e:
        print(f"Error reading sensor: {e}")
        print("Retrying in 2 seconds...")
        time.sleep(2)
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None
    finally:
        dht_device.exit()

if __name__ == "__main__":
    # Test with multiple readings
    print("=" * 60)
    print("DHT22 Sensor Reader - Bird Cage Location")
    print("=" * 60)
    
    for i in range(5):
        print(f"\nReading {i+1}:")
        data = read_sensor()
        if data:
            print(json.dumps(data, indent=2))
        time.sleep(3)  # Wait 3 seconds between readings
    
    print("\n" + "=" * 60)
    print("Sensor test complete!")