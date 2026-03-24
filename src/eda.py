import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from chart_utils import create_figure, format_axis, annotate_bars, save_figure


RAW_DATA_PATH = "data/raw/deliveries_simulated.csv"
PROCESSED_DATA_PATH = "data/processed/deliveries_cleaned.csv"
FIGURES_DIR = "outputs/figures"
METRICS_DIR = "outputs/metrics"


def ensure_directories():
    os.makedirs("data/processed", exist_ok=True)
    os.makedirs(FIGURES_DIR, exist_ok=True)
    os.makedirs(METRICS_DIR, exist_ok=True)


def load_data(file_path=RAW_DATA_PATH):
    df = pd.read_csv(file_path)
    return df


def clean_data(df):
    df = df.copy()

    categorical_columns = [
        "city",
        "state",
        "traffic_level",
        "vehicle_type",
        "delivery_window",
        "delivery_status",
    ]

    for col in categorical_columns:
        df[col] = df[col].astype(str).str.strip()

    numeric_columns = [
        "latitude",
        "longitude",
        "distance_km",
        "estimated_time_min",
        "package_weight_kg",
        "fuel_cost_brl",
        "delay_risk",
        "original_cost_brl",
    ]

    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna().reset_index(drop=True)

    return df


def save_processed_data(df, output_path=PROCESSED_DATA_PATH):
    df.to_csv(output_path, index=False)


def create_summary_metrics(df):
    summary = {
        "total_deliveries": len(df),
        "average_distance_km": round(df["distance_km"].mean(), 2),
        "average_estimated_time_min": round(df["estimated_time_min"].mean(), 2),
        "average_package_weight_kg": round(df["package_weight_kg"].mean(), 2),
        "average_original_cost_brl": round(df["original_cost_brl"].mean(), 2),
        "total_estimated_cost_brl": round(df["original_cost_brl"].sum(), 2),
        "delay_rate_percent": round(df["delay_risk"].mean() * 100, 2),
    }

    summary_df = pd.DataFrame([summary])
    summary_df.to_csv(os.path.join(METRICS_DIR, "summary_metrics.csv"), index=False)

    city_summary = (
        df.groupby(["city", "state"], as_index=False)
        .agg(
            deliveries=("delivery_id", "count"),
            avg_distance_km=("distance_km", "mean"),
            avg_estimated_time_min=("estimated_time_min", "mean"),
            avg_cost_brl=("original_cost_brl", "mean"),
            delay_rate=("delay_risk", "mean"),
        )
    )

    city_summary["avg_distance_km"] = city_summary["avg_distance_km"].round(2)
    city_summary["avg_estimated_time_min"] = city_summary["avg_estimated_time_min"].round(2)
    city_summary["avg_cost_brl"] = city_summary["avg_cost_brl"].round(2)
    city_summary["delay_rate"] = (city_summary["delay_rate"] * 100).round(2)

    city_summary.to_csv(os.path.join(METRICS_DIR, "city_summary.csv"), index=False)

    return summary_df, city_summary


def plot_distance_distribution(df):
    fig, ax = create_figure(figsize=(10, 6))

    counts, bins, patches = ax.hist(
        df["distance_km"],
        bins=18,
        edgecolor="white",
        linewidth=1.0,
        alpha=0.9,
    )

    mean_value = df["distance_km"].mean()
    median_value = df["distance_km"].median()

    ax.axvline(mean_value, linestyle="--", linewidth=1.5, label=f"Mean: {mean_value:.1f} km")
    ax.axvline(median_value, linestyle=":", linewidth=1.8, label=f"Median: {median_value:.1f} km")

    format_axis(
        ax,
        title="Distribution of Delivery Distance",
        subtitle="Histogram with central tendency markers for route planning analysis",
        xlabel="Distance (km)",
        ylabel="Number of Deliveries",
        integer_y=True,
    )

    ax.legend(loc="upper right")
    save_figure(fig, os.path.join(FIGURES_DIR, "distance_distribution.png"))


