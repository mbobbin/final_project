import shiny
from shiny import App, ui, reactive, render
import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd

# Read in the grouped data frame (assumed to already be a GeoDataFrame with a geometry column)
calls_type_census = gpd.read_file(
    r"response_times_by_tract_call_type.csv"
)
citywide_call_types=pd.read_csv("avg_citywide_by_category.csv")
citywide_call_types["Time_Diff_Minutes"]=citywide_call_types["Time_Diff_Minutes"].astype(float)
# Ensure 'Call Category' and other columns are properly typed
calls_type_census["Call Category"] = calls_type_census["Call Category"].astype(str)
calls_type_census["Time_Diff_Minutes"] = calls_type_census["Time_Diff_Minutes"].astype(float)
menu_choices = list(calls_type_census["Call Category"].unique())  # Convert to a Python list

# UI Design
app_ui = ui.page_fluid(
    ui.panel_title("Police Response Times by Census Tract in Seattle"),
    ui.input_select(
        id="crime",
        label="Choose a type of crime:",
        choices=menu_choices
    ),
    ui.output_text("citywide_info"),
    ui.output_text("overall_response"),
      ui.row(
        ui.column(6, ui.output_plot("chart", height="500px")),  # First plot on the left side
        ui.column(6, ui.output_plot("static_chart", height="500px"))  # Second plot on the right side
    )
)

# Server logic
def server(input, output, session):
    @reactive.Calc
    def full_data():
        return calls_type_census

    @reactive.Calc
    def subsetted_data():
        df = full_data()
        selected_call = input.crime()
        return df[df["Call Category"] == selected_call]
    @reactive.Calc
    def full_citywide_data():
        return citywide_call_types
    @reactive.Calc
    def citywide_stat():
        df=full_citywide_data()
        selected_category = input.crime()
        filtered_df=df[df["Call Category"]==selected_category]
        if not filtered_df.empty:
            response_time = filtered_df["Time_Diff_Minutes"].iloc[0]
            return f"Average Police response time citywide for {selected_category}: {response_time:.2f} minutes"
        else:
            return f"No data available for {selected_category}"
    @output
    @render.plot
    def chart():
        filtered_data = subsetted_data()

        # Debugging: Print the filtered data to check its structure
        print(filtered_data.head())  # Check the first few rows of filtered data

        if filtered_data.empty:
            print("No data to plot!")
            return None  # Handle case where no data is found
        filtered_data['geometry'] = gpd.GeoSeries.from_wkt(filtered_data['geometry'])
        filtered_data = gpd.GeoDataFrame(filtered_data, geometry="geometry")
        # Create a Matplotlib plot
        fig, ax = plt.subplots(figsize=(14, 8))

        # Plot the data as a map using geopandas
        plot = filtered_data.plot(
            column="Time_Diff_Minutes",  # Column to define color
            cmap="Reds",  # Color map
            legend=True,
            legend_kwds={"label":"Average Response Time (Minutes)"},
            ax=ax
        )

        # Set title and remove axis for a clean map
        ax.set_title("Average Police Response Time by Census Tract for Selected Crime", fontsize=14)
        ax.axis("off")  # Turn off the axis for a clean map

        # Update legend title after plot
        # Get the legend (colorbar) from the plot
        legend = ax.get_children()[0]  # This gets the colorbar
        legend.set_label("Average Response Time (Minutes)")  # Set legend title

        # Adjust layout to prevent clipping of the legend
        fig.tight_layout()

        return fig  # Return the figure for rendering
    @output
    @render.plot
    def static_chart():
    # Create static data for plotting (this can be replaced with your actual static data)
        static_data = gpd.read_file("agg_calls_census_merged.csv")  # Use the full dataset or any fixed subset
        static_data["Time_Diff_Minutes"]=static_data["Time_Diff_Minutes"].astype(float)
        static_data['geometry'] = gpd.GeoSeries.from_wkt(static_data['geometry'])
        static_data=gpd.GeoDataFrame(static_data, geometry="geometry")
        fig, ax = plt.subplots(figsize=(14, 8))

    # Plot the static data as a map using GeoPandas
        static_data.plot(
        column="Time_Diff_Minutes",  # Column to define color
        cmap="Reds",  # Color map for the static plot
        legend=True,
        ax=ax
        )

        # Set title and remove axis for a clean map
        ax.set_title("Overall Police Response Times by Census Tract", fontsize=14)
        ax.axis("off")  # Turn off the axis for a clean map

        # Update legend title after plot
        # Get the legend (colorbar) from the plot
        legend = ax.get_children()[0]  # This gets the colorbar
        legend.set_label("Average Response Time (Minutes)") 

        # Adjust layout to prevent clipping
        fig.tight_layout()

        return fig  # Return the figure for rendering
    @output
    @render.text
    def citywide_info():
        return citywide_stat()
    @output
    @render.text
    def overall_response():
        return "Average response time for all calls citywide is 42.81 minutes"

# Create the app
app = App(app_ui, server)

if __name__ == "__main__":
    app.run()


