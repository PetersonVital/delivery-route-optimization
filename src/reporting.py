import os
import pandas as pd
import matplotlib.pyplot as plt


PROCESSED_DATA_PATH = "data/processed/deliveries_cleaned.csv"
ROUTE_COMPARISON_PATH = "outputs/metrics/route_comparison.csv"
CITY_SUMMARY_PATH = "outputs/metrics/city_summary.csv"
SUMMARY_METRICS_PATH = "outputs/metrics/summary_metrics.csv"

FIGURES_DIR = "outputs/figures"
METRICS_DIR = "outputs/metrics"

DISTANCE_COMPARISON_FIGURE = os.path.join(FIGURES_DIR, "route_distance_comparison.png")
DISTANCE_REDUCTION_FIGURE = os.path.join(FIGURES_DIR, "distance_reduction_percent.png")
DELAY_RATE_FIGURE = os.path.join(FIGURES_DIR, "overall_delay_rate.png")
AVG_COST_BY_VEHICLE_FIGURE = os.path.join(FIGURES_DIR, "report_avg_cost_by_vehicle.png")
DELIVERIES_BY_CITY_FIGURE = os.path.join(FIGURES_DIR, "deliveries_by_city.png")
FINAL_REPORT_METRICS_PATH = os.path.join(METRICS_DIR, "final_report_metrics.csv")


def ensure_directories():
    os.makedirs(FIGURES_DIR, exist_ok=True)
    os.makedirs(METRICS_DIR, exist_ok=True)


def load_data():
    processed_df = pd.read_csv(PROCESSED_DATA_PATH)
    route_comparison_df = pd.read_csv(ROUTE_COMPARISON_PATH)
    city_summary_df = pd.read_csv(CITY_SUMMARY_PATH)
    summary_metrics_df = pd.read_csv(SUMMARY_METRICS_PATH)

    return processed_df, route_comparison_df, city_summary_df, summary_metrics_df


def plot_route_distance_comparison(route_comparison_df):
    original_distance = route_comparison_df.loc[0, "original_route_distance_km"]
    optimized_distance = route_comparison_df.loc[0, "optimized_route_distance_km"]

    labels = ["Original Route", "Optimized Route"]
    values = [original_distance, optimized_distance]

    plt.figure(figsize=(8, 5))
    plt.bar(labels, values)
    plt.title("Original vs Optimized Route Distance")
    plt.ylabel("Distance (km)")
    plt.tight_layout()
    plt.savefig(DISTANCE_COMPARISON_FIGURE)
    plt.close()


def plot_distance_reduction(route_comparison_df):
    reduction_percent = route_comparison_df.loc[0, "distance_reduction_percent"]

    plt.figure(figsize=(6, 5))
    plt.bar(["Distance Reduction"], [reduction_percent])
    plt.title("Distance Reduction Percentage")
    plt.ylabel("Reduction (%)")
    plt.tight_layout()
    plt.savefig(DISTANCE_REDUCTION_FIGURE)
    plt.close()


def plot_overall_delay_rate(summary_metrics_df):
    delay_rate = summary_metrics_df.loc[0, "delay_rate_percent"]

    plt.figure(figsize=(6, 5))
    plt.bar(["Delay Rate"], [delay_rate])
    plt.title("Overall Delay Rate")
    plt.ylabel("Rate (%)")
    plt.tight_layout()
    plt.savefig(DELAY_RATE_FIGURE)
    plt.close()


def plot_average_cost_by_vehicle(processed_df):
    avg_cost = processed_df.groupby("vehicle_type")["original_cost_brl"].mean().sort_values()

    plt.figure(figsize=(8, 5))
    plt.bar(avg_cost.index, avg_cost.values)
    plt.title("Average Cost by Vehicle Type")
    plt.xlabel("Vehicle Type")
    plt.ylabel("Average Cost (BRL)")
    plt.tight_layout()
    plt.savefig(AVG_COST_BY_VEHICLE_FIGURE)
    plt.close()


def plot_deliveries_by_city(city_summary_df):
    city_labels = city_summary_df["city"] + " - " + city_summary_df["state"]
    deliveries = city_summary_df["deliveries"]

    plt.figure(figsize=(10, 6))
    plt.bar(city_labels, deliveries)
    plt.title("Number of Deliveries by City")
    plt.xlabel("City")
    plt.ylabel("Deliveries")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(DELIVERIES_BY_CITY_FIGURE)
    plt.close()


def build_final_report_metrics(processed_df, route_comparison_df, summary_metrics_df):
    final_metrics = {
        "total_deliveries": int(summary_metrics_df.loc[0, "total_deliveries"]),
        "average_distance_km": round(summary_metrics_df.loc[0, "average_distance_km"], 2),
        "average_estimated_time_min": round(summary_metrics_df.loc[0, "average_estimated_time_min"], 2),
        "average_original_cost_brl": round(summary_metrics_df.loc[0, "average_original_cost_brl"], 2),
        "total_estimated_cost_brl": round(summary_metrics_df.loc[0, "total_estimated_cost_brl"], 2),
        "delay_rate_percent": round(summary_metrics_df.loc[0, "delay_rate_percent"], 2),
        "original_route_distance_km": round(route_comparison_df.loc[0, "original_route_distance_km"], 2),
        "optimized_route_distance_km": round(route_comparison_df.loc[0, "optimized_route_distance_km"], 2),
        "distance_reduction_km": round(route_comparison_df.loc[0, "distance_reduction_km"], 2),
        "distance_reduction_percent": round(route_comparison_df.loc[0, "distance_reduction_percent"], 2),
    }

    final_metrics_df = pd.DataFrame([final_metrics])
    final_metrics_df.to_csv(FINAL_REPORT_METRICS_PATH, index=False)

    return final_metrics_df


def run_reporting():
    ensure_directories()

    processed_df, route_comparison_df, city_summary_df, summary_metrics_df = load_data()

    plot_route_distance_comparison(route_comparison_df)
    plot_distance_reduction(route_comparison_df)
    plot_overall_delay_rate(summary_metrics_df)
    plot_average_cost_by_vehicle(processed_df)
    plot_deliveries_by_city(city_summary_df)

    final_metrics_df = build_final_report_metrics(
        processed_df,
        route_comparison_df,
        summary_metrics_df,
    )

    print("Reporting completed successfully.")
    print(f"Final report metrics saved to: {FINAL_REPORT_METRICS_PATH}")
    print("\nFinal report metrics:")
    print(final_metrics_df.to_string(index=False))
    print("\nGenerated figures:")
    print(f"- {DISTANCE_COMPARISON_FIGURE}")
    print(f"- {DISTANCE_REDUCTION_FIGURE}")
    print(f"- {DELAY_RATE_FIGURE}")
    print(f"- {AVG_COST_BY_VEHICLE_FIGURE}")
    print(f"- {DELIVERIES_BY_CITY_FIGURE}")


if __name__ == "__main__":
    run_reporting()
