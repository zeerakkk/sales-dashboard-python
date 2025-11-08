import dash
from dash import dcc, html
import pandas as pd

data = {
    'month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
    'Electronics': [15000, 18000, 22000, 19000, 24000, 21000],
    'Clothing': [8000, 9500, 11000, 10500, 12000, 13000],
    'Food': [12000, 13000, 14000, 14500, 15000, 16000]
}
df = pd.DataFrame(data)

app = dash.Dash(__name__)
app.title = "Sales Dashboard"

app.layout = html.Div(
    style={"fontFamily": "Arial", "margin": "40px"},
    children=[
        html.H1("📈 Sales Dashboard", style={"textAlign": "center"}),

        html.Label("Select Category:", style={"fontWeight": "bold"}),
        dcc.Dropdown(
            id="category-dropdown",
            options=[{"label": c, "value": c} for c in df.columns if c != 'month'],
            value="Electronics",
            clearable=False,
            style={"width": "50%"}
        ),

        html.Div(id="total-sales-card",
                 style={"textAlign": "center", "fontSize": "22px", "margin": "20px"}),

        dcc.Graph(id="sales-bar-chart")
    ]
)

if __name__ == "__main__":
    app.run(debug=True)