def plot_average_time_by_traffic(df):
    avg_time = (
        df.groupby("traffic_level")["estimated_time_min"]
        .mean()
        .reindex(["Low", "Medium", "High"])
        .reset_index()
    )

    fig, ax = create_figure(figsize=(8, 5))
    bars = ax.bar(avg_time["traffic_level"], avg_time["estimated_time_min"], width=0.6)

    format_axis(
        ax,
        title="Average Estimated Time by Traffic Level",
        subtitle="Delivery time increases as traffic conditions worsen",
        xlabel="Traffic Level",
        ylabel="Estimated Time (minutes)",
    )

    annotate_bars(ax, fmt="{:.1f}", suffix=" min")
    save_figure(fig, os.path.join(FIGURES_DIR, "average_time_by_traffic.png"))


def plot_average_cost_by_vehicle(df):
    avg_cost = (
        df.groupby("vehicle_type")["original_cost_brl"]
        .mean()
        .sort_values(ascending=True)
        .reset_index()
    )

    fig, ax = create_figure(figsize=(8, 5))
    bars = ax.bar(avg_cost["vehicle_type"], avg_cost["original_cost_brl"], width=0.6)

    format_axis(
        ax,
        title="Average Cost by Vehicle Type",
        subtitle="Operational cost varies by transportation mode",
        xlabel="Vehicle Type",
        ylabel="Average Cost (BRL)",
        y_as_currency=True,
    )

    annotate_bars(ax, fmt="{:.1f}", prefix="R$ ")
    save_figure(fig, os.path.join(FIGURES_DIR, "average_cost_by_vehicle.png"))


def plot_delay_rate_by_traffic(df):
    delay_rate = (
        df.groupby("traffic_level")["delay_risk"]
        .mean()
        .reindex(["Low", "Medium", "High"])
        .mul(100)
        .reset_index()
    )

    fig, ax = create_figure(figsize=(8, 5))
    bars = ax.bar(delay_rate["traffic_level"], delay_rate["delay_risk"], width=0.6)

    format_axis(
        ax,
        title="Delay Rate by Traffic Level",
        subtitle="Higher traffic intensity is associated with higher delivery delay risk",
        xlabel="Traffic Level",
        ylabel="Delay Rate (%)",
        y_as_percent=True,
    )

    annotate_bars(ax, fmt="{:.1f}", suffix="%")
    save_figure(fig, os.path.join(FIGURES_DIR, "delay_rate_by_traffic.png"))


def plot_correlation_matrix(df):
    numeric_df = df[
        [
            "distance_km",
            "estimated_time_min",
            "package_weight_kg",
            "fuel_cost_brl",
            "delay_risk",
            "original_cost_brl",
        ]
    ]

    corr = numeric_df.corr()

    fig, ax = create_figure(figsize=(9, 7))
    im = ax.imshow(corr, aspect="auto")

    ax.set_xticks(range(len(corr.columns)))
    ax.set_yticks(range(len(corr.columns)))
    ax.set_xticklabels(corr.columns, rotation=35, ha="right")
    ax.set_yticklabels(corr.columns)

    for i in range(len(corr.index)):
        for j in range(len(corr.columns)):
            ax.text(
                j,
                i,
                f"{corr.iloc[i, j]:.2f}",
                ha="center",
                va="center",
                fontsize=9,
                color="#1F1F1F",
            )

    format_axis(
        ax,
        title="Correlation Matrix",
        subtitle="Relationship between core operational and delay-related variables",
    )

    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    save_figure(fig, os.path.join(FIGURES_DIR, "correlation_matrix.png"))


def run_eda():
    ensure_directories()

    df = load_data()
    df = clean_data(df)
    save_processed_data(df)

    summary_df, city_summary = create_summary_metrics(df)

    plot_distance_distribution(df)
    plot_average_time_by_traffic(df)
    plot_average_cost_by_vehicle(df)
    plot_delay_rate_by_traffic(df)
    plot_correlation_matrix(df)

    print("EDA completed successfully.")
    print(f"Processed data saved to: {PROCESSED_DATA_PATH}")
    print(f"Figures saved to: {FIGURES_DIR}")
    print(f"Metrics saved to: {METRICS_DIR}")
    print("\nSummary metrics:")
    print(summary_df.to_string(index=False))
    print("\nCity summary preview:")
    print(city_summary.head().to_string(index=False))


if __name__ == "__main__":
    run_eda()
