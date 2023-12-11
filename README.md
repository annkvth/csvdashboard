# csvdashboard

A streamlit dashboard for quick plotting of csv files using plotly

## Prerequisite

Might change as the project evolves --> see requirements.txt 

## Usage

To start the dashboard:

```
streamlit run csv-dashboard.py
```

This will open a browser window with the dashboard. 

To use it: Load a csv file, then go to the tab of the plot type you want to make and select what you want to plot. 

For different type of plots are supported in this first version (line plot, 1D histo, 2D histo, scatter plot with profile histos).

The line plot also allows to convert string timestamps to time format for the x axis (using pandas to_datetime function).


## Remarks

Instead of running locally, this can also be hosted as an app on streamlit.io
