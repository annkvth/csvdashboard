import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Initialize df as a global variable
df = pd.DataFrame()


# -----------------------------------
# --- Define different plot types ---
# -----------------------------------


def line_plot(df):
    # Get user input for x-axis and y-axis column selection
    x_axis_column = st.selectbox("Select a column for the x-axis:", df.columns)
    selected_columns = st.multiselect("Select columns for the y-axis:", df.columns)

    # Optional datetime conversion for x-axis
    convert_to_datetime = st.checkbox("Convert x-axis column to datetime", value=True)
    if convert_to_datetime:
        df[x_axis_column] = pd.to_datetime(df[x_axis_column])

    # Store traces in a list
    traces = []

    # Plot the selected columns against the selected x-axis column
    for selected_column in selected_columns:
        # Drop rows with NaN values in the selected column
        df_filtered = df[[x_axis_column, selected_column]].dropna()

        if not df_filtered.empty:
            # Create a trace for each column
            trace = go.Scatter(x=df_filtered[x_axis_column], y=df_filtered[selected_column], mode='lines', name=f'{selected_column} over {x_axis_column}')
            traces.append(trace)
        else:
            st.warning(f"No valid data to plot for {selected_column}.")

    # Create a single Plotly figure with all traces
    fig = go.Figure(data=traces)

    # Set layout
    fig.update_layout(title=f'Overlay of {", ".join(selected_columns)} over {x_axis_column}',
                      xaxis_title=x_axis_column,
                      yaxis_title="Values")

    # Display the combined plot
    st.plotly_chart(fig)


def histogram_1d(df):
    # Get user input for the column for 1D histogram
    selected_column_1d = st.selectbox("Select a column for 1D Histogram:", df.columns)

    # Drop rows with NaN values in the selected column
    df_filtered = df[selected_column_1d].dropna()

    # Plot 1D histogram
    if not df_filtered.empty:
        fig = px.histogram(df_filtered, x=selected_column_1d, title=f'1D Histogram of {selected_column_1d}')
        st.plotly_chart(fig)
    else:
        st.warning(f"No valid data to plot for {selected_column_1d}.")


def histogram_2d(df):
    # Get user input for x-axis and y-axis column selection for 2D histogram
    x_axis_column_2d = st.selectbox("Select a column for the x-axis (2D Histogram):", df.columns)
    y_axis_column_2d = st.selectbox("Select a column for the y-axis (2D Histogram):", df.columns)

    # Drop rows with NaN values in the selected columns
    df_filtered = df[[x_axis_column_2d, y_axis_column_2d]].dropna()

    # Create a density heatmap for 2D histogram
    if not df_filtered.empty:
        fig = go.Figure(go.Histogram2d(x=df_filtered[x_axis_column_2d], y=df_filtered[y_axis_column_2d], colorscale='Viridis'))
        fig.update_layout(title=f'2D Histogram of {x_axis_column_2d} vs {y_axis_column_2d}',
                          xaxis_title=x_axis_column_2d,
                          yaxis_title=y_axis_column_2d)
        st.plotly_chart(fig)
    else:
        st.warning(f"No valid data to plot for {x_axis_column_2d} vs {y_axis_column_2d}.")


def scatter_2d(df):
    # Get user input for x-axis and y-axis column selection for 2D scatter plot
    x_axis_column_2d = st.selectbox("Select a column for the x-axis (2D Scatter):", df.columns)
    y_axis_column_2d = st.selectbox("Select a column for the y-axis (2D Scatter):", df.columns)

    # Drop rows with NaN values in the selected columns
    df_filtered = df[[x_axis_column_2d, y_axis_column_2d]].dropna()

    # Plot 2D scatter plot using Plotly Graph Objects
    if not df_filtered.empty:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df_filtered[x_axis_column_2d], y=df_filtered[y_axis_column_2d], mode='markers'))
        fig.update_layout(title=f'2D Scatter plot of {x_axis_column_2d} vs {y_axis_column_2d}',
                          xaxis_title=x_axis_column_2d,
                          yaxis_title=y_axis_column_2d)
        st.plotly_chart(fig)
    else:
        st.warning(f"No valid data to plot for {x_axis_column_2d} vs {y_axis_column_2d}.")



# -------------------------------------
# --- The Main function starts here ---
# -------------------------------------
    
@st.cache_data
def load_data(url):
    df = pd.read_csv(url)
    return df

# Page title
st.title("CSV Data Plotting App")


# Expander for CSV file loading
with st.expander("CSV File Loading", expanded=True):
    # File uploader
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    # Check if a file is uploaded
    if uploaded_file is not None:
        # Read the CSV file into a DataFrame
        df = load_data(uploaded_file)

        # Display the DataFrame
        st.write("### Data Preview:")
        st.write(df)


        
# Display tabs only if DataFrame is not empty
if not df.empty:
    tab1, tab2, tab3, tab4 = st.tabs(["Line Plot", "1D Histogram", "2D Histogram", "2D Scatter with Profiles"])

    with tab1:
        st.header("Plot 1")
        line_plot(df)

    with tab2:
        st.header("Plot 2")
        histogram_1d(df)

    with tab3:
        st.header("Plot 3")
        histogram_2d(df)

    with tab4:
        st.header("Plot 4")
        scatter_2d(df)
