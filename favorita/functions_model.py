import pandas as pd
from prophet.diagnostics import cross_validation, performance_metrics
from prophet import Prophet
from favorita.functions import *
from sklearn.model_selection import ParameterGrid

def store_selection(store_selected):
    #preprocess for the whole dataframe
    #df_main =pd.read_csv('Data/df_main_V4.csv')
    #df_main_store = df_main.groupby(['date','store_nbr']).agg({'sales':'sum', 'onpromotion':'sum', 'is_holiday':'mean', 'dcoilwtico':'mean'})
    #df_main_store.reset_index(inplace=True)
    #df_main_store=df_main_store[df_main_store['store_nbr']==store_selected]
    #df_main_store = df_main_store[df_main_store['date']<'2017-04-01']
    #df_main_store.rename(columns = {'date':'ds', 'sales':'y'}, inplace=True)
    #df_main_store.drop(columns = ['store_nbr'], inplace=True)

    #preprocess for the dataframe selected by store
    df =pd.read_csv("Data/data_pulled_from_GCP/"f'store{store_selected}')
    df = df[df['date']<'2017-04-01']
    df.rename(columns = {'date':'ds', 'sales':'y'}, inplace=True)
    df.drop(columns = ['store_nbr'], inplace=True)
    df.reset_index(drop=True, inplace=True)
    #return df_main_store
    return df

def grid_search(df):

# Create parameter grid
    params_grid = {'seasonality_mode':(['multiplicative']),
               'changepoint_prior_scale':[0.05, 0.08, 0.11],
               'seasonality_prior_scale':[0.05, 0.08, 0.11],
               'prior_scale_is_holiday':[0.01, 0.5, 0.1],
               'prior_scale_onpromotion':[0.01, 0.5, 0.1],
               'prior_scale_dcoilwtico':[0.01, 0.5, 0.1],
               'fourier_order':[5]
              }
    #Pour TEST, runs easier
    #params_grid = {'seasonality_mode':(['multiplicative']),
    #       'changepoint_prior_scale':[0.05],
    #       'seasonality_prior_scale':[0.08],
    #       'prior_scale_is_holiday':[0.5],
    #       'prior_scale_onpromotion':[ 0.1],
    #       'prior_scale_dcoilwtico':[0.01],
    #       'fourier_order':[5]
    #          }
# Get all the model parameters in a list of dictionary
    grid = ParameterGrid(params_grid)

    mdape = []  # Store the RMSEs for each params here

    for p in grid:
        m = Prophet(changepoint_prior_scale = p['changepoint_prior_scale'],
                             seasonality_prior_scale = p['seasonality_prior_scale'],
                             seasonality_mode = p['seasonality_mode'],
                             weekly_seasonality=True,
                            daily_seasonality = True,
                             yearly_seasonality = True,
                             interval_width=0.95)
        m.add_regressor('is_holiday', prior_scale = p['prior_scale_is_holiday'])
        m.add_regressor('onpromotion', prior_scale = p['prior_scale_onpromotion'])
        m.add_regressor('dcoilwtico', prior_scale = p['prior_scale_dcoilwtico'])
        m.add_seasonality(name='monthly', period=30.417, fourier_order=p['fourier_order'])
        m.fit(df[['ds', 'y', 'is_holiday', 'onpromotion', 'dcoilwtico']])
        df_cv = cross_validation(m, horizon='91 days',initial = '1095 days', parallel="threads")
        df_p = performance_metrics(df_cv, rolling_window=1)
        mdape.append(df_p['mdape'].values[0])

    # Find the best parameters

    tuning_results = pd.DataFrame(grid)
    tuning_results['mdape'] = mdape
    tuning_results_min= tuning_results[tuning_results['mdape']==tuning_results['mdape'].min()]

    return tuning_results_min

#def pred ():
def get_forecast(df,
                best_params,
                                ):

    m = Prophet(changepoint_prior_scale = best_params.loc[0,'changepoint_prior_scale'],
                seasonality_prior_scale = best_params.loc[0,'seasonality_prior_scale'],
                seasonality_mode = best_params.loc[0,'seasonality_mode'],
                weekly_seasonality=True,
                daily_seasonality = False,
                yearly_seasonality = True,
                interval_width=0.95)
    m.add_regressor('onpromotion', prior_scale = best_params.loc[0,'prior_scale_onpromotion'])
    m.add_regressor('is_holiday', prior_scale = best_params.loc[0,'prior_scale_is_holiday'])
    m.add_regressor('dcoilwtico', prior_scale = best_params.loc[0,'prior_scale_dcoilwtico'])
    m.add_seasonality(name='monthly', period=30.417, fourier_order= best_params.loc[0,'fourier_order'])
    m.fit(df[['ds', 'y', 'is_holiday', 'onpromotion', 'dcoilwtico']])

    #forecast from prophet
    future=m.make_future_dataframe(periods=91, freq= 'D')
    future.insert(1, 'onpromotion', df['onpromotion'])
    future.insert(2, 'is_holiday', df['is_holiday'])
    future.insert(3, 'dcoilwtico', df['dcoilwtico'])
    df_pred= m.predict(future)
    mask = (df_pred['ds'] >='2017-04-01') & (df_pred['ds'] < '2017-06-30')
    df_pred.loc[mask]
    return m, m.predict(future),df_pred.loc[mask]

def regressor_delimitor(df):
    df.reset_index(inplace=True, drop=True)
    df=df.rename(columns={'date':'ds', 'sales':'y'})
    return df
