![alt text](imgs/logo_futurcasa.png)
# **Sistema de Tasación de Viviendas**

### Este proyecto consiste en el desarrollo de un **sistema automático de tasación de viviendas basado en técnicas de Machine Learning**. Con un ***modelo predictivo entrenado* con datos de viviendas reales, el sistema estima el precio de una propiedad en función de sus características**. Muy pronto el sistema estará desplegado en una aplicación interactiva mediante **Streamlit**, donde los usuarios podrán introducir los detalles de una vivienda y obtener una estimación junto con intervalos de confianza.

---

## **1. Motivación**

### El objetivo de este proyecto es proporcionar una herramienta rápida y precisa para estimar el precio de una vivienda, facilitando el trabajo a inmobiliarias, compradores y vendedores. Se pretende sustituir la intuición y los cálculos manuales por una metodología científica y datos.

---

## **2. Datos utilizados**

### El conjunto de datos incluye información de más de 1,100 viviendas, con un rango de precios entre **11,800 y 950,000 euros**. Las principales columnas incluyen:

- ### **Municipio:** Localización de la vivienda.
- ### **Tipo de vivienda:** Casa, piso, chalet, etc.
- ### **Número de habitaciones, aseos y metros cuadrados.**
- ### **Extras:** Garaje, terraza, aire acondicionado, zona centro, entre otros.

### Se eliminaron variables no relevantes como "piscina", "ascensor" y "reformado", y se llevaron a cabo tareas de codificación, normalización y eliminación de outliers.

---

## **3. Modelos utilizados**

### Se probaron varios modelos y combinaciones:

- ### **Gradient Boosting Regressor**: Modelo base con ajustes iniciales.
- ### **XGBoost Regressor**: Por su eficiencia en datos estructurados.
- ### **Voting Regressor**: Combinación de ambos modelos con pesos personalizados (Gradient Boosting: 0.2, XGBoost: 1).

### Métricas finales del modelo:
- ### **MAE:** 57,174.55
- ### **MAPE:** 0.3293 (32.93%)
- ### **RMSE:** 79,853.99
- ### **R2:** 0.8041 (80.41%)

#### Estas métricas indican que el modelo tiene una buena capacidad predictiva, aunque con margen de mejora en el futuro.

---

## *4. Desarrollo de la aplicación*

### **La aplicación con desarrollo en **Streamlit** permitirá la interacción del usuario**. Algunas de sus características clave:

- ### ***Interfaz intuitiva:*** Los usuarios pueden seleccionar características como "Municipio" y "Tipo de vivienda" mediante menús desplegables.
- ### ***Condicionales inteligentes:*** Dependiendo del tipo de vivienda, se habilitan o deshabilitan opciones (por ejemplo, "Planta" no aplica para casas o chalets).
- ### ***Resultados detallados:*** Precio estimado con intervalos de confianza basados en MAE y MAPE.

### ***Ajustes visuales:***
- ### Uso de una paleta de colores basada en el logotipo de "FuturCasa".
- ### Logotipo reducido y centrado.
- ### Selectores organizados en filas y columnas para mayor claridad.

---

## **5. Conclusiones y próximos pasos**

### Conclusiones:
- ### El modelo ofrece estimaciones razonablemente precisas, aunque se detectaron relaciones inesperadas en algunas variables, como "Zona centro" y "Planta".
- ### Estas inconsistencias podrían deberse a outliers o falta de datos relevantes.

### Próximos pasos:
1. **Reentrenar el modelo:** Incluir nuevas transformaciones basadas en insights obtenidos (como eliminar relaciones irrelevantes).
2. **Ajustes en la aplicación:** Optimizar el flujo para que las opciones sean más intuitivas y flexibles.
3. **Ampliación del dataset:** Incluir más datos para mejorar la generalización del modelo.
4. **Despliegue en la nube:** Publicar la aplicación para un acceso público mediante plataformas como **Streamlit Cloud** o **AWS**.

---

## **6. Requisitos del proyecto**

- **Librerías:** Pandas, Scikit-learn, Matplotlib, Seaborn ,Streamlit
- **Archivos necesarios:**
  - ### `Gradient_XGB_model.pkl`: Modelo entrenado.
  - ### `label_encoders.pkl`: Codificadores de variables categóricas.
  - ### `scaler_voting.pkl`: Escalador para normalizar datos.

---

## **7. Uso de la aplicación**

### Para ejecutar el sistema de tasación:

1. ### **Clonar este repositorio.**
2. ### **Instalar dependencias: `pip install -r requirements.txt`**
3. ### **Ejecutar el archivo Streamlit: `streamlit run app.py`**

---

### Este proyecto es una base para futuras mejoras en el ámbito de la predicción inmobiliaria, ofreciendo un equilibrio entre técnicas de Machine Learning avanzadas y una experiencia de usuario optimizada.

- ## ***Presentacion con Gamma:*** https://gamma.app/docs/Tasacion-Automatica-de-Viviendas-para-FuturCasa-62nqt7sw22z685w