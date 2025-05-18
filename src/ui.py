from shiny import ui

app_ui = ui.page_sidebar(
    # Menú lateral
    ui.sidebar(
        # Selección de período de tiempo
        ui.input_slider("periodo", "Período de tiempo", min=2021, max=2025, value=(2021, 2025), sep=""),
        # Tipo de vehículo
        ui.input_select("tipo", "Seleccionar tipo:", choices=[
            "AUTOS", "MOTOS", "AUTOBUS DE 2 EJES", "AUTOBUS DE 3 EJES", "AUTOBUS DE 4 EJES",
            "CAMIONES DE 2 EJES", "CAMIONES DE 3 EJES", "CAMIONES DE 4 EJES", "CAMIONES DE 5 EJES",
            "CAMIONES DE 6 EJES", "CAMIONES DE 7 EJES", "CAMIONES DE 8 EJES", "CAMIONES DE 9 EJES",
            "EJE EXTRA AUTOBUS", "EJE EXTRA CAMION", "PEATONES", "TRICICLOS"
        ]),
        # Selección de mes
        ui.input_select("mes", "Meses:", choices=[str(i) for i in range(1, 13)], selected="1"),
        # Selección de año
        ui.input_select("anio", "Seleccionar año:", choices=[str(a) for a in range(2021, 2026)], selected="2021"),
        # Grupo de tipos de vehículo
        ui.input_checkbox_group("tipos_hist", None, choices={
            "AUTOS": "Auto",
            "MOTOS": "Moto",
            "AUTOBUS DE 2 EJES": "Autobús de 2 ejes",
            "AUTOBUS DE 3 EJES": "Autobús de 3 ejes",
            "AUTOBUS DE 4 EJES": "Autobús de 4 ejes",
            "CAMIONES DE 2 EJES": "Camión de 2 ejes",
            "CAMIONES DE 3 EJES": "Camión de 3 ejes",
            "CAMIONES DE 4 EJES": "Camión de 4 ejes",
            "CAMIONES DE 5 EJES": "Camión de 5 ejes",
            "CAMIONES DE 6 EJES": "Camión de 6 ejes",
            "CAMIONES DE 7 EJES": "Camión de 7 ejes",
            "CAMIONES DE 8 EJES": "Camión de 8 ejes",
            "CAMIONES DE 9 EJES": "Camión de 9 ejes",
            "EJE EXTRA AUTOBUS": "Eje extra autobús",
            "EJE EXTRA CAMION": "Eje extra camión",
            "PEATONES": "Peatones",
            "TRICICLOS": "Triciclos"
        })
    ),
    # Contenido principal
    ui.column(12,
        # Fila 1: Tarjetas de resumen      
        ui.row(
            ui.layout_columns(
                # Tarjeta 1: Total de vehículos dependiendo del tipo
                ui.card(
                    ui.div(
                        ui.HTML('<img src="https://img.icons8.com/ios-filled/50/car--v1.png" width="30">'),
                        ui.div(ui.output_text("titulo_total_vehiculo"), class_="fw-bold text-primary"),
                        ui.h3(ui.output_text("total_vehiculo"), class_="fw-bold"),
                        class_="text-center",
                        style="height: 100%;"
                    ),
                    class_="p-3 shadow-sm",
                    style="height: 100px;"
                ),
                # Tarjeta 2: Frecuencia
                ui.card(
                    ui.div(
                        ui.HTML('<img src="https://img.icons8.com/ios-filled/50/calendar--v1.png" width="30">'),
                        ui.div("Frecuencia", class_="fw-bold text-primary"),
                        ui.h3(ui.output_text("frecuencia"), class_="fw-bold"),
                        class_="text-center",
                        style="height: 100%;"
                    ),
                    class_="p-3 shadow-sm",
                    style="height: 100px;"
                ),
                # Tarjeta 3: Pronóstico dependiendo del tipo y el mes a futuro
                ui.card(
                    ui.div(
                        ui.HTML('<img src="https://img.icons8.com/ios-filled/50/car--v1.png" width="30">'),
                        ui.div(ui.output_text("titulo_pronostico"), class_="fw-bold text-primary"),
                        ui.h3(ui.output_text("pronostico"), class_="fw-bold"),
                        class_="text-center",
                        style="height: 100%;"
                    ),
                    class_="p-3 shadow-sm",
                    style="height: 100px;"
                )
            ),
            style="min-height: 200px;"
        ),
        # Fila 2: Datos
        ui.row(
            ui.column(6,
                # Tarjeta 1: Tabla de datos filtrados
                ui.card(
                    ui.h5("Conjunto de datos"),
                    ui.output_data_frame("tabla_datos_filtrados"),
                    class_="p-3"
                )
            ),
            ui.column(6,
                # Tarjeta 2: Gráfico de predicción con historial
                ui.card(
                    ui.h5("Pronóstico (Mes)"),
                    ui.output_plot("grafico_prediccion"),
                    class_="p-3"
                )
            )
        ),
        # Fila 3: Resumen de datos
        ui.row(
            # Columna 1: Gráfico de frecuencias por tipo de vehículo seleccionado
            ui.column(6,
                ui.card(
                    ui.h5("Frecuencias de tipos de vehículo por año"),
                    ui.output_plot("grafico_histograma"),
                    class_="p-3"
                )
            ),
            # Columna 2: Lista de cantidades por tipo de vehículo seleccionado
            ui.column(3,
                ui.card(
                    ui.h5("Cantidad de vehículos"),
                    ui.output_ui("resumen_vehiculos"),
                    class_="p-3"
                )
            ),
            # Columna 3: Estadísticas mayor/menor por tipo de vehículo seleccionado
            ui.column(3,
                ui.card(
                    ui.h5("Estadísticas:"),
                    ui.div("Tipo de vehículo con mayor movimiento:", class_="fw-bold text-primary"),
                    ui.output_text("vehiculo_mayor"),
                    ui.br(),
                    ui.div("Tipo de vehículo con menor movimiento:", class_="fw-bold text-primary"),
                    ui.output_text("vehiculo_menor"),
                    class_="p-3"
                )
            )
        ),
    ),
    title="Movimientos mensuales por tipo de vehículo en la red CAPUFE",
)
