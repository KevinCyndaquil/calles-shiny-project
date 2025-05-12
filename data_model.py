import pandas as pd

DATA_URL = 'data.csv'

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