import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


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
    plt.figure(figsize=(10, 6))
    plt.hist(df["distance_km"], bins=20, edgecolor="black")
    plt.title("Distribution of Delivery Distance")
    plt.xlabel("Distance (km)")
    plt.ylabel("Number of Deliveries")
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "distance_distribution.png"))
    plt.close()


def plot_average_time_by_traffic(df):
    avg_time = (
        df.groupby("traffic_level")["estimated_time_min"]
        .mean()
        .reindex(["Low", "Medium", "High"])
    )

    plt.figure(figsize=(8, 5))
    plt.bar(avg_time.index, avg_time.values)
    plt.title("Average Estimated Time by Traffic Level")
    plt.xlabel("Traffic Level")
    plt.ylabel("Estimated Time (minutes)")
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "average_time_by_traffic.png"))
    plt.close()


def plot_average_cost_by_vehicle(df):
    avg_cost = df.groupby("vehicle_type")["original_cost_brl"].mean().sort_values()

    plt.figure(figsize=(8, 5))
    plt.bar(avg_cost.index, avg_cost.values)
    plt.title("Average Cost by Vehicle Type")
    plt.xlabel("Vehicle Type")
    plt.ylabel("Average Cost (BRL)")
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "average_cost_by_vehicle.png"))
    plt.close()


def plot_delay_rate_by_traffic(df):
    delay_rate = (
        df.groupby("traffic_level")["delay_risk"]
        .mean()
        .reindex(["Low", "Medium", "High"])
        * 100
    )

    plt.figure(figsize=(8, 5))
    plt.bar(delay_rate.index, delay_rate.values)
    plt.title("Delay Rate by Traffic Level")
    plt.xlabel("Traffic Level")
    plt.ylabel("Delay Rate (%)")
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "delay_rate_by_traffic.png"))
    plt.close()


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

    plt.figure(figsize=(8, 6))
    plt.imshow(corr, interpolation="nearest", aspect="auto")
    plt.xticks(range(len(corr.columns)), corr.columns, rotation=45, ha="right")
    plt.yticks(range(len(corr.columns)), corr.columns)
    plt.colorbar()
    plt.title("Correlation Matrix")
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "correlation_matrix.png"))
    plt.close()


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
