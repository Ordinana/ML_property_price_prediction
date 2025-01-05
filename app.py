import streamlit as st
import pandas as pd
import joblib

def main():
    # Estilo general
    st.markdown(
        """
        <style>
        .title {
            font-size: 28px;
            font-weight: bold;
            text-align: center;
            color: white;
            background-color: #4e7c3f;
            padding: 10px;
            border-radius: 10px;
        }
        .subtitle {
            font-size: 22px;
            text-align: center;
            color: #4e7c3f;
            margin-bottom: 12px;
        }
        .stButton button {
            background-color: #4e7c3f;
            color: white;
            border-radius: 5px;
            font-size: 16px;
        }
        .stButton button:hover {
            background-color: #1D5C3A;
            color: white;
        }
        .block-container {
            background-color: #F5F5F5;
            padding: 20px;
            border-radius: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Añadir logotipo
    st.image("./imgs/logo_futurcasa.png", use_container_width=True)

    # Título de la aplicación
    st.markdown(
        """
        <div class="title">Sistema de Tasación de Viviendas</div>
        <div class="subtitle">Introduce los detalles de la vivienda para obtener una tasación estimada.</div>
        """,
        unsafe_allow_html=True
    )

    # Cargar modelo, encoders y scaler
    modelo = joblib.load("./model/Gradient_XGB_model.pkl")
    label_encoders = joblib.load("./model/label_encoders.pkl")
    scaler = joblib.load("./model/scaler_voting.pkl")

    # Diseño de entrada en 2 filas y 5 columnas
    cols = st.columns(5)

    municipio = cols[0].selectbox("Municipio", label_encoders['municipio'].classes_)
    tipo_vivienda = cols[1].selectbox("Tipo de vivienda", label_encoders['tipo_vivienda'].classes_)
    habitaciones = cols[2].number_input("Habitaciones", min_value=1, step=1)
    metros_cuadrados = cols[3].number_input("Metros cuadrados", min_value=25, step=1)
    aseos = cols[4].number_input("Aseos", min_value=1, step=1)

    cols = st.columns(5)

    # Condicionales según el tipo de vivienda
    if tipo_vivienda in ['Piso', 'Estudio']:
        planta = cols[0].number_input("Planta", min_value=1, step=1)
        zona_centro = cols[1].selectbox("¿Zona centro?", ['Sí', 'No'])
        terraza = cols[2].selectbox("¿Terraza?", ['Sí', 'No'])
    elif tipo_vivienda == 'Casa':
        planta = 0  # No aplica
        zona_centro = cols[1].selectbox("¿Zona centro?", ['Sí', 'No'])
        terraza = cols[2].selectbox("¿Terraza?", ['Sí', 'No'])
    else:
        planta = 0  # Valor predeterminado para viviendas donde no aplica
        zona_centro = 'No'  # Valor predeterminado para viviendas fuera de zona centro
        terraza = 'No'  # Valor predeterminado

    garaje = cols[3].selectbox("¿Garaje?", ['Sí', 'No'])

    # Aire acondicionado temporalmente a "No"
    aire_acondicionado = "No"
    # aire_acondicionado = cols[4].selectbox("¿Aire acondicionado?", ['Sí', 'No'])

    # Crear DataFrame con los datos ingresados
    nueva_vivienda = pd.DataFrame({
        'municipio': [municipio],
        'tipo_vivienda': [tipo_vivienda],
        'habitaciones': [habitaciones],
        'metros_cuadrados': [metros_cuadrados],
        'aseos': [aseos],
        'planta': [planta],
        'garaje': [garaje],
        'zona_centro': [zona_centro],
        'terraza': [terraza],
        'aire_acondicionado': [aire_acondicionado]
    })

    # Botón para realizar la predicción
    if st.button("Calcular Tasación"):
        # Codificación y escalado
        nueva_vivienda_codificada = codificacion_y_escalado(nueva_vivienda, label_encoders, scaler)

        # Métricas del modelo
        mae = 57174.55  # Cambia esto si tienes otros valores
        mape = 0.32931

        # Predicción e intervalos
        prediccion, intervalo_mae, intervalo_mape = prediccion_con_intervalo(modelo, nueva_vivienda_codificada, mae, mape)

        # Mostrar resultados
        st.subheader("Resultados de la Tasación")
        st.write(f"Precio estimado: **{prediccion:,.2f} euros**")
        st.write(f"Intervalo basado en MAE: **({intervalo_mae[0]:,.2f} - {intervalo_mae[1]:,.2f}) euros**")
        st.write(f"Intervalo basado en MAPE: **({intervalo_mape[0]:,.2f} - {intervalo_mape[1]:,.2f}) euros**")

# Funciones de codificación y predicción
def codificacion_y_escalado(nueva_vivienda, label_encoders, scaler):
    binary_mappings = {
        'zona_centro': {'Sí': 1, 'No': 0},
        'terraza': {'Sí': 1, 'No': 0},
        'aire_acondicionado': {'Sí': 1, 'No': 0}
    }

    # Aplica el mapeo a las columnas binarias
    for col, mapping in binary_mappings.items():
        nueva_vivienda[col] = nueva_vivienda[col].map(mapping)

    # Aplica la codificación a las columnas categóricas
    categoricas = ['municipio', 'tipo_vivienda', 'garaje']
    for col in categoricas:
        le = label_encoders[col]
        nueva_vivienda[col] = nueva_vivienda[col].apply(lambda x: x if x in le.classes_ else 'Otro')
        nueva_vivienda[col] = le.transform(nueva_vivienda[col])

    # Escalado
    columnas_ordenadas = scaler.feature_names_in_
    nueva_vivienda = nueva_vivienda[columnas_ordenadas]
    nueva_vivienda_escalada = scaler.transform(nueva_vivienda)
    return nueva_vivienda_escalada

def prediccion_con_intervalo(modelo, nueva_vivienda, mae, mape):
    prediccion = modelo.predict(nueva_vivienda)[0]
    intervalo_mae = (prediccion - mae, prediccion + mae)
    intervalo_mape = (prediccion * (1 - mape), prediccion * (1 + mape))
    return prediccion, intervalo_mae, intervalo_mape

if __name__ == "__main__":
    main()
