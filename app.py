import dash
from dash import html
import pandas as pd

data = {
    'month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
    'Electronics': [15000, 18000, 22000, 19000, 24000, 21000],
    'Clothing': [8000, 9500, 11000, 10500, 12000, 13000],
    'Food': [12000, 13000, 14000, 14500, 15000, 16000]
}

df = pd.DataFrame(data)

app = dash.Dash(__name__)
app.layout = html.Div("Data loaded successfully!")

if __name__ == "__main__":
    app.run(debug=True)
