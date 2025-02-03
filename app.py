from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import numpy as np
import math
import folium

app = Flask(__name__)

# Cache to store data in memory
cache = {
    'excel_data': None,
    'assignments': {}
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file:
            # Read Excel directly into memory
            cache['excel_data'] = pd.read_excel(file, sheet_name="Shipments_Data")
            return redirect(url_for('select_timeslot'))
    return render_template('upload.html')

@app.route('/select_timeslot', methods=['GET', 'POST'])
def select_timeslot():
    if request.method == 'POST':
        timeslot = request.form['timeslot']
        return redirect(url_for('show_trips', timeslot=timeslot))
    return render_template('select_timeslot.html')

@app.route('/trips/<timeslot>')
def show_trips(timeslot):
    shipments_df = cache['excel_data']
    if shipments_df is None:
        return redirect(url_for('upload_file'))

    store_lat, store_lon = shipments_df.iloc[0]['Latitude'], shipments_df.iloc[0]['Longitude']
    df_timeslot = shipments_df[shipments_df['Delivery Timeslot'] == timeslot]
    df_timeslot_with_shop = insert_shop_location(df_timeslot, store_lat, store_lon)
    dist_matrix = calculate_distance_matrix_with_shop(df_timeslot_with_shop)
    
    headers = ['Shop'] + df_timeslot['Shipment ID'].astype(str).tolist()
    
    vehicles = [
        {"type": "3W", "count": 50, "capacity": 5, "max_radius": 15, "max_trip_time": 240},
        {"type": "4W-EV", "count": 25, "capacity": 8, "max_radius": 20, "max_trip_time": 300},
        {"type": "4W", "count": float('inf'), "capacity": 25, "max_radius": float('inf'), "max_trip_time": 480}
    ]

    assignments = assign_shipments(headers, dist_matrix.tolist(), vehicles)
    cache['assignments'][timeslot] = assignments

    return render_template('trips.html', assignments=assignments, timeslot=timeslot)

@app.route('/map/<timeslot>/<int:index>')
def show_map(timeslot, index):
    shipments_df = cache['excel_data']
    assignments = cache['assignments'].get(timeslot, [])
    
    if shipments_df is None or not assignments:
        return redirect(url_for('upload_file'))
    
    route = assignments[index]['Route'].split(' -> ')
    map_html = generate_map(route, shipments_df)
    return render_template('map.html', map_html=map_html, timeslot=timeslot)

# Helper functions (unchanged)
def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0  # Radius of the Earth in kilometers
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance

def insert_shop_location(df, store_lat, store_lon):
    shop_data = pd.DataFrame(
        {'Shipment ID': ['Shop'], 'Latitude': [store_lat], 'Longitude': [store_lon], 'Delivery Timeslot': ['Shop']})
    df_with_shop = pd.concat([shop_data, df], ignore_index=True)
    return df_with_shop

def calculate_distance_matrix_with_shop(df):
    n = len(df)
    dist_matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(i, n):
            lat1, lon1 = df.iloc[i]['Latitude'], df.iloc[i]['Longitude']
            lat2, lon2 = df.iloc[j]['Latitude'], df.iloc[j]['Longitude']
            dist = haversine(lat1, lon1, lat2, lon2)
            dist_matrix[i, j] = dist_matrix[j, i] = dist
    return dist_matrix

def assign_shipments(headers, distance_matrix, vehicles):
    shipments = headers[1:]  # Exclude the shop from shipments
    n = len(shipments)
    assigned = [False] * n
    vehicle_assignments = []

    # Track the maximum distance for 4W vehicles
    max_4w_distance = 0

    for vehicle in vehicles:
        count = vehicle["count"]
        if count == float('inf'):
            count = n

        for _ in range(count):
            current_capacity = 0
            current_distance = 0
            current_shipments = []
            last_location = 0  # Start at the shop (index 0)

            while current_capacity < vehicle["capacity"]:
                min_distance = float('inf')
                next_shipment = -1

                for i in range(n):
                    if not assigned[i]:
                        shipment_index = i + 1  # Skip the shop (index 0)
                        if shipment_index < len(distance_matrix) and last_location < len(
                                distance_matrix[shipment_index]):
                            if distance_matrix[last_location][shipment_index] < min_distance:
                                min_distance = distance_matrix[last_location][shipment_index]
                                next_shipment = i

                if next_shipment == -1:
                    break

                shipment_index = next_shipment + 1
                if shipment_index < len(distance_matrix) and last_location < len(distance_matrix[shipment_index]):
                    total_distance = current_distance + min_distance + distance_matrix[shipment_index][0]
                    if total_distance <= vehicle["max_radius"]:
                        current_distance += min_distance
                        current_capacity += 1
                        assigned[next_shipment] = True
                        current_shipments.append(shipments[next_shipment])
                        last_location = shipment_index
                    else:
                        break

            if current_shipments:
                total_distance = current_distance + distance_matrix[last_location][0]
                trip_time = (total_distance * 5) + (len(current_shipments) * 10)
                capacity_utilization = current_capacity / vehicle["capacity"]
                time_utilization = trip_time / vehicle["max_trip_time"]

                # Calculate distance utilization differently for 4W vehicles
                if vehicle["type"] == "4W":
                    # Update the maximum distance for 4W vehicles
                    if total_distance > max_4w_distance:
                        max_4w_distance = total_distance
                    distance_utilization = total_distance / max_4w_distance if max_4w_distance != 0 else 0
                else:
                    distance_utilization = total_distance / vehicle["max_radius"]

                # Ensure the route starts and ends with "Shop" and does not include "Shop" in between
                route = ["Shop"] + current_shipments + ["Shop"]

                # Remove duplicate "Shop" occurrences if any
                if route.count("Shop") > 2:
                    route = ["Shop"] + [x for x in route if x != "Shop"] + ["Shop"]

                route_string = " -> ".join(route)

                # Ensure "Shop" is not included in the "Shipments Delivered" column
                current_shipments = [x for x in current_shipments if x != "Shop"]
                shipments_delivered = ", ".join(current_shipments)  # Only shipment IDs, no "Shop"

                vehicle_assignments.append({
                    "Vehicle Type": vehicle["type"],
                    "Total Shipments": len(current_shipments),
                    "Shipments Delivered": shipments_delivered,  # Only shipment IDs, no "Shop"
                    "Route": route_string,  # Route includes "Shop" at start and end
                    "MST Distance": round(total_distance, 2),
                    "Trip Time": round(trip_time, 2),
                    "Capacity Utilization": round(capacity_utilization, 2),
                    "Time Utilization": round(time_utilization, 2),
                    "COV_UTI (Distance Utilization)": round(distance_utilization, 2)
                })

    return vehicle_assignments

def generate_map(route, shipments_df):
    m = folium.Map(location=[shipments_df.iloc[0]['Latitude'], shipments_df.iloc[0]['Longitude']], zoom_start=12)
    folium.Marker(
        location=[shipments_df.iloc[0]['Latitude'], shipments_df.iloc[0]['Longitude']],
        popup='Shop',
        icon=folium.Icon(color='red', icon='home')
    ).add_to(m)

    for i, shipment_id in enumerate(route[1:-1], 1):
        shipment = shipments_df[shipments_df['Shipment ID'] == int(shipment_id)].iloc[0]
        folium.Marker(
            location=[shipment['Latitude'], shipment['Longitude']],
            popup=f"Stop {i} (Order {shipment_id})",
            icon=folium.Icon(color='blue', icon='shopping-cart', prefix='fa'),
        ).add_to(m)

    route_coords = [[shipments_df.iloc[0]['Latitude'], shipments_df.iloc[0]['Longitude']]]
    for shipment_id in route[1:-1]:
        shipment = shipments_df[shipments_df['Shipment ID'] == int(shipment_id)].iloc[0]
        route_coords.append([shipment['Latitude'], shipment['Longitude']])
    route_coords.append([shipments_df.iloc[0]['Latitude'], shipments_df.iloc[0]['Longitude']])

    folium.PolyLine(
        locations=route_coords,
        weight=5,
        color='blue',
        opacity=0.8,
        tooltip='Route'
    ).add_to(m)

    return m._repr_html_()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
