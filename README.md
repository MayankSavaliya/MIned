# 🚚 Smart Route Optimization System

> 🌟 Intelligent delivery route optimization using advanced algorithms and real-time mapping 

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)
[![Pandas](https://img.shields.io/badge/Pandas-2.1.4-orange.svg)](https://pandas.pydata.org/)
[![NumPy](https://img.shields.io/badge/NumPy-1.26.2-lightblue.svg)](https://numpy.org/)
[![Folium](https://img.shields.io/badge/Folium-0.15.1-brightgreen.svg)](https://python-visualization.github.io/folium/)
[![OpenPyXL](https://img.shields.io/badge/OpenPyXL-3.1.2-blue.svg)](https://openpyxl.readthedocs.io/)

## 🌐 Live Demo of the Project

Try out the live application: [SwiftRoute Demo](https://swiftroute.onrender.com)

[![Deployment Status](https://img.shields.io/website?url=https%3A%2F%2Fswiftroute.onrender.com&logo=render&label=SwiftRoute)](https://swiftroute.onrender.com)

Deployed on [Render](https://render.com/) with automatic deployments from GitHub.

<div align="center">
  <img src="https://skillicons.dev/icons?i=python,flask,git,vscode" alt="Tech Stack" />
</div>

## 🎯 Problem Statement

The project addresses several key challenges in last-mile delivery optimization:

🔹 **Route Efficiency**: Optimize delivery routes for multiple vehicle types while minimizing travel distance and time

🔹 **Vehicle Constraints**: Handle different vehicle capacities and operational limitations:
  - Distance radius restrictions
  - Vehicle capacity limits
  - Time window constraints

🔹 **Real-time Processing**: Process and optimize routes in real-time without local storage dependencies

🔹 **Multi-Vehicle Strategy**: Efficiently assign deliveries across different vehicle types:
  - 3-Wheelers for narrow streets and short distances
  - Electric vehicles for eco-friendly medium-range deliveries
  - Standard 4-wheelers for longer routes and larger capacities

🔹 **Business Goals**:
  - Maximize vehicle utilization
  - Minimize delivery time
  - Optimize resource allocation
  - Reduce operational costs

## ✨ Features

🔄 Upload Excel file with shipment data  
📊 Select delivery timeslots for route planning  
🛣️ Optimized route generation for different vehicle types  
🗺️ Interactive map visualization of routes  
⚖️ Vehicle capacity and distance constraints handling  
⚡ Real-time route optimization

## 🚗 Vehicle Types and Constraints

### 🛵 3-Wheeler (3W)
- 📦 Count: 50
- 🔢 Capacity: 5 shipments
- 📏 Maximum radius: 15 km

### 🚙 4-Wheeler EV (4W-EV)
- 📦 Count: 25
- 🔢 Capacity: 8 shipments
- 📏 Maximum radius: 20 km

### 🚛 4-Wheeler (4W)
- 📦 Count: Unlimited
- 🔢 Capacity: 25 shipments
- 📏 Maximum radius: Unlimited

## 🚀 Installation

1. Clone the repository:
```bash
git clone https://github.com/MayankSavaliya/SwiftRoute-MINeD.git
cd SwiftRoute-MINeD
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## 📱 Usage

1. Start the application:
```bash
python app.py
```

2. Open your browser and navigate to:
```
http://localhost:5000
```

3. 📤 Upload given Excel file with shipment data
4. 🕒 Select a timeslot
5. 📋 View optimized routes and vehicle assignments
6. 🗺️ Click on routes to view interactive maps

## 🛠️ Technical Details

- 🎯 Built with Flask
- 📊 Uses Pandas for data processing
- 🧮 Implements custom route optimization algorithm
- 🗺️ Interactive maps using Folium
- 💾 In-memory data processing without local storage

## 📌 Requirements

| Technology | Version |
|------------|---------|
| 🐍 Python | 3.8+ |
| 🌶️ Flask | 3.0.0 |
| 🐼 Pandas | 2.1.4 |
| 🔢 NumPy | 1.26.2 |
| 🗺️ Folium | 0.15.1 |
