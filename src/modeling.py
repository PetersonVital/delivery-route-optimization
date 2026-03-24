import os
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

from chart_utils import create_figure, format_axis, annotate_barh, save_figure


INPUT_DATA_PATH = "data/processed/deliveries_cleaned.csv"
FIGURES_DIR = "outputs/figures"
METRICS_DIR = "outputs/metrics"

CLASSIFICATION_REPORT_PATH = os.path.join(METRICS_DIR, "classification_report.txt")
MODEL_METRICS_PATH = os.path.join(METRICS_DIR, "model_metrics.csv")
FEATURE_IMPORTANCE_PATH = os.path.join(FIGURES_DIR, "feature_importance.png")
CONFUSION_MATRIX_PATH = os.path.join(FIGURES_DIR, "confusion_matrix.png")


def ensure_directories():
    os.makedirs(FIGURES_DIR, exist_ok=True)
    os.makedirs(METRICS_DIR, exist_ok=True)


def load_data(file_path=INPUT_DATA_PATH):
    return pd.read_csv(file_path)


def prepare_features_and_target(df):
    feature_columns = [
        "city",
        "state",
        "distance_km",
        "estimated_time_min",
        "traffic_level",
        "vehicle_type",
        "delivery_window",
        "package_weight_kg",
        "fuel_cost_brl",
        "original_cost_brl",
    ]

    target_column = "delay_risk"

    x = df[feature_columns].copy()
    y = df[target_column].copy()

    return x, y


def build_pipeline(numeric_features, categorical_features):
    numeric_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
        ]
    )

    categorical_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore")),
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, numeric_features),
            ("cat", categorical_transformer, categorical_features),
        ]
    )

    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=8,
        random_state=42,
    )

    pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("model", model),
        ]
    )

    return pipeline


def save_classification_outputs(y_test, y_pred):
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred, digits=4, zero_division=0)
    cm = confusion_matrix(y_test, y_pred)

    metrics_df = pd.DataFrame(
        [
            {
                "accuracy": round(accuracy, 4),
                "true_negative": int(cm[0, 0]),
                "false_positive": int(cm[0, 1]),
                "false_negative": int(cm[1, 0]),
                "true_positive": int(cm[1, 1]),
            }
        ]
    )
    metrics_df.to_csv(MODEL_METRICS_PATH, index=False)

    with open(CLASSIFICATION_REPORT_PATH, "w", encoding="utf-8") as file:
        file.write(report)

    return metrics_df, cm, report


def plot_confusion_matrix(cm):
    fig, ax = create_figure(figsize=(6, 5))
    im = ax.imshow(cm, aspect="auto")

    ax.set_xticks([0, 1])
    ax.set_yticks([0, 1])
    ax.set_xticklabels(["Predicted On Time", "Predicted Delayed"])
    ax.set_yticklabels(["Actual On Time", "Actual Delayed"])

    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(
                j,
                i,
                str(cm[i, j]),
                ha="center",
                va="center",
                fontsize=12,
                fontweight="semibold",
                color="#1F1F1F",
            )

    format_axis(
        ax,
        title="Confusion Matrix",
        subtitle="Classification results for delivery delay prediction",
    )

    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    save_figure(fig, CONFUSION_MATRIX_PATH)


def get_feature_names(preprocessor, numeric_features, categorical_features):
    cat_encoder = preprocessor.named_transformers_["cat"].named_steps["onehot"]
    cat_feature_names = cat_encoder.get_feature_names_out(categorical_features)
    return list(numeric_features) + list(cat_feature_names)


def plot_feature_importance(pipeline, numeric_features, categorical_features):
    preprocessor = pipeline.named_steps["preprocessor"]
    model = pipeline.named_steps["model"]

    feature_names = get_feature_names(preprocessor, numeric_features, categorical_features)
    importances = model.feature_importances_

    feature_importance_df = pd.DataFrame(
        {
            "feature": feature_names,
            "importance": importances,
        }
    ).sort_values("importance", ascending=False)

    top_features = feature_importance_df.head(10).sort_values("importance", ascending=True)

    fig, ax = create_figure(figsize=(10, 6))
    bars = ax.barh(top_features["feature"], top_features["importance"], height=0.65)

    format_axis(
        ax,
        title="Top 10 Feature Importances",
        subtitle="Most relevant variables for delivery delay prediction",
        xlabel="Importance Score",
        ylabel="Feature",
    )

    annotate_barh(ax, fmt="{:.3f}")
    save_figure(fig, FEATURE_IMPORTANCE_PATH)

    return feature_importance_df

    feature_names = get_feature_names(preprocessor, numeric_features, categorical_features)
    importances = model.feature_importances_

    feature_importance_df = pd.DataFrame(
        {
            "feature": feature_names,
            "importance": importances,
        }
    ).sort_values("importance", ascending=False)

    top_features = feature_importance_df.head(10).sort_values("importance")

    plt.figure(figsize=(10, 6))
    plt.barh(top_features["feature"], top_features["importance"])
    plt.title("Top 10 Feature Importances")
    plt.xlabel("Importance")
    plt.ylabel("Feature")
    plt.tight_layout()
    plt.savefig(FEATURE_IMPORTANCE_PATH)
    plt.close()

    return feature_importance_df


def run_modeling():
    ensure_directories()

    df = load_data()
    x, y = prepare_features_and_target(df)

    numeric_features = [
        "distance_km",
        "estimated_time_min",
        "package_weight_kg",
        "fuel_cost_brl",
        "original_cost_brl",
    ]

    categorical_features = [
        "city",
        "state",
        "traffic_level",
        "vehicle_type",
        "delivery_window",
    ]

    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    pipeline = build_pipeline(numeric_features, categorical_features)
    pipeline.fit(x_train, y_train)

    y_pred = pipeline.predict(x_test)

    metrics_df, cm, report = save_classification_outputs(y_test, y_pred)
    plot_confusion_matrix(cm)
    feature_importance_df = plot_feature_importance(
        pipeline,
        numeric_features,
        categorical_features,
    )

    feature_importance_df.to_csv(
        os.path.join(METRICS_DIR, "feature_importance.csv"),
        index=False,
    )

    print("Modeling completed successfully.")
    print(f"Metrics saved to: {MODEL_METRICS_PATH}")
    print(f"Classification report saved to: {CLASSIFICATION_REPORT_PATH}")
    print(f"Confusion matrix saved to: {CONFUSION_MATRIX_PATH}")
    print(f"Feature importance saved to: {FEATURE_IMPORTANCE_PATH}")
    print("\nModel metrics:")
    print(metrics_df.to_string(index=False))
    print("\nTop 10 important features:")
    print(feature_importance_df.head(10).to_string(index=False))
    print("\nClassification report:")
    print(report)


if __name__ == "__main__":
    run_modeling()
