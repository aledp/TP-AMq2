"""
train.py

COMPLETAR DOCSTRING

DESCRIPCIÓN:
AUTOR:
FECHA:
"""

# Imports
import argparse
from io import StringIO
import logging
import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.linear_model import LinearRegression


class ModelTrainingPipeline(object):

    def __init__(self, input_path, model_path):
        # Configuración del sistema de logs
        logging.basicConfig(
            filename='./logs/logging_info_ModelTrain.log',
            level=logging.INFO,
            filemode='w',
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S')

        # seteo de las rutas de input y model
        self.input_path = input_path
        self.output_path = model_path
         

    def read_data(self) -> pd.DataFrame:
        """
        COMPLETAR DOCSTRING

        :return pandas_df: The desired DataLake table as a DataFrame
        :rtype: pd.DataFrame
        """

        # Cargar los datos de input
        processed_data_df = pd.read_csv(self.input_path)

        # loggin
        buf = StringIO()
        processed_data_df.info(buf=buf)
        logging.info("Carga de datos completa. Dataset info:\n%s",
                     buf.getvalue())

        return processed_data_df

    def model_training(self, processed_data_df: pd.DataFrame):
        """
        COMPLETAR DOCSTRING

        """
        # ----- division en train y test -----

        # Elimnar columnas que son muy específicas
        df_dataset = processed_data_df.drop(
            columns=['Item_Identifier', 'Outlet_Identifier'])

        # División del dataset de train y test
        df_train = df_dataset.loc[df_dataset['Set'] == 'train']
        df_test = df_dataset.loc[df_dataset['Set'] == 'test']

        # Eliminando columnas sin datos
        df_train.drop(['Set'], axis=1, inplace=True)
        df_test.drop(['Item_Outlet_Sales', 'Set'], axis=1, inplace=True)
        # ver / oportunidad de mejora: estas sentencias arrojan warnings.

        # loggin
        logging.info('Division en train y test exitosa')
        logging.info("Tamaño Train set:\n%s", df_train.shape)
        logging.info("Tamaño Test set :\n%s", df_test.shape)

        # ----- entrenamiento del modelo -----

        seed = 28
        model = LinearRegression()

        # División de dataset de entrenaimento y validación
        df_train_features = df_train.drop(columns='Item_Outlet_Sales')
        x_train, x_val, y_train, y_val = train_test_split(
            df_train_features, df_train['Item_Outlet_Sales'], test_size=0.3, random_state=seed)

        # Entrenamiento del modelo
        model.fit(x_train, y_train)

        # Predicción del modelo ajustado para el conjunto de validación
        y_pred = model.predict(x_val)

        # Cálculo de los errores cuadráticos medios y Coeficiente de Determinación
        # (R^2)
        mse_train = metrics.mean_squared_error(y_train, model.predict(x_train))
        R2_train = model.score(x_train, y_train)

        mse_val = metrics.mean_squared_error(y_val, y_pred)
        R2_val = model.score(x_val, y_val)

        # Logging: metricas del modelo
        logging.info('Métricas del Modelo:')
        logging.info(
            "ENTRENAMIENTO: RMSE: {:.2f} - R2: {:.4f}:\n%s".format(mse_train**0.5, R2_train))
        logging.info(
            "VALIDACIÓN: RMSE: {:.2f} - R2: {:.4f}:\n%s".format(mse_val**0.5, R2_val))
        logging.info('\nCoeficientes del Modelo:')

        # Logging: Constante del modelo
        logging.info("Intersección: {:.2f}:\n%s".format(model.intercept_))

        # Logging: Coeficientes del modelo
        coef = pd.DataFrame(x_train.columns, columns=['features'])
        coef['Coeficiente Estimados'] = model.coef_
        logging.info("Coeficientes del modelo:\n%s", coef)

        # ----- model return -----

        logging.info("Tipo de modelo:\n%s",model)

        return model

    def model_dump(self, model_trained) -> None:
        """
        COMPLETAR DOCSTRING

        """

        # Serialización del modelo
        with open(self.output_path, 'wb') as file_model:
            pickle.dump(model_trained, file_model)
            file_model.close()

        return None

    def run(self):

        processed_data = self.read_data()
        model_trained = self.model_training(processed_data)
        self.model_dump(model_trained)


if __name__ == "__main__":

    # Parser de argumentos
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", "-i", required=True,
                        help="Path to the first input")
    parser.add_argument("--model", "-m", required=True,
                        help="Path to the output model")

    # Parsear los argumentos de la línea de comandos
    args = parser.parse_args()

    # run ModelTrainingPipeline
    ModelTrainingPipeline(
        input_path=args.input,
        model_path=args.model).run()
