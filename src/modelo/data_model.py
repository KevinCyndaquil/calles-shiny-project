import pandas as pd
import joblib
import pickle
import os
from prophet import Prophet

DATA_URL = 'modelo/data.csv'

ID_COLUMNS = [
    'NOMBRE',
    'TIPO',
    'FECHA',
] 
VALUE_COLUMNS = [
    'AUTOS',
    'MOTOS',
    'AUTOBUS DE 2 EJES',
    'AUTOBUS DE 3 EJES',
    'AUTOBUS DE 4 EJES',
    'CAMIONES DE 2 EJES',
    'CAMIONES DE 3 EJES',
    'CAMIONES DE 4 EJES',
    'CAMIONES DE 5 EJES',
    'CAMIONES DE 6 EJES',
    'CAMIONES DE 7 EJES',
    'CAMIONES DE 8 EJES',
    'CAMIONES DE 9 EJES',
    'TRICICLOS',
    'EJE EXTRA AUTOBUS',
    'EJE EXTRA CAMION',
    'PEATONES',
]
MESES = {
    'ENERO': 1,
    'FEBRERO': 2,
    'MARZO': 3,
    'ABRIL': 4,
    'MAYO': 5,
    'JUNIO': 6,
    'JULIO': 7,
    'AGOSTO': 8,
    'SEPTIEMBRE': 9,
    'OCTUBRE': 10,
    'NOVIEMBRE': 11,
    'DICIEMBRE': 12,
}

def load_from_disk():
    df = pd.read_csv(DATA_URL, encoding='latin1')

    for col in VALUE_COLUMNS:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    df = df.groupby(['AÑO', 'MES'])[VALUE_COLUMNS].sum().reset_index()

    df['MES'] = df['MES'].str.upper().map(MESES)
    df['FECHA'] = pd.to_datetime(dict(year=df['AÑO'], month=df['MES'], day=1))
    df.sort_values('FECHA', inplace=True)

    return df

def load_monthly(month):
    df = load_from_disk()

    return df[df['FECHA'] == month]

def count_by_year(year):
    df = load_from_disk()

    return df[df['AÑO'] == year]

def predecir_valor(tipo, mes=1):
    ruta_modelo = f"modelo/models/{tipo}.pkl"

    if not os.path.exists(ruta_modelo):
        raise FileNotFoundError(f"Modelo no encontrado para {tipo}")

    try:
        modelo = joblib.load(ruta_modelo)
    except Exception:
        with open(ruta_modelo, "rb") as f:
            modelo = pickle.load(f)

    if not isinstance(modelo, Prophet):
        raise TypeError("Modelo no es Prophet válido")

    fecha_base = modelo.history['ds'].max()  # Último mes registrado
    fecha_objetivo = fecha_base + pd.DateOffset(months=mes)

    if mes < 1 or mes > 12:
        raise ValueError("Solo se permite predecir de 1 a 12 meses después del último dato")

    future = modelo.make_future_dataframe(periods=mes, freq="MS")
    forecast = modelo.predict(future)

    valor = forecast[forecast["ds"] == fecha_objetivo]["yhat"]
    if valor.empty:
        raise ValueError("No se encontró predicción exacta para esa fecha")

    return int(valor.iloc[0]), fecha_objetivo


def generar_serie_pronostico(tipo, pasos=12):
    # Retorna el forecast completo (dataframe) y el modelo Prophet entrenado.
    ruta_modelo = f"modelo/models/{tipo}.pkl"

    if not os.path.exists(ruta_modelo):
        raise FileNotFoundError(f"Modelo no encontrado para {tipo}")

    modelo = joblib.load(ruta_modelo)

    if isinstance(modelo, Prophet):
        # Las fechas futuras
        future = modelo.make_future_dataframe(periods=pasos, freq='MS')
        forecast = modelo.predict(future)
        return modelo, forecast
    else:
        raise TypeError("Solo compatible con Prophet en este gráfico")

