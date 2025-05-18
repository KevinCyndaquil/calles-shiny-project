from shiny import render, reactive, ui
from modelo.data_model import load_from_disk, predecir_valor, generar_serie_pronostico
from matplotlib.ticker import FuncFormatter
import matplotlib.pyplot as plt
import pandas as pd
import locale

df = load_from_disk()
try:
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
except locale.Error:
    locale.setlocale(locale.LC_TIME, 'C')  # fallback genérico

def server(input, output, session):

    @reactive.Calc
    def datos_filtrados():
        periodo = input.periodo()
        return df[
            (df["AÑO"] >= periodo[0]) &
            (df["AÑO"] <= periodo[1])
        ]

    @output
    @render.text
    def titulo_total_vehiculo():
        tipo = input.tipo()
        return f"Total de {tipo.title()} hasta 2025"

    @output
    @render.text
    def total_vehiculo():
        tipo = input.tipo()
        data = datos_filtrados()

        if tipo in data.columns:
            total = int(data[tipo].sum())
            return f"{total:,}"
        return "No disponible"
    
    @output
    @render.text
    def titulo_pronostico():
        tipo = input.tipo()
        meses = int(input.mes())  # meses a futuro

        try:
            _, fecha = predecir_valor(tipo, meses)
            nombre_mes = fecha.strftime('%B').capitalize()
            anio = fecha.year
            return f"Pronóstico para {nombre_mes} {anio}"
        except Exception:
            return "Fecha inválida"

    @output
    @render.text
    def pronostico():
        tipo = input.tipo()
        meses = int(input.mes())  # meses a futuro

        try:
            valor, _ = predecir_valor(tipo, meses)
            return f"{valor:,}"
        except Exception as e:
            return f"Error: {str(e)}"
        
    @output
    @render.text
    def frecuencia():
        return "1 mes"

    @output
    @render.plot
    def grafico_prediccion():
        tipo = input.tipo()
        meses = int(input.mes())

        try:
            modelo, forecast = generar_serie_pronostico(tipo)
            fig, ax = plt.subplots(figsize=(6, 3.5))
            modelo.plot(forecast, ax=ax)
            fecha_objetivo = modelo.history['ds'].max() + pd.DateOffset(months=meses)
            punto = forecast[forecast["ds"] == fecha_objetivo]

            if not punto.empty:
                y_val = punto["yhat"].values[0]
                ax.plot(fecha_objetivo, y_val, 'ro', markersize=4, label="Pronóstico seleccionado")
                ax.annotate(f"{int(y_val):,}", (fecha_objetivo, y_val), textcoords="offset points", xytext=(0, 10),  ha='center', fontsize=4, color='red')

            ax.set_title(f"Pronóstico para {tipo}")
            ax.set_xlabel("Fecha")
            ax.set_ylabel("Cantidad")
            ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{int(x):,}'))

            if not punto.empty:
                ax.legend(loc="lower right", fontsize=5)

            return fig

        except Exception as e:
            fig, ax = plt.subplots()
            ax.text(0.5, 0.5, str(e), ha='center', va='center', wrap=True)
            ax.set_axis_off()
            return fig
        
    @output
    @render.data_frame
    def tabla_datos_filtrados():
        anio = int(input.anio())
        tipos = input.tipos_hist()  # lista de columnas a mostrar

        if not tipos:
            return pd.DataFrame({"Mensaje": ["Selecciona al menos un tipo de vehículo."]})
    
        df = load_from_disk()
        df = df[df["AÑO"] == anio]

        columnas = ["AÑO", "MES"] + list(tipos)

        # Convertir número de mes a nombre del mes antes de mostrar
        meses_es = {
            1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril',
            5: 'Mayo', 6: 'Junio', 7: 'Julio', 8: 'Agosto',
            9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
        }

        df = df.copy()
        df["MES"] = df["MES"].map(meses_es)

        df_filtrado = df[columnas]
        return df_filtrado
    
    @output
    @render.plot
    def grafico_histograma():
        anio = int(input.anio())
        tipos = input.tipos_hist()

        if not tipos:
            fig, ax = plt.subplots()
            ax.text(0.5, 0.5, "Selecciona al menos un tipo de vehículo", 
                    ha='center', va='center', fontsize=12, wrap=True)
            ax.set_axis_off()
            return fig

        df = load_from_disk()
        df_anio = df[df["AÑO"] == anio]

        # Sumar por tipo
        totales = df_anio[list(tipos)].sum()

        fig, ax = plt.subplots(figsize=(6, 3.5))
        colores = ['steelblue', 'red', 'limegreen', 'gold', 'magenta', 'cyan', 'orange', 'gray', 'purple']
        ax.bar(totales.index, totales.values, color=colores[:len(totales)])

        ax.set_ylabel("Cantidad")
        ax.tick_params(axis='x', labelsize=9, rotation=90)

        ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{int(x):,}'))

        return fig
    
    @output
    @render.ui
    def resumen_vehiculos():
        anio = int(input.anio())
        tipos = input.tipos_hist()

        if not tipos:
            return ui.div("Selecciona al menos un tipo de vehículo")

        df = load_from_disk()
        df_anio = df[df["AÑO"] == anio]
        totales = df_anio[list(tipos)].sum().sort_values(ascending=False)

        # Diccionario de íconos 
        iconos = {
            "AUTOS": "car--v1",
            "MOTOS": "motorcycle",
            "AUTOBUS DE 2 EJES": "bus--v1",
            "AUTOBUS DE 3 EJES": "bus--v2",
            "AUTOBUS DE 4 EJES": "bus",
            "CAMIONES DE 2 EJES": "truck",
            "CAMIONES DE 3 EJES": "truck",
            "CAMIONES DE 4 EJES": "truck",
            "CAMIONES DE 5 EJES": "truck",
            "CAMIONES DE 6 EJES": "truck",
            "CAMIONES DE 7 EJES": "truck",
            "CAMIONES DE 8 EJES": "truck",
            "CAMIONES DE 9 EJES": "truck",
            "TRICICLOS": "tricycle",
            "PEATONES": "user",
            "EJE EXTRA CAMION": "truck",
            "EJE EXTRA AUTOBUS": "bus",
        }

        html = ""
        for tipo, valor in totales.items():
            icono = iconos.get(tipo, "car--v1")  # ícono por defecto
            nombre = tipo.title()
            html += f'''
            <p>
                <img src="https://img.icons8.com/ios-filled/24/{icono}.png" />
                <strong>{nombre}:</strong> {int(valor):,}
            </p>
            '''

        return ui.HTML(html)
    
    @output
    @render.text
    def vehiculo_mayor():
        anio = int(input.anio())
        tipos = input.tipos_hist()

        if not tipos:
            return "Sin selección"

        df = load_from_disk()
        df_anio = df[df["AÑO"] == anio]
        totales = df_anio[list(tipos)].sum()
        tipo_max = totales.idxmax()
        return tipo_max.title()


    @output
    @render.text
    def vehiculo_menor():
        anio = int(input.anio())
        tipos = input.tipos_hist()

        if not tipos:
            return "Sin selección"

        df = load_from_disk()
        df_anio = df[df["AÑO"] == anio]
        totales = df_anio[list(tipos)].sum()
        tipo_min = totales.idxmin()
        return tipo_min.title()





