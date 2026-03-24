import os
import math
import pandas as pd
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp


INPUT_DATA_PATH = "data/processed/deliveries_cleaned.csv"
METRICS_DIR = "outputs/metrics"
OUTPUT_ROUTE_PATH = os.path.join(METRICS_DIR, "optimized_route.csv")
OUTPUT_COMPARISON_PATH = os.path.join(METRICS_DIR, "route_comparison.csv")


def ensure_directories():
    os.makedirs(METRICS_DIR, exist_ok=True)


def load_data(file_path=INPUT_DATA_PATH):
    df = pd.read_csv(file_path)
    return df


def haversine_distance(lat1, lon1, lat2, lon2):
    r = 6371  # Earth radius in km

    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return r * c


def build_distance_matrix(locations):
    matrix = []

    for from_node in locations:
        row = []
        for to_node in locations:
            distance = haversine_distance(
                from_node["latitude"],
                from_node["longitude"],
                to_node["latitude"],
                to_node["longitude"],
            )
            row.append(int(distance * 1000))  # meters as integer
        matrix.append(row)

    return matrix


def create_data_model(df, sample_size=20):
    df_sample = df.head(sample_size).copy()

    depot_lat = df_sample["latitude"].mean()
    depot_lon = df_sample["longitude"].mean()

    depot = {
        "delivery_id": 0,
        "city": "Depot",
        "state": "N/A",
        "latitude": depot_lat,
        "longitude": depot_lon,
    }

    locations = [depot] + df_sample[
        ["delivery_id", "city", "state", "latitude", "longitude"]
    ].to_dict(orient="records")

    data = {
        "distance_matrix": build_distance_matrix(locations),
        "num_vehicles": 1,
        "depot": 0,
        "locations": locations,
    }

    return data, df_sample


def solve_route(data):
    manager = pywrapcp.RoutingIndexManager(
        len(data["distance_matrix"]),
        data["num_vehicles"],
        data["depot"],
    )

    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data["distance_matrix"][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    )

    solution = routing.SolveWithParameters(search_parameters)

    if solution is None:
        return None, None, None

    index = routing.Start(0)
    route_nodes = []
    route_distance = 0

    while not routing.IsEnd(index):
        node_index = manager.IndexToNode(index)
        route_nodes.append(node_index)

        previous_index = index
        index = solution.Value(routing.NextVar(index))
        route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)

    route_nodes.append(manager.IndexToNode(index))

    return route_nodes, route_distance / 1000, data["locations"]


def calculate_original_route_distance(locations):
    total_distance = 0

    for i in range(len(locations) - 1):
        total_distance += haversine_distance(
            locations[i]["latitude"],
            locations[i]["longitude"],
            locations[i + 1]["latitude"],
            locations[i + 1]["longitude"],
        )

    return total_distance


def save_route_results(route_nodes, locations, optimized_distance, original_distance):
    route_rows = []

    for sequence, node in enumerate(route_nodes):
        location = locations[node]
        route_rows.append(
            {
                "sequence": sequence,
                "delivery_id": location["delivery_id"],
                "city": location["city"],
                "state": location["state"],
                "latitude": location["latitude"],
                "longitude": location["longitude"],
            }
        )

    route_df = pd.DataFrame(route_rows)
    route_df.to_csv(OUTPUT_ROUTE_PATH, index=False)

    comparison_df = pd.DataFrame(
        [
            {
                "original_route_distance_km": round(original_distance, 2),
                "optimized_route_distance_km": round(optimized_distance, 2),
                "distance_reduction_km": round(original_distance - optimized_distance, 2),
                "distance_reduction_percent": round(
                    ((original_distance - optimized_distance) / original_distance) * 100, 2
                ) if original_distance > 0 else 0,
            }
        ]
    )
    comparison_df.to_csv(OUTPUT_COMPARISON_PATH, index=False)

    return route_df, comparison_df


def run_optimization():
    ensure_directories()

    df = load_data()
    data, df_sample = create_data_model(df, sample_size=20)

    route_nodes, optimized_distance, locations = solve_route(data)

    if route_nodes is None:
        print("No solution found.")
        return

    original_locations = data["locations"]
    original_distance = calculate_original_route_distance(original_locations)

    route_df, comparison_df = save_route_results(
        route_nodes,
        locations,
        optimized_distance,
        original_distance,
    )

    print("Route optimization completed successfully.")
    print(f"Optimized route saved to: {OUTPUT_ROUTE_PATH}")
    print(f"Comparison metrics saved to: {OUTPUT_COMPARISON_PATH}")
    print("\nOptimized route preview:")
    print(route_df.head().to_string(index=False))
    print("\nComparison metrics:")
    print(comparison_df.to_string(index=False))


if __name__ == "__main__":
    run_optimization()
