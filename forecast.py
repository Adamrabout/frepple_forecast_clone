import pandas as pd
from prophet import Prophet

def generate_forecast(df):
    df['ds'] = pd.to_datetime(df['date'])  # Ensure date is in correct format
    df['y'] = df['sales']  # Assuming 'sales' is the column with sales data

    # Create a Prophet model and fit the data
    model = Prophet()
    model.fit(df)

    # Forecast for the next year
    future = model.make_future_dataframe(periods=365)
    forecast = model.predict(future)
    return forecast
