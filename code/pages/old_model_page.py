# pages/old_model_page.py
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import dash
import numpy as np
from .model_pipeline import predict_car_price, fill_missing_values

# ------------------------------
# Old Model Page Layout
# ------------------------------
old_model_page = dbc.Container([
    html.H1("Old Car Price Predictor", className="text-center my-4"),
    html.P(
        "This is our earlier version of the predictor. It provides basic predictions but lacks "
        "the advanced imputation, regularization, and optimization used in the new version.",
        className="lead text-center mb-4"
    ),

    dbc.Row([
        dbc.Col([
            html.Label("Transmission Type"),
            dcc.Dropdown(
                id="transmission_old",
                options=[
                    {"label": "Manual", "value": 0},
                    {"label": "Automatic", "value": 1}
                ],
                placeholder="Select Transmission Type (optional)",
                className="mb-3"
            ),

            html.Label("Max Power (bhp)"),
            dcc.Input(
                id="max_power_old", type="number",
                placeholder="Enter Max Power (optional)",
                className="form-control mb-3"
            ),

            dbc.Button("Predict", id="submit_old", color="primary", className="mt-3"),
            html.Br(), html.Br(),
            dbc.Button("Try Again", id="try_again_old", color="warning", className="me-2"),
            dbc.Button("Back to Home", href="/", color="secondary")
        ], md=6)
    ]),

    html.Hr(),
    html.Div(id="prediction_output_old", className="h4 text-success text-center mt-3")
], className="my-4")

# ------------------------------
# Old Model Callbacks
# ------------------------------
def register_old_model_callbacks(app):
    @app.callback(
        Output("transmission_old", "value"),
        Output("max_power_old", "value"),
        Output("prediction_output_old", "children"),
        Input("submit_old", "n_clicks"),
        Input("try_again_old", "n_clicks"),
        State("transmission_old", "value"),
        State("max_power_old", "value"),
        prevent_initial_call=True
    )
    def handle_prediction_or_reset(submit_clicks, try_again_clicks, transmission, max_power):
        ctx = dash.callback_context
        if not ctx.triggered:
            raise dash.exceptions.PreventUpdate

        button_id = ctx.triggered[0]["prop_id"].split(".")[0]

        if button_id == "submit_old":
            try:
                # Fill missing values if user didn't input them
                transmission, max_power = fill_missing_values(transmission, max_power)

                # Prepare features
                sample = np.array([[transmission, max_power]])  # 2 features as expected by old model

                # Predict
                prediction = predict_car_price(sample)
                return transmission, max_power, f"Predicted Car Price: ${prediction:,.2f}"

            except Exception as e:
                return transmission, max_power, f"Error: {str(e)}"

        elif button_id == "try_again_old":
            # Reset inputs
            return None, None, ""
