# Delivery Route Optimization

An end-to-end logistics analytics project focused on reducing delivery distance, estimated time, and operational cost through route optimization, geospatial visualization, and predictive modeling.

## Overview

This project simulates a delivery operation and applies analytics, optimization, and machine learning techniques to improve decision-making in last-mile logistics.

The main business question behind this project is:

**How can route optimization reduce delivery distance, delivery time, and operational cost while helping identify deliveries at higher risk of delay?**

## Business Problem

Delivery operations often face inefficiencies caused by poor route planning, unnecessary travel distance, traffic-related delays, and increasing transportation costs.

In real business environments, these inefficiencies can lead to higher operational expenses, lower service reliability, delayed deliveries, and reduced customer satisfaction.

This project addresses that challenge by combining route optimization and delay prediction in a single business-oriented analytics case study.

## Project Goals

The main goals of this project are:

- Simulate a realistic delivery dataset
- Analyze operational patterns in distance, time, cost, and delay risk
- Optimize delivery routes using operations research
- Compare original and optimized routing performance
- Build interactive route maps for visual analysis
- Predict delivery delays using machine learning
- Present results through business-focused visualizations and metrics

## Tech Stack

- Python
- Pandas
- NumPy
- Matplotlib
- Folium
- Google OR-Tools
- scikit-learn
- Jupyter Notebook

## Current Progress

The project already includes the main first-version implementation stages.

Implemented so far:

- Repository folder organization
- Initial project documentation
- Delivery data simulation script
- Exploratory data analysis script
- Route optimization script with OR-Tools
- Interactive route mapping with Folium
- Delivery delay prediction model
- Reporting script for final presentation charts and metrics

## Project Structure

```text
delivery-route-optimization/
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
├── src/
│   ├── data_generation.py
│   ├── eda.py
│   ├── optimization.py
│   ├── mapping.py
│   ├── modeling.py
│   └── reporting.py
├── outputs/
│   ├── figures/
│   ├── maps/
│   └── metrics/
├── dashboard/
├── requirements.txt
└── README.md
```

## Methodology

The project is structured in six main stages:

1. **Data Simulation**  
   Create a synthetic delivery dataset with variables such as city, distance, estimated time, traffic level, delivery status, and operational cost.

2. **Exploratory Data Analysis**  
   Analyze patterns related to travel distance, delivery time, cost distribution, and delay-related factors.

3. **Route Optimization**  
   Use Google OR-Tools to optimize delivery routes and reduce total route distance.

4. **Geospatial Visualization**  
   Build interactive route maps for both the original and optimized scenarios using Folium.

5. **Delay Prediction**  
   Train a machine learning model to identify deliveries with a higher probability of delay.

6. **Business Reporting**  
   Consolidate operational results into presentation-ready metrics and charts.

## Dataset Design

The simulated dataset includes variables such as:

- `delivery_id`
- `city`
- `state`
- `latitude`
- `longitude`
- `distance_km`
- `estimated_time_min`
- `traffic_level`
- `vehicle_type`
- `delivery_window`
- `package_weight_kg`
- `fuel_cost_brl`
- `delivery_status`
- `delay_risk`
- `original_cost_brl`

## Implemented Scripts

### `src/data_generation.py`
Generates the synthetic delivery dataset and saves the raw file to `data/raw/`.

### `src/eda.py`
Cleans the dataset, creates summary metrics, and generates exploratory analysis charts.

### `src/optimization.py`
Builds a simplified routing problem and uses Google OR-Tools to calculate an optimized route.

### `src/mapping.py`
Creates interactive Folium maps for the original and optimized delivery routes.

### `src/modeling.py`
Trains a machine learning model to predict delivery delays and generates classification outputs.

### `src/reporting.py`
Consolidates project results and creates presentation-ready charts and final summary metrics.

## Current Outputs

The project generates outputs such as:

### Data
- Processed delivery dataset
- Cleaned analytical dataset

### Metrics
- Summary operational metrics
- City-level performance metrics
- Route comparison metrics
- Optimized route sequence
- Model evaluation metrics
- Final report metrics

### Figures
- Distance distribution
- Average estimated time by traffic level
- Average cost by vehicle type
- Delay rate by traffic level
- Correlation matrix
- Confusion matrix
- Feature importance chart
- Route distance comparison
- Distance reduction percentage
- Overall delay rate
- Deliveries by city

### Maps
- Original route map
- Optimized route map

## Business Value

This case study demonstrates how analytics can support logistics and operations teams by:

- improving route efficiency,
- reducing unnecessary transportation costs,
- supporting operational prioritization,
- identifying deliveries at higher risk of delay,
- and enabling more data-driven decision-making.

## How to Run

After cloning the repository, install the dependencies listed in `requirements.txt`.

Suggested execution order:

1. Run `src/data_generation.py`
2. Run `src/eda.py`
3. Run `src/optimization.py`
4. Run `src/mapping.py`
5. Run `src/modeling.py`
6. Run `src/reporting.py`

## Project Status

**In progress**

The first end-to-end version of the project structure and core scripts is complete. The next steps involve refining outputs, improving visual presentation, and strengthening the portfolio narrative for GitHub and LinkedIn.

## Next Steps

- Add screenshots of charts and maps to the README
- Create a portfolio-ready dashboard view
- Refine route optimization with more realistic business constraints
- Improve model evaluation and interpretation
- Add notebook versions for presentation and walkthrough
- Prepare LinkedIn project communication materials

## Author

**Peterson Vital**  
Mechanical Engineer | Data Analytics | Machine Learning

- LinkedIn: [linkedin.com/in/petersonvital](https://linkedin.com/in/petersonvital)

---

This project is part of my portfolio to showcase applied analytics, logistics optimization, and machine learning for real-world business problems.
