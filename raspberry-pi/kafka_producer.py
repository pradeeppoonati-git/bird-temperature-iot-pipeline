"""
Kafka Producer - Stream Temperature Data
Reads from both DHT22 sensor and Ecobee, sends to Kafka
"""

import time
import json
from datetime import datetime
from kafka import KafkaProducer
import board
import adafruit_dht
import requests
import os

# Configuration
KAFKA_BROKER = "localhost:9092"
KAFKA_TOPIC = "temperature-readings"
HOME_ASSISTANT_URL = os.getenv("HOME_ASSISTANT_URL", "http://10.20.27.40:8123")
HOME_ASSISTANT_TOKEN = os.getenv("HOME_ASSISTANT_TOKEN")
DHT_PIN = board.D4

# Initialize Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=[KAFKA_BROKER],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def read_dht22():
    """Read from DHT22 sensor"""
    dht_device = adafruit_dht.DHT22(DHT_PIN, use_pulseio=False)
    
    try:
        temperature_c = dht_device.temperature
        humidity = dht_device.humidity
        
        if temperature_c is not None and humidity is not None:
            reading = {
                "timestamp": datetime.now().isoformat(),
                "sensor_id": "raspberry_pi_dht22",
                "location": "bird_cage_window_area",
                "temperature_celsius": round(temperature_c, 2),
                "temperature_fahrenheit": round(temperature_c * 9/5 + 32, 2),
                "humidity": round(humidity, 2),
                "source": "DHT22",
                "device": "raspberry_pi"
            }
            return reading
    except RuntimeError as e:
        print(f"DHT22 Error: {e}")
        return None
    except Exception as e:
        print(f"DHT22 Unexpected error: {e}")
        return None
    finally:
        dht_device.exit()
    
    return None

def read_ecobee():
    """Read from Ecobee via Home Assistant"""
    headers = {
        "Authorization": f"Bearer {HOME_ASSISTANT_TOKEN}",
        "Content-Type": "application/json"
    }
    
    try:
        # Get temperature
        temp_response = requests.get(
            f"{HOME_ASSISTANT_URL}/api/states/sensor.my_ecobee_current_temperature",
            headers=headers,
            timeout=10
        )
        temp_data = temp_response.json()
        
        # Get humidity
        humidity_response = requests.get(
            f"{HOME_ASSISTANT_URL}/api/states/sensor.my_ecobee_current_humidity",
            headers=headers,
            timeout=10
        )
        humidity_data = humidity_response.json()
        
        # Get HVAC status
        hvac_response = requests.get(
            f"{HOME_ASSISTANT_URL}/api/states/climate.my_ecobee",
            headers=headers,
            timeout=10
        )
        hvac_data = hvac_response.json()
        
        reading = {
            "timestamp": datetime.now().isoformat(),
            "sensor_id": "ecobee_thermostat",
            "location": "whole_house",
            "temperature_fahrenheit": float(temp_data['state']),
            "temperature_celsius": round((float(temp_data['state']) - 32) * 5/9, 2),
            "humidity": float(humidity_data['state']),
            "hvac_mode": hvac_data['state'],
            "hvac_action": hvac_data['attributes']['hvac_action'],
            "target_temperature": hvac_data['attributes']['temperature'],
            "source": "Ecobee",
            "device": "smart_thermostat"
        }
        
        return reading
        
    except Exception as e:
        print(f"Ecobee Error: {e}")
        return None

def send_to_kafka(data):
    """Send data to Kafka topic"""
    try:
        future = producer.send(KAFKA_TOPIC, value=data)
        record_metadata = future.get(timeout=10)
        print(f"✓ Sent to Kafka - Topic: {record_metadata.topic}, Partition: {record_metadata.partition}, Offset: {record_metadata.offset}")
        return True
    except Exception as e:
        print(f"✗ Kafka Error: {e}")
        return False

def main():
    print("=" * 70)
    print("🚀 Starting Temperature Streaming to Kafka")
    print(f"📍 Topic: {KAFKA_TOPIC}")
    print(f"🔗 Broker: {KAFKA_BROKER}")
    print("=" * 70)
    
    reading_count = 0
    
    try:
        while True:
            reading_count += 1
            print(f"\n📊 Reading #{reading_count} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print("-" * 70)
            
            # Read DHT22 sensor
            dht_data = read_dht22()
            if dht_data:
                print(f"🍓 DHT22: {dht_data['temperature_fahrenheit']}°F, {dht_data['humidity']}% humidity")
                send_to_kafka(dht_data)
            else:
                print("🍓 DHT22: Read failed")
            
            time.sleep(2)  # Small delay between sensors
            
            # Read Ecobee
            ecobee_data = read_ecobee()
            if ecobee_data:
                print(f"🌡️  Ecobee: {ecobee_data['temperature_fahrenheit']}°F, {ecobee_data['humidity']}% humidity, HVAC: {ecobee_data['hvac_action']}")
                send_to_kafka(ecobee_data)
            else:
                print("🌡️  Ecobee: Read failed")
            
            # Wait before next reading cycle (every 15 seconds total)
            print(f"\n⏳ Waiting 15 seconds before next reading...")
            time.sleep(13)
            
    except KeyboardInterrupt:
        print("\n\n🛑 Stopping stream...")
        producer.flush()
        producer.close()
        print("✓ Kafka producer closed")
        print("=" * 70)

if __name__ == "__main__":
    if not HOME_ASSISTANT_TOKEN:
        print("ERROR: HOME_ASSISTANT_TOKEN environment variable not set!")
        exit(1)
    
    main()