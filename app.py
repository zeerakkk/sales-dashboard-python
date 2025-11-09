"""
Sales Dashboard Web App
Author: [Your Name]
Description:
An interactive Plotly Dash application that visualizes sales data by category.
Includes responsive layout (Bootstrap), hover animations (CSS), and export-to-CSV functionality.
Now enhanced with basic error handling to prevent crashes from invalid inputs.
"""

import dash
from dash import dcc, html, Input, Output, no_update
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

# ==========================
# Sample Data
# ==========================
data = {
    "month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
    "Electronics": [15000, 18000, 22000, 19000, 24000, 21000],
    "Clothing": [8000, 9500, 11000, 10500, 12000, 13000],
    "Food": [12000, 13000, 14000, 14500, 15000, 16000],
}
df = pd.DataFrame(data)

# ==========================
# Dash App Setup
# ==========================
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Sales Dashboard"

# ==========================
# Layout
# ==========================
app.layout = dbc.Container(
    [
        # Header
        html.H1(
            "📈 Sales Dashboard",
            className="text-center mt-4 mb-4",
            id="main-title",
        ),

        # Dropdown row
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Label("Select Category:", style={"fontWeight": "bold"}),
                        dcc.Dropdown(
                            id="category-dropdown",
                            options=[
                                {"label": c, "value": c}
                                for c in df.columns
                                if c != "month"
                            ],
                            value="Electronics",
                            clearable=False,
                        ),
                    ],
                    width=12,
                    md=6,
                ),
            ],
            className="mb-4",
        ),

        # Total sales card row
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardBody(
                                    [
                                        html.H4("Total Sales", className="card-title"),
                                        html.Div(
                                            id="total-sales-card",
                                            className="fs-4 fw-bold",
                                        ),
                                    ]
                                )
                            ],
                            color="primary",
                            inverse=True,
                            className="text-center",
                        )
                    ],
                    width=12,
                    md=6,
                )
            ],
            className="mb-4 justify-content-center",
        ),

        # Charts row
        dbc.Row(
            [
                dbc.Col([dcc.Graph(id="sales-bar-chart")], md=6, sm=12),
                dbc.Col([dcc.Graph(id="sales-line-chart")], md=6, sm=12),
            ],
            className="mb-4",
        ),

        # Export button row
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Button(
                            "⬇ Export CSV",
                            id="export-btn",
                            n_clicks=0,
                            className="btn btn-success",
                        ),
                        html.Div(id="export-msg", className="mt-2 fw-semibold"),
                    ],
                    className="text-center",
                )
            ],
            className="mb-4",
        ),
    ],
    fluid=True,
)

# ==========================
# Callbacks
# ==========================


@app.callback(
    [
        Output("sales-bar-chart", "figure"),
        Output("sales-line-chart", "figure"),
        Output("total-sales-card", "children"),
    ],
    Input("category-dropdown", "value"),
)
def update_dashboard(selected_category: str):
    """Update charts and total card when a category is selected.
    Includes basic error handling for invalid inputs.
    """
    try:
        # Validation: ensure selected category exists
        if selected_category not in df.columns:
            return no_update, no_update, "⚠️ Invalid category selected."

        # Bar chart
        bar_fig = px.bar(
            df,
            x="month",
            y=selected_category,
            title=f"Monthly Sales - {selected_category}",
            color="month",
            text=selected_category,
        )
        bar_fig.update_layout(
            showlegend=False, yaxis_title="Sales ($)", template="plotly_white"
        )

        # Line chart
        line_fig = px.line(
            df,
            x="month",
            y=selected_category,
            markers=True,
            title=f"Sales Trend - {selected_category}",
        )
        line_fig.update_layout(yaxis_title="Sales ($)", template="plotly_white")

        # Total sales text
        total_sales = df[selected_category].sum()
        total_text = f"${total_sales:,.0f}"

        return bar_fig, line_fig, total_text

    except Exception as e:
        # Catch unexpected errors (e.g., data issues)
        error_msg = f"❌ An error occurred while updating: {e}"
        return no_update, no_update, error_msg


@app.callback(
    Output("export-msg", "children"),
    Input("export-btn", "n_clicks"),
    prevent_initial_call=True,
)
def export_csv(n_clicks: int):
    """Export the current data to CSV when the button is clicked.
    Includes error handling to catch file-write issues.
    """
    try:
        filename = "sales_data.csv"
        df.to_csv(filename, index=False)
        return f"✅ Data exported successfully as {filename}"
    except Exception as e:
        return f"❌ Failed to export data: {e}"


# ==========================
# Run the app
# ==========================
if __name__ == "__main__":
    app.run(debug=True)



