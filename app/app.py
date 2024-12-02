import shiny
from shiny import App, ui, reactive, render
import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd

# Read in the grouped data frame (assumed to already be a GeoDataFrame with a geometry column)
calls_type_census = gpd.read_file(
    r"C:\Users\Mitch\Documents\GitHub\final_project\response_times_by_tract_call_type.csv"
)

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
    ui.output_plot("chart",height="800px"),  # Render Matplotlib plot
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
        fig, ax = plt.subplots(figsize=(15, 9))

        # Plot the data as a map using geopandas
        plot = filtered_data.plot(
            column="Time_Diff_Minutes",  # Column to define color
            cmap="Reds",  # Color map
            legend=True,
            legend_kwds={"label":"Average Response Time (Minutes)"},
            ax=ax
        )

        # Set title and remove axis for a clean map
        ax.set_title("Average Police Response Time by Census Tract", fontsize=16)
        ax.axis("off")  # Turn off the axis for a clean map

        # Update legend title after plot
        # Get the legend (colorbar) from the plot
        legend = ax.get_children()[0]  # This gets the colorbar
        legend.set_label("Average Response Time (Minutes)")  # Set legend title

        # Adjust layout to prevent clipping of the legend
        fig.tight_layout()

        return fig  # Return the figure for rendering

# Create the app
app = App(app_ui, server)

if __name__ == "__main__":
    app.run()


