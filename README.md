# econ_dashboard
API download, clean data, structure data, push to Streamlit

The purpose of the app is for users to determine if two data variables are related

1) This app pulls about two dozen economic variables from the Federal Reserve's FRED database via API
2) It then resamples the data so the daily, weekly, and quarterly data all align with the monthly cadence
3) The data is then pushed to a Streamlit dashboard, where one can view at and interact with the data
4) The app allows users to compare two time series data elements
5) The data is visualized through three charts
   a) actual data over time
   b) yoy data over time
   c) yoy scatterplot with correlation coefficient
6) Users can select different variables and different time frames
