"""
Sales Dashboard Web App for Novel Sense Task
Author: Muhammad Zeerak

Description:
An interactive Plotly Dash web application that visualizes monthly sales data
for multiple product categories. 

Features:
- Dropdown filter to choose a category
- Two synchronized charts (bar and line)
- Responsive layout using Dash Bootstrap Components
- Custom hover animations via CSS
- CSV export button
- Basic error handling and user feedback
"""

# -------------------------------
# IMPORTS
# -------------------------------
# Dash is the main web framework
import dash

# dcc (Dash Core Components) = dropdowns, graphs, etc.
# html (Dash HTML Components) = HTML tags for layout
# Input, Output = used for callback functionality
# no_update = prevents unwanted figure refresh if something fails
from dash import dcc, html, Input, Output, no_update

# Bootstrap components for responsive layouts and prebuilt styling
import dash_bootstrap_components as dbc

# pandas for handling and manipulating tabular data
import pandas as pd

# plotly.express for quick interactive data visualizations
import plotly.express as px


# -------------------------------
# DATA SETUP
# -------------------------------
# Define mock sales data for 3 categories

data = {
    "month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
    "Electronics": [15000, 18000, 22000, 19000, 24000, 21000],
    "Clothing": [8000, 9500, 11000, 10500, 12000, 13000],
    "Food": [12000, 13000, 14000, 14500, 15000, 16000],
}

# Convert the dictionary to a pandas DataFrame
df = pd.DataFrame(data)


# -------------------------------
# DASH APP INITIALIZATION
# -------------------------------
# Initialize the Dash app
# external_stylesheets loads Bootstrap for styling

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Set browser tab title
app.title = "Sales Dashboard"


# -------------------------------
# LAYOUT
# -------------------------------
# The layout defines the structure and appearance of the web app
# We use Bootstrap's Container, Row, and Col to make it responsive

app.layout = dbc.Container(
    [
        # ---------- Header ----------
        html.H1(
            "📈 Sales Dashboard",        # Title text with emoji
            className="text-center mt-4 mb-4",  # Centered with margin
            id="main-title",             # ID used for custom CSS hover animation
        ),

        # ---------- Dropdown Row ----------
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Label(
                            "Select Category:",
                            style={"fontWeight": "bold"}  # Bold label
                        ),
                        dcc.Dropdown(
                            id="category-dropdown",       # Dropdown component ID
                            options=[
                                {"label": c, "value": c}  # Create an option for each column
                                for c in df.columns
                                if c != "month"           # Skip the 'month' column
                            ],
                            value="Electronics",          # Default selection
                            clearable=False,              # Prevent user from clearing it completely
                        ),
                    ],
                    width=12,
                    md=6,  # Medium+ screens = half width, small screens = full width
                ),
            ],
            className="mb-4",  # Bottom margin for spacing
        ),

        # ---------- Total Sales Card ----------
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardBody(
                                    [
                                        html.H4(
                                            "Total Sales", className="card-title"
                                        ),
                                        html.Div(
                                            id="total-sales-card",   # Output placeholder for total value
                                            className="fs-4 fw-bold" # Font size 4, bold
                                        ),
                                    ]
                                )
                            ],
                            color="primary",  # Blue Bootstrap color
                            inverse=True,     # White text on colored background
                            className="text-center",  # Center align card content
                        )
                    ],
                    width=12,
                    md=6,
                )
            ],
            className="mb-4 justify-content-center",
        ),

        # ---------- Two Graphs (Bar + Line) ----------
        dbc.Row(
            [
                dbc.Col([dcc.Graph(id="sales-bar-chart")], md=6, sm=12),
                dbc.Col([dcc.Graph(id="sales-line-chart")], md=6, sm=12),
            ],
            className="mb-4",
        ),

        # ---------- Export Button ----------
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Button(
                            "⬇ Export CSV",
                            id="export-btn",        # Button ID
                            n_clicks=0,             # Tracks how many times it’s clicked
                            className="btn btn-success",  # Bootstrap button style
                        ),
                        html.Div(
                            id="export-msg",       # Message placeholder
                            className="mt-2 fw-semibold"
                        ),
                    ],
                    className="text-center",
                )
            ],
            className="mb-4",
        ),
    ],
    fluid=True,  # Makes layout responsive to screen width
)


# -------------------------------
# CALLBACKS
# -------------------------------
# Dash callbacks connect UI (inputs) to logic (outputs)
# Whenever the dropdown changes, this callback runs automatically

@app.callback(
    [
        Output("sales-bar-chart", "figure"),   # Update bar chart
        Output("sales-line-chart", "figure"),  # Update line chart
        Output("total-sales-card", "children") # Update total card text
    ],
    Input("category-dropdown", "value"),       # Trigger input
)
def update_dashboard(selected_category: str):
    """
    Updates both charts and the total sales card based on the selected category.
    Includes error handling to prevent app crashes if the input is invalid.
    """
    try:
        # --- Input validation ---
        if selected_category not in df.columns:
            return no_update, no_update, "⚠️ Invalid category selected."

        # --- Bar Chart ---
        bar_fig = px.bar(
            df,
            x="month",
            y=selected_category,
            title=f"Monthly Sales - {selected_category}",
            color="month",
            text=selected_category,
        )
        bar_fig.update_layout(
            showlegend=False, 
            yaxis_title="Sales ($)", 
            template="plotly_white"
        )

        # --- Line Chart ---
        line_fig = px.line(
            df,
            x="month",
            y=selected_category,
            markers=True,
            title=f"Sales Trend - {selected_category}",
        )
        line_fig.update_layout(
            yaxis_title="Sales ($)", 
            template="plotly_white"
        )

        # --- Total Sales Calculation ---
        total_sales = df[selected_category].sum()
        total_text = f"${total_sales:,.0f}"  # Format with commas and $ sign

        return bar_fig, line_fig, total_text

    except Exception as e:
        # Catch unexpected runtime errors and display a friendly message
        error_msg = f"An error occurred while updating: {e}"
        return no_update, no_update, error_msg


# Second callback: triggered when user clicks "Export CSV"
@app.callback(
    Output("export-msg", "children"),  # Text message area
    Input("export-btn", "n_clicks"),   # Button click trigger
    prevent_initial_call=True          # Ignore the first render
)
def export_csv(n_clicks: int):
    """
    Exports the DataFrame to a CSV file and confirms success to the user.
    Includes error handling for file write issues.
    """
    try:
        filename = "sales_data.csv"
        df.to_csv(filename, index=False)
        return f"Data exported successfully as {filename}"
    except Exception as e:
        return f"Failed to export data: {e}"


# -------------------------------
# RUN APP
# -------------------------------
# The main entry point — starts the Dash web server locally

if __name__ == "__main__":
    # debug=True enables live reloading and error messages while developing
    app.run(debug=True)




