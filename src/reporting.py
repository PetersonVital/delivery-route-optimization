import os
import pandas as pd
import matplotlib.pyplot as plt
from chart_utils import create_figure, format_axis, annotate_bars, save_figure


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

    fig, ax = create_figure(figsize=(8, 5))
    bars = ax.bar(labels, values, width=0.6)

    format_axis(
        ax,
        title="Original vs Optimized Route Distance",
        subtitle="Comparison of route length before and after optimization",
        ylabel="Distance (km)",
    )

    annotate_bars(ax, fmt="{:.1f}", suffix=" km")
    save_figure(fig, DISTANCE_COMPARISON_FIGURE)


def plot_distance_reduction(route_comparison_df):
    reduction_percent = route_comparison_df.loc[0, "distance_reduction_percent"]

    fig, ax = create_figure(figsize=(6, 5))
    bars = ax.bar(["Distance Reduction"], [reduction_percent], width=0.55)

    format_axis(
        ax,
        title="Distance Reduction Percentage",
        subtitle="Relative improvement after route optimization",
        ylabel="Reduction (%)",
        y_as_percent=True,
    )

    annotate_bars(ax, fmt="{:.1f}", suffix="%")
    save_figure(fig, DISTANCE_REDUCTION_FIGURE)


def plot_overall_delay_rate(summary_metrics_df):
    delay_rate = summary_metrics_df.loc[0, "delay_rate_percent"]

    fig, ax = create_figure(figsize=(6, 5))
    bars = ax.bar(["Delay Rate"], [delay_rate], width=0.55)

    format_axis(
        ax,
        title="Overall Delay Rate",
        subtitle="Share of deliveries classified as delayed in the simulated operation",
        ylabel="Delay Rate (%)",
        y_as_percent=True,
    )

    annotate_bars(ax, fmt="{:.1f}", suffix="%")
    save_figure(fig, DELAY_RATE_FIGURE)


def plot_average_cost_by_vehicle(processed_df):
    avg_cost = (
        processed_df.groupby("vehicle_type")["original_cost_brl"]
        .mean()
        .sort_values(ascending=True)
        .reset_index()
    )

    fig, ax = create_figure(figsize=(8, 5))
    bars = ax.bar(avg_cost["vehicle_type"], avg_cost["original_cost_brl"], width=0.6)

    format_axis(
        ax,
        title="Average Cost by Vehicle Type",
        subtitle="Average operational cost segmented by transportation mode",
        xlabel="Vehicle Type",
        ylabel="Average Cost (BRL)",
        y_as_currency=True,
    )

    annotate_bars(ax, fmt="{:.1f}", prefix="R$ ")
    save_figure(fig, AVG_COST_BY_VEHICLE_FIGURE)


def plot_deliveries_by_city(city_summary_df):
    plot_df = city_summary_df.sort_values("deliveries", ascending=False).copy()
    plot_df["city_label"] = plot_df["city"] + " - " + plot_df["state"]

    fig, ax = create_figure(figsize=(10, 6))
    bars = ax.bar(plot_df["city_label"], plot_df["deliveries"], width=0.65)

    format_axis(
        ax,
        title="Number of Deliveries by City",
        subtitle="Distribution of simulated deliveries across covered cities",
        xlabel="City",
        ylabel="Deliveries",
        rotate_xticks=35,
        integer_y=True,
    )

    annotate_bars(ax, fmt="{:.0f}")
    save_figure(fig, DELIVERIES_BY_CITY_FIGURE)


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
