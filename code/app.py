from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc

# Import page layouts
from pages.new_model_page import new_model_page, register_new_model_callbacks
from pages.old_model_page import old_model_page

# Initialize Dash app
app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True
)
app.title = "Car Price Predictor"

# Layout with URL routing
app.layout = dbc.Container([
    dcc.Location(id="url", refresh=False),
    html.Div(id="page-content")
], fluid=True)

# ------------------------------
# Home Page Layout
# ------------------------------
home_page = dbc.Container([
    html.H1("Welcome to Car Price Predictor", className="text-center my-5"),

    html.P(
        "We’ve deployed our machine learning model here so you can easily make predictions "
        "about car prices right from your browser. No technical background needed—just follow the steps!",
        className="lead text-center mb-4"
    ),

    # --------------------------
    # How Prediction Works
    # --------------------------
    dbc.Card([
        dbc.CardHeader(html.H4("How Prediction Works")),
        dbc.CardBody([
            html.Ol([
                html.Li("Select either new or old machine learning model for the car price prediction."),
                html.Li("Navigate to the respective model prediction page."),
                html.Li([
                    "Enter the values you know to the two input fields:",
                    html.Ul([
                        html.Li("Transmission: Manual or Automatic"),
                        html.Li("Engine Power: Maximum engine power in bhp")
                    ])
                ]),
                html.Li("Leave fields blank if you don’t know them — the system will handle it."),
                html.Li("Click 'Predict' to see the estimated car price. The model outputs an estimated car price in dollars."),
                html.Li("Click 'Try Again' to reset the form.")
            ])
        ])
    ], className="mb-4"),

    # --------------------------
    # Navigation Section
    # --------------------------
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardHeader(html.H4("Navigation")),
            dbc.CardBody([
                html.P("Choose which version of the predictor you’d like to try:"),

                # Old Model Button + Tooltip
                dbc.Button("Old Model", id="old-btn", href="/old_model_page",
                           color="secondary", className="me-2"),
                dbc.Tooltip(
                    "This is our earlier version of the predictor. "
                    "It provides basic predictions but lacks the advanced imputation, "
                    "regularization, and optimization used in the new version.",
                    target="old-btn"
                ),

                # New Model Button + Tooltip
                dbc.Button("New Model", id="new-btn", href="/new_model_page",
                           color="primary"),
                dbc.Tooltip(
                    "This is our optimized model using regularization and hyperparameter search. "
                    "It provides more accurate and robust predictions.",
                    target="new-btn"
                )
            ])
        ]), width=12)
    ])
], className="my-4")

# ------------------------------
# Routing Callback
# ------------------------------
@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname")
)
def display_page(pathname):
    if pathname == "/old_model_page":
        return old_model_page
    elif pathname == "/new_model_page":
        return new_model_page
    return home_page

# Register callbacks for new model page
register_new_model_callbacks(app)

# ------------------------------
# Run the app
# ------------------------------
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8050)
