import os
import shutil

import pandas as pd
from prophet import Prophet
from sklearn.metrics import mean_squared_error

import joblib
import matplotlib.pyplot as plt
from modelo import data_model as data 
 
MODELS_URL = 'modelo\models'
TEST_RESULTS_URL = 'test_results'

VACACIONES = [
    '2022-01-01',  # Año Nuevo
    '2022-02-14',  # Día de San Valentín (movimiento en centros comerciales)
    '2022-03-21',  # Día de Benito Juárez (México) / comienzo primavera
    '2022-04-10',  # Inicio Semana Santa
    '2022-04-14',  # Jueves Santo
    '2022-04-15',  # Viernes Santo
    '2022-05-01',  # Día del Trabajo
    '2022-05-10',  # Día de la Madre (movilidad comercial)
    '2022-06-24',  # Fin del ciclo escolar (aproximado)
    '2022-07-15',  # Vacaciones de verano (inicio)
    '2022-09-15',  # Fiestas patrias (ej. México)
    '2022-10-31',  # Halloween (movilidad en zonas residenciales)
    '2022-11-01',  # Día de Todos los Santos
    '2022-11-02',  # Día de los Muertos
    '2022-11-20',  # Revolución Mexicana / feriados similar
    '2022-12-12',  # Día de la Virgen de Guadalupe (peregrinaciones masivas)
    '2022-12-24',  # Nochebuena
    '2022-12-25',  # Navidad
    '2022-12-31',  # Fin de año
]

def load_models(test = False):
    if test:
        prepare_folder(TEST_RESULTS_URL)

    df = data.load_from_disk()

    for col in data.VALUE_COLUMNS:
        model = generate_model(df, col, test)
        joblib.dump(model, os.path.join(MODELS_URL, F'{col}.pkl'))

def predict(model_name, period):
    model = joblib.load(os.path.join(MODELS_URL, F'{model_name}.pkl'))

    future = model.make_future_dataframe(periods=period, freq='ME')
    forecast = model.predict(future)

    return forecast

def generate_model(df, y, test = False):
    print(F'Generating model... @{y}')

    ts = df.rename(columns={'FECHA': 'ds', y: 'y'})[['ds', 'y']]
    holidays = pd.DataFrame({
        'holiday': 'vacaciones',
        'ds': pd.to_datetime(VACACIONES),  # ejemplo de vacaciones
        'lower_window': 0,
        'upper_window': 1,
    })
    model = Prophet(
        daily_seasonality=False,
        weekly_seasonality=False,
        yearly_seasonality=True,
        changepoint_prior_scale=0.1,
        holidays=holidays, )

    if test:
        train_size = int(len(ts) * 0.8)
        train_df = ts[:train_size]
        test_df = ts[train_size:]

        model.fit(train_df)

        test_model(model, test_df, y)
    else:
        model.fit(ts)

    return model

def test_model(model, test_df, col = 'unknown'):
    future = model.make_future_dataframe(periods=len(test_df), freq='ME')
    forecast = model.predict(future)

    forecast_test = forecast.tail(len(test_df))

    mse = mean_squared_error(test_df['y'], forecast_test['yhat'])
    print(f"Mean Squared Error (MSE): {mse} above {test_df['y'].mean()}")

    plt.plot(test_df['y'].values, label='True Values')
    plt.plot(forecast_test['yhat'].values, label='Predicted Values')
    plt.legend()
    plt.title('True VS Predicted Values')
    plt.savefig(os.path.join(TEST_RESULTS_URL, F'{col}_t-vs-p.png'))
    plt.close()

    errors = test_df['y'] - forecast_test['yhat']
    plt.plot(errors, label='Errors')
    plt.legend()
    plt.title('Predicted Errors')
    plt.savefig(os.path.join(TEST_RESULTS_URL, F'{col}_e-c.png'))
    plt.close()

def prepare_folder(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)

