# Delivery Route Optimization

An end-to-end logistics analytics project focused on reducing delivery distance, estimated time, and operational cost through route optimization and predictive modeling.

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
- Analyze operational patterns in distance, time, and cost
- Optimize delivery routes using operations research
- Compare performance before and after optimization
- Predict delivery delays using machine learning
- Present results through clear and business-focused visualizations

## Tech Stack

- Python
- Pandas
- NumPy
- Matplotlib
- Plotly
- Folium
- Google OR-Tools
- scikit-learn
- Jupyter Notebook

## Current Progress

The initial repository structure is complete, and the first implementation stage of the project has already started.

Implemented so far:

- Repository folder organization
- Initial project documentation
- Delivery data simulation script (`src/data_generation.py`)
- Exploratory data analysis script (`src/eda.py`)
- Processed dataset and output generation structure

## Project Structure

```text
delivery-route-optimization/
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
├── src/
│   ├── data_generation.py
│   └── eda.py
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
   Analyze patterns related to travel distance, delivery time, cost distribution, and potential delay factors.

3. **Route Optimization**  
   Use Google OR-Tools to optimize delivery routes and reduce total distance and operational effort.

4. **Geospatial Visualization**  
   Build route maps and visual comparisons using Folium and Plotly.

5. **Delay Prediction**  
   Train a machine learning model to identify deliveries with a higher probability of delay.

6. **Business Impact Analysis**  
   Compare original and optimized scenarios using operational and financial metrics.

## Initial Simulated Dataset

The first version of the simulated dataset is designed to include variables such as:

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

## Current Analytical Outputs

The exploratory analysis stage is designed to generate:

- A cleaned dataset in `data/processed/`
- Summary operational metrics
- City-level performance metrics
- Distance distribution chart
- Average estimated time by traffic level
- Average cost by vehicle type
- Delay rate by traffic level
- Correlation matrix for numerical variables

## Expected Outputs

This project is expected to include:

- Delivery route maps before and after optimization
- Comparison of total distance, time, and cost
- Operational performance charts
- Feature importance for delay prediction
- Confusion matrix and classification metrics
- Portfolio-ready project documentation

## Business Value

This case study demonstrates how analytics can support logistics and operations teams by improving route efficiency, reducing unnecessary transportation costs, helping prioritize critical deliveries, and enabling more data-driven operational decisions.

## How to Run

After cloning the repository, install the dependencies listed in `requirements.txt`.

Current implementation files:

```text
src/data_generation.py
src/eda.py
```

Main execution flow:

1. Run the data simulation script to generate the raw delivery dataset
2. Run the exploratory data analysis script to clean the data and generate metrics and visual outputs

## Project Status

**In progress**

The repository structure, data simulation step, and exploratory analysis stage are already defined. The next steps are route optimization, geospatial visualization, and predictive modeling.

## Next Steps

- Generate the first simulated delivery dataset
- Perform exploratory data analysis
- Implement route optimization with OR-Tools
- Generate route maps and comparative metrics
- Train a delay prediction model
- Create dashboard-ready visual assets
- Finalize the project for GitHub and LinkedIn presentation

## Author

**Peterson Vital**  
Mechanical Engineer | Data Analytics | Machine Learning

- LinkedIn: [linkedin.com/in/petersonvital](https://linkedin.com/in/petersonvital)

---

This project is part of my portfolio to showcase applied analytics, logistics optimization, and machine learning for real-world business problems.
