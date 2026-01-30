# Bird Temperature Monitoring - IoT Data Pipeline

## 🐦 Project Overview

An end-to-end IoT data engineering solution that monitors temperature at my bird's cage location (near window) and compares it with whole-house temperature from Ecobee thermostat.

### The Problem
My wife and I keep our bird's cage by the window for natural light, but worry about temperature fluctuations. We often move the cage inside without knowing if it's actually necessary. This project uses real-time data to make informed decisions.

## 🏗️ Architecture

**Tech Stack:**
- Edge: Raspberry Pi 5 + DHT22 sensor
- Streaming: Apache Kafka
- Processing: Azure Databricks (PySpark)
- Storage: Azure Data Lake Gen2 (Delta Lake)
- Integration: Home Assistant (Ecobee via HomeKit)

**Data Flow:**
```
Raspberry Pi Sensor → Kafka → Azure Databricks → ADLS Gen2 (Bronze/Silver/Gold) → Analytics
Ecobee (Home Assistant) ↗
```

## 📊 Medallion Architecture

- **Bronze:** Raw sensor data
- **Silver:** Validated, enriched data
- **Gold:** Aggregated analytics & comparisons

## 🚀 Status

✅ Phase 1: Infrastructure setup complete
🚧 Phase 2: Hardware integration (sensor arriving Jan 31)
📅 Phase 3: Streaming pipeline
📅 Phase 4: Real-time analytics

## 👨‍💻 Author

Pradeep Poonati - Data Engineer
- GitHub: [@pradeeppoonati-git](https://github.com/pradeeppoonati-git)
- Email: pradeep.poonati@gmail.com
