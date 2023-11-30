import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Initialize df as a global variable
df = pd.DataFrame()

def line_plot(df):
    # Get user input for x-axis and y-axis column selection
    x_axis_column = st.selectbox("Select a column for the x-axis:", df.columns)
    selected_columns = st.multiselect("Select columns for the y-axis:", df.columns)

    # Optional datetime conversion for x-axis
    convert_to_datetime = st.checkbox("Convert x-axis column to datetime", value=True)
    if convert_to_datetime:
        df[x_axis_column] = pd.to_datetime(df[x_axis_column])

    # Plot the selected columns against the selected x-axis column
    if selected_columns:
        fig = px.line(df, x=x_axis_column, y=selected_columns, title=f'{", ".join(selected_columns)} over {x_axis_column}')
        st.plotly_chart(fig)
    else:
        st.warning("Please select at least one column for plotting.")

def histogram_1d(df):
    # Get user input for the column for 1D histogram
    selected_column_1d = st.selectbox("Select a column for 1D Histogram:", df.columns)

    # Plot 1D histogram
    fig = px.histogram(df, x=selected_column_1d, title=f'1D Histogram of {selected_column_1d}')
    st.plotly_chart(fig)

def histogram_2d(df):
    # Get user input for x-axis and y-axis column selection for 2D histogram
    x_axis_column_2d = st.selectbox("Select a column for the x-axis (2D Histogram):", df.columns)
    y_axis_column_2d = st.selectbox("Select a column for the y-axis (2D Histogram):", df.columns)

    # Create a density heatmap for 2D histogram
    fig = go.Figure(go.Histogram2d(x=df[x_axis_column_2d], y=df[y_axis_column_2d], colorscale='Viridis'))

    # Update layout
    fig.update_layout(title=f'2D Histogram of {x_axis_column_2d} vs {y_axis_column_2d}',
                      xaxis_title=x_axis_column_2d,
                      yaxis_title=y_axis_column_2d)

    st.plotly_chart(fig)

def scatter_2d(df):
    # Get user input for x-axis and y-axis column selection for 2D histogram
    x_axis_column_2d = st.selectbox("Select a column for the x-axis (2D Scatter):", df.columns)
    y_axis_column_2d = st.selectbox("Select a column for the y-axis (2D Scatter):", df.columns)

    # Plot 2D histogram using scatter plot
    fig = px.scatter(df, x=x_axis_column_2d, y=y_axis_column_2d, marginal_x="histogram", marginal_y="histogram", title=f'2D Scatter plot of {x_axis_column_2d} vs {y_axis_column_2d}')
    st.plotly_chart(fig)

#def select_and_plot(df):
#    # Get user input for plot type
#    plot_type = st.selectbox("Select plot type:", ["Line Plot", "1D Histogram", "2D Histogram", "2D Scatter with Profiles"])
#
#    # Plot based on the selected plot type
#    if plot_type == "Line Plot":
#        line_plot(df)
#            
#    elif plot_type == "1D Histogram":
#        histogram_1d(df)
#        
#    elif plot_type == "2D Histogram":
#        histogram_2d(df)
#        
#    elif plot_type == "2D Scatter with Profiles":
#        scatter_2d(df)
#
#    else:
#        st.warning("Invalid plot type selected.")

    
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
