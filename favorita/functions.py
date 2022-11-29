from prophet import Prophet
import pandas as pd

def drop_rename_columns(df):
    """Keep only useful columns for Prophet forecast"""
    df = df[['date', 'sales']]
    df.rename(columns={'date': 'ds', 'sales':'y'}, inplace=True)
    return df

def split_train_test(df):
    """split a dataframe to have train and test value"""
    df_train = df[df['ds']<'2017-04-01']
    df_train.reset_index(drop = True, inplace = True)
    df_test = df[(df['ds']>='2017-04-01')&(df['ds']<'2017-07-01')]
    df_test.reset_index(drop = True, inplace = True)
    return (df_train, df_test)

def forecast_with_Prophet(df_train):
    """Make Prophet forecast"""
    m=Prophet()
    m.fit(df_train)
    future = m.make_future_dataframe(periods=91)
    forecast = m.predict(future)
    return forecast

def MAPE_of_forecast(forecast, df_test):
    """Compute MAPE between forecasted values and actual data"""
    forecast_only = forecast[(forecast['ds']>='2017-04-01')&(forecast['ds']<'2017-07-01')]
    forecast_only.reset_index(drop = True, inplace = True)
    return MAPE(forecast_only['yhat'], df_test['y'])

def MAPE(y_hat, y):
    """Compute the MAPE between two vectors: our prediction and the actual value"""
    return sum(abs((y_hat-y)/y))

def get_baseline_score(df):
    """Re-use all the functions above to directly compute a baseline score of a given dataframe"""
    clean_df = drop_rename_columns(df)
    df_train=split_train_test(clean_df)[0]
    df_test=split_train_test(clean_df)[1]
    forecast=forecast_with_Prophet(df_train)
    return MAPE_of_forecast(forecast, df_test)
