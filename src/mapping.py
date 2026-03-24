import os
import pandas as pd
import folium


PROCESSED_DATA_PATH = "data/processed/deliveries_cleaned.csv"
OPTIMIZED_ROUTE_PATH = "outputs/metrics/optimized_route.csv"
MAPS_DIR = "outputs/maps"

ORIGINAL_MAP_PATH = os.path.join(MAPS_DIR, "route_before.html")
OPTIMIZED_MAP_PATH = os.path.join(MAPS_DIR, "route_after.html")


def ensure_directories():
    os.makedirs(MAPS_DIR, exist_ok=True)


def load_processed_data():
    return pd.read_csv(PROCESSED_DATA_PATH)


def load_optimized_route():
    return pd.read_csv(OPTIMIZED_ROUTE_PATH)


def build_original_route(df, sample_size=20):
    df_sample = df.head(sample_size).copy()

    depot_lat = df_sample["latitude"].mean()
    depot_lon = df_sample["longitude"].mean()

    depot_row = pd.DataFrame(
        [
            {
                "sequence": 0,
                "delivery_id": 0,
                "city": "Depot",
                "state": "N/A",
                "latitude": depot_lat,
                "longitude": depot_lon,
            }
        ]
    )

    route_df = df_sample[
        ["delivery_id", "city", "state", "latitude", "longitude"]
    ].copy()
    route_df.insert(0, "sequence", range(1, len(route_df) + 1))

    route_df = pd.concat([depot_row, route_df], ignore_index=True)

    final_depot = depot_row.copy()
    final_depot["sequence"] = len(route_df)

    route_df = pd.concat([route_df, final_depot], ignore_index=True)

    return route_df


def create_map(route_df, output_path, map_title):
    center_lat = route_df["latitude"].mean()
    center_lon = route_df["longitude"].mean()

    route_map = folium.Map(location=[center_lat, center_lon], zoom_start=6)

    coordinates = []

    for _, row in route_df.iterrows():
        lat = row["latitude"]
        lon = row["longitude"]
        coordinates.append([lat, lon])

        if row["delivery_id"] == 0:
            popup_text = f"""
            <b>{map_title}</b><br>
            Sequence: {row['sequence']}<br>
            Location: Depot
            """
            tooltip_text = "Depot"
            marker_color = "red"
            icon_name = "home"
        else:
            popup_text = f"""
            <b>{map_title}</b><br>
            Sequence: {row['sequence']}<br>
            Delivery ID: {row['delivery_id']}<br>
            City: {row['city']}<br>
            State: {row['state']}
            """
            tooltip_text = f"Stop {row['sequence']}: {row['city']}"
            marker_color = "blue"
            icon_name = "info-sign"

        folium.Marker(
            location=[lat, lon],
            popup=folium.Popup(popup_text, max_width=250),
            tooltip=tooltip_text,
            icon=folium.Icon(color=marker_color, icon=icon_name),
        ).add_to(route_map)

    folium.PolyLine(
        locations=coordinates,
        weight=4,
        opacity=0.8,
    ).add_to(route_map)

    route_map.save(output_path)


def run_mapping():
    ensure_directories()

    processed_df = load_processed_data()
    optimized_route_df = load_optimized_route()

    original_route_df = build_original_route(processed_df, sample_size=20)

    create_map(
        route_df=original_route_df,
        output_path=ORIGINAL_MAP_PATH,
        map_title="Original Route",
    )

    create_map(
        route_df=optimized_route_df,
        output_path=OPTIMIZED_MAP_PATH,
        map_title="Optimized Route",
    )

    print("Maps generated successfully.")
    print(f"Original route map saved to: {ORIGINAL_MAP_PATH}")
    print(f"Optimized route map saved to: {OPTIMIZED_MAP_PATH}")


if __name__ == "__main__":
    run_mapping()
