UBA-LSE-IA

Trabajo final de Aprendizaje Máquina II

Integrantes:

* Del Porto, María Alejandra

* Munar, Juan Ignacio

----------

La consigna del trabajo práctico está detallada en "AMq2-TP integrador.pdf"

Principalmente consiste en la refactorización del código en "notebook_analysis_train.ipynb" cual fue desarrolado por un tercero.

-----------

Machine Learning para BigMart

Este proyecto de Machine Learning se enfoca en predecir las ventas de productos en las tiendas BigMart. Está compuesto de los scripts:

## `train_pipeline.py`

Este script orquesta el proceso de entrenamiento del modelo. Primero, ejecuta el script de ingeniería de características y luego entrena el modelo utilizando el dataset procesado.

Las rutas para la lectura y escritura de de archivos se pasan como argumentos en las llamadas a las funciones que están en este script.

## `inference_pipeline.py`

Este script lleva a cabo el proceso de inferencia, es decir, predice las ventas de productos basado en un conjunto de datos que se pasa como entrada. Al igual que el script de entrenamiento, comienza ejecutando el script de feature_engineering y luego utiliza el modelo previamente entrenado para hacer predicciones.

Las rutas para la lectura y escritura de de archivos se pasan como argumentos en las llamadas a las funciones que están en este script.

## `feature_engineering.py`

Este script realiza varias etapas de preprocesamiento y de feature_engineering en un conjunto de datos CSV.

Los argumentos que deben pasarse al llamar a la funcion run de este módulo son:

* input1: Ruta al archivo CSV con los datos de entrenamiento o el total del dataset 

* input2 (opcional): Ruta al archivo CSV del dataset de test.

* output: Ruta para guardar el dataset procesado (FE_TrainPipe_processed_data.csv para entrenamiento, FE_InferencePipe_processed_data.csv para inferencia)


* Archivo de logs:
Se genera un archivo de log para cada ejecución con el nombre especificado (logging_info_FE_TrainPipe para entrenamiento, logging_info_FE_InferencePipe para inferencia).

## `train.py`

Este script se encarga del entrenamiento de un modelo de regresión lineal utilizando el dataset procesado generado previamente por `feature_engineering.py`.

Los argumentos que deben pasarse al llamar a la funcion run de este módulo son:

* input: Ruta al archivo CSV de datos procesados

* model: Ruta para guardar el modelo entrenado en formato pickle (modeloDump.pkl)

* Archivo de logs:

El archivo de logs se guarda como logging_info_ModelTrain.log.


## `predict.py`

Este script realiza la predicción de las ventas de productos utilizando el modelo entrenado y el dataset de procesado que se pasó como entrada.

Los argumentos que deben pasarse al llamar a la funcion run de este módulo son:

* input: Ruta al archivo CSV de datos procesados para inferencia

* model: Ruta al modelo entrenado en formato pickle

* output: Ruta para guardar el archivo CSV con las predicciones (predicted_data.csv)


* Archivo de logs:

El archivo de logs se guarda como logging_info_predict.log.




