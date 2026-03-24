import os
import numpy as np
import pandas as pd


def simulate_deliveries(n_deliveries=200, random_state=42):
    np.random.seed(random_state)

    cities = [
        {"city": "Sao Paulo", "state": "SP", "center_lat": -23.5505, "center_lon": -46.6333},
        {"city": "Rio de Janeiro", "state": "RJ", "center_lat": -22.9068, "center_lon": -43.1729},
        {"city": "Belo Horizonte", "state": "MG", "center_lat": -19.9167, "center_lon": -43.9345},
        {"city": "Vitoria", "state": "ES", "center_lat": -20.3155, "center_lon": -40.3128},
        {"city": "Curitiba", "state": "PR", "center_lat": -25.4284, "center_lon": -49.2733},
    ]

    traffic_levels = ["Low", "Medium", "High"]
    vehicle_types = ["Motorcycle", "Van", "Truck"]
    delivery_windows = ["Morning", "Afternoon", "Evening"]
    status_options = ["On Time", "Delayed"]

    traffic_weights = [0.3, 0.45, 0.25]
    vehicle_weights = [0.35, 0.45, 0.20]
    window_weights = [0.4, 0.35, 0.25]

    rows = []

    for delivery_id in range(1, n_deliveries + 1):
        city_data = cities[np.random.randint(0, len(cities))]

        city = city_data["city"]
        state = city_data["state"]

        latitude = city_data["center_lat"] + np.random.normal(0, 0.08)
        longitude = city_data["center_lon"] + np.random.normal(0, 0.08)

        distance_km = max(1, np.random.normal(18, 8))
        traffic_level = np.random.choice(traffic_levels, p=traffic_weights)
        vehicle_type = np.random.choice(vehicle_types, p=vehicle_weights)
        delivery_window = np.random.choice(delivery_windows, p=window_weights)

        package_weight_kg = max(0.2, np.random.normal(8, 4))
        fuel_cost_brl = round(np.random.uniform(5.4, 6.5), 2)

        traffic_multiplier = {"Low": 1.0, "Medium": 1.25, "High": 1.6}[traffic_level]
        vehicle_speed = {"Motorcycle": 38, "Van": 32, "Truck": 26}[vehicle_type]
        vehicle_cost_per_km = {"Motorcycle": 1.2, "Van": 2.1, "Truck": 3.4}[vehicle_type]

        estimated_time_min = (distance_km / vehicle_speed) * 60 * traffic_multiplier
        estimated_time_min += np.random.normal(0, 6)
        estimated_time_min = max(10, estimated_time_min)

        original_cost_brl = (
            12
            + (distance_km * vehicle_cost_per_km)
            + (estimated_time_min * 0.18)
            + (package_weight_kg * 0.35)
        )

        delay_score = 0
        if traffic_level == "High":
            delay_score += 2
        elif traffic_level == "Medium":
            delay_score += 1

        if distance_km > 25:
            delay_score += 2
        elif distance_km > 15:
            delay_score += 1

        if delivery_window == "Evening":
            delay_score += 1

        if vehicle_type == "Truck":
            delay_score += 1

        delayed = 1 if delay_score + np.random.randint(0, 3) >= 4 else 0
        delivery_status = status_options[1] if delayed else status_options[0]

        rows.append(
            {
                "delivery_id": delivery_id,
                "city": city,
                "state": state,
                "latitude": round(latitude, 6),
                "longitude": round(longitude, 6),
                "distance_km": round(distance_km, 2),
                "estimated_time_min": round(estimated_time_min, 2),
                "traffic_level": traffic_level,
                "vehicle_type": vehicle_type,
                "delivery_window": delivery_window,
                "package_weight_kg": round(package_weight_kg, 2),
                "fuel_cost_brl": fuel_cost_brl,
                "delivery_status": delivery_status,
                "delay_risk": delayed,
                "original_cost_brl": round(original_cost_brl, 2),
            }
        )

    df = pd.DataFrame(rows)
    return df


def main():
    output_dir = "data/raw"
    os.makedirs(output_dir, exist_ok=True)

    df = simulate_deliveries(n_deliveries=200, random_state=42)
    output_path = os.path.join(output_dir, "deliveries_simulated.csv")
    df.to_csv(output_path, index=False)

    print("Dataset created successfully.")
    print(f"File saved to: {output_path}")
    print("\nPreview:")
    print(df.head())


if __name__ == "__main__":
    main()
