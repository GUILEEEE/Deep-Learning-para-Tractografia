# Deep Learning para Tractografía Basada en Streamlines

Este proyecto explora el uso de **deep learning** para la reconstrucción de tractos cerebrales a partir de imágenes de resonancia magnética por difusión (DWI). A través de un modelo de **perceptrón multicapa (MLP)**, se entrenó una red neuronal capaz de predecir direcciones locales de propagación y generar tractogramas de manera automática.

---

## ⚙️ Metodología

1. **Preprocesamiento de datos**
   - Se utilizaron dos archivos: ismrm2015_withReversed__peaks.nii.gz y 2_filtered_loops.trk. Dichos datos fueron preprocesados y curado por expertos en neuroimagen y fueron obtenidos de la [base de datos de Tractometer](https://tractometer.org/ismrm2015/processed_data/).
.
   - Del archivo ismrm2015_withReversed__peaks.nii.gz se obtuvieron se generaron 100 mil vecindades cúbicas de **picos de funciones de distribución de orientación (fODFs)** centradas en un punto y de los streamlines del archivo 2_filtered_loops.trk se extrajeron los vectores de direccion previa y actual en dicho punto.

2. **Generación de datos de entrenamiento**
   - Cada muestra de entrenamiento corresponde a una tupla `(vecindad+direccion_previa, dirección_actual)` extraída de los picos de ODF y de los streamlines del tractograma validado por expertos.

3. **Modelo**
   - Se implementó un **Perceptrón Multicapa (MLP)**.
   - La arquitectura incluye capas lineales, funciones de activación ReLU y dropout para evitar sobreajuste.

4. **Tracking**
   - El modelo predice la dirección de propagación de cada nuevo punto de un streamline basado en la ecuación de propagación dada por:
     $$
     \mathbf{p}_{nuevo} = \mathbf{p}_{actual} + a \mathbf{d},
     $$
     donde $\mathbf{p}_{nuevo}$ es el punto nuevo a actualizar, $\mathbf{p}_{actual}$ el punto actual centro de la vecindad, $a$ el tamaño de paso y $\mathbf{d}$ la dirección estimada por el modelo preentrenado.
   - Se implementó un algoritmo de tracking que actualiza posiciones siguiendo las predicciones de un modelo MLP que extrae una vecindad y dirección previa del punto dado.

---

## 📊 Resultados

- El modelo alcanzó un **error angular promedio de 15.3°** en pruebas de validación.
- Los tractogramas generados lograron reconstruir tractos principales como:
  - **Tracto corticoespinal**  
  - **Cuerpo calloso**
- Se generaron tractogramas de hasta **100,000 streamlines** utilizando el modelo entrenado.
- Limitaciones actuales:
  - Presencia de falsos positivos a nivel local.
  - Ausencia de una rutina de selección de tractos posterior al tracking.

---

## 🔮 Trabajo Futuro

- Incorporar un módulo de **selección de tractos** para reducir falsos positivos.
- Explorar **arquitecturas con memoria** (RNNs, LSTMs, Transformers) para mejorar la consistencia de trayectorias.
- Evaluar métricas adicionales que capturen la calidad topológica de los tractogramas.

---

## 📚 Referencias

1. Derek K. Jones (ed.), *Diffusion MRI: Theory, Methods, and Applications*. Oxford Academic, 2010.  
   https://doi.org/10.1093/med/9780195369779.001.0001  

2. Davood Karimi, Simon K. Warfield. *Diffusion MRI with machine learning*. Imaging Neuroscience 2024; 2: 1–55.  
   https://doi.org/10.1162/imag_a_00353  

---

## 👨‍💻 Autor

**Guillermo Sierra Vargas**  
Centro de Investigación en Matemáticas – Unidad Monterrey  

Asesores:  
- Ángel Ramón Aranda Campos (CIMAT Mérida)  
- Miguel Ángel Uh Zapata (CIMAT Mérida)  
