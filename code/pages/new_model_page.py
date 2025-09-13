from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import dash
import numpy as np


from .model_pipeline import predict_car_price_new, fill_missing_values


# ------------------------------
# New Model Page Layout
# ------------------------------
new_model_page = dbc.Container([
    html.H1("New & Improved Car Price Predictor", className="text-center my-4"),

    dbc.Card([
        dbc.CardHeader(html.H4("Why Use the New Model?")),
        dbc.CardBody([
            html.Ul([
                html.Li("✅ Improved accuracy with advanced regularization techniques."),
                html.Li("✅ Better handling of missing values using imputation."),
                html.Li("✅ More robust training (batch, mini-batch, stochastic)."),
                html.Li("✅ Enhanced performance with momentum optimization."),
            ])
        ])
    ], className="mb-4"),


    dbc.Row([
        dbc.Col([
            html.Label("Transmission Type"),
            dcc.Dropdown(
                id="transmission",
                options=[
                    {"label": "Manual", "value": 0},
                    {"label": "Automatic", "value": 1}
                ],
                placeholder="Select Transmission Type (optional)",
                className="mb-3"
            ),

            html.Label("Max Power (bhp)"),
            dcc.Input(
                id="max_power", type="number",
                placeholder="Enter Max Power (optional)",
                className="form-control mb-3"
            ),

            dbc.Button("Predict", id="submit-btn", color="primary", className="mt-3"),
            html.Br(), html.Br(),
            dbc.Button("Try Again", id="try-again-btn", color="warning", className="me-2"),
            dbc.Button("Back to Home", href="/", color="secondary")
        ], md=6)
    ]),

    html.Hr(),
    html.Div(id="prediction-output", className="h4 text-success text-center mt-3")
], className="my-4")

# ------------------------------
# Callbacks for new model
# ------------------------------
def register_new_model_callbacks(app):
    @app.callback(
        Output("transmission", "value"),
        Output("max_power", "value"),
        Output("prediction-output", "children"),
        Input("submit-btn", "n_clicks"),
        Input("try-again-btn", "n_clicks"),
        State("transmission", "value"),
        State("max_power", "value"),
        prevent_initial_call=True
    )
    def handle_prediction_or_reset(submit_clicks, try_again_clicks, transmission, max_power):
        ctx = dash.callback_context

        if not ctx.triggered:
            raise dash.exceptions.PreventUpdate

        button_id = ctx.triggered[0]["prop_id"].split(".")[0]

        if button_id == "submit-btn":
            try:
                # Fill missing values with imputation
                transmission, max_power = fill_missing_values(transmission, max_power)

                # Prepare features
                features = [transmission, max_power]
                #sample = np.array([[1] + features])
                sample = np.array([[1] + features], dtype=np.float64) 
                #sample = np.array([features])
                # Prediction
                prediction = predict_car_price_new(sample)
                return transmission, max_power, f"Predicted Car Price: ${prediction:,.2f}"

            except Exception as e:
                return transmission, max_power, f"Error: {str(e)}"

        elif button_id == "try-again-btn":
            # Reset inputs
            return None, None, ""
