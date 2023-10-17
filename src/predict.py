"""
predict.py

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


class MakePredictionPipeline(object):

    def __init__(self, input_path, model_path, output_path, model=None):

        # Configuración del sistema de logs
        logging.basicConfig(
            filename='./logs/logging_info_predict.log',
            level=logging.INFO,
            filemode='w',
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S')

        error_handler = logging.FileHandler('./logs/logging_info_predict.log')
        # Guardará solo mensajes de nivel ERROR
        error_handler.setLevel(logging.ERROR)
        error_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        error_handler.setFormatter(error_formatter)
        # manejador al logger
        logger = logging.getLogger()
        logger.addHandler(error_handler)

        # seteo de las rutas de input y output
        self.input_path = input_path
        self.model_path = model_path
        self.output_path = output_path
        self.model = model

        # Logging
        logging.info("input_path:\n%s", self.input_path)
        logging.info("model_path:\n%s", self.model_path)
        logging.info("output_path:\n%s", self.output_path)

    def load_data(self) -> pd.DataFrame:
        """
        Read the input data from the specified path and return it as a DataFrame.

        :return raw_df: The desired DataLake table as a DataFrame
        :rtype: pd.DataFrame
        """

        data = pd.read_csv(self.input_path)

        # loggin
        buf = StringIO()
        data.info(buf=buf)
        logging.info("Carga de datos completa:\n%s",
                     buf.getvalue())

        return data

    def load_model(self) -> None:
        """
        Load de pickle model.
        """
        try:
            with open(self.model_path, 'rb') as file:
                model = pickle.load(file)
                self.model = model
                logging.info("El archivo es un pickle válido.")
                logging.info("Modelo cargado:\n%s", model)
        except pickle.UnpicklingError as e:
            logging.error(
                "%s El archivo no es un pickle válido. Error: %s",
                type(e),
                e)
            raise
        except Exception as e:
            logging.error(
                "%s Ocurrió un error al intentar cargar el archivo %s:",
                type(e),
                e)

        return None

    def make_predictions(self, data_df: pd.DataFrame) -> pd.DataFrame:
        """
        COMPLETAR DOCSTRING
        """

        logging.info("---- columnas en data_df -----:\n%s", data_df.columns)

        columnas_necesarias_pred = [
            'Item_Weight',
            'Item_Visibility',
            'Item_MRP',
            'Outlet_Establishment_Year',
            'Outlet_Size',
            'Outlet_Location_Type',
            'Outlet_Type_Grocery Store',
            'Outlet_Type_Supermarket Type1',
            'Outlet_Type_Supermarket Type2',
            'Outlet_Type_Supermarket Type3'
        ]

        columnas_id = ['Item_Identifier', 'Outlet_Identifier']
        logging.info("columnas_necesarias_pred:\n%s", columnas_necesarias_pred)
        data_necesarias_df = data_df[columnas_necesarias_pred]
        logging.info("data_necesarias_df:\n%s", data_necesarias_df.columns)
        data_id_df = data_df[columnas_id]

        # ---- make_predictions ----

        model_lr = self.model

        predicted_data = model_lr.predict(data_necesarias_df)

        predicted_data_df = pd.DataFrame(
            {'Item_Outlet_Sales_Predicted': predicted_data})

        logging.info("Predicción completa:\n%s", predicted_data_df.head())

        # combinación de dataframes
        indices_alineados = predicted_data_df.index.equals(data_id_df.index)
        if indices_alineados:
            data_with_prediction_df = pd.concat(
                [data_id_df, predicted_data_df], axis=1)
            logging.info(
                "Dataframe con las predicciones:\n%s",
                data_with_prediction_df.head())
        else:
            logging.info("Combinación fallida. No coinciden los indices")

        return data_with_prediction_df

    def write_predictions(self, predicted_data_df: pd.DataFrame) -> None:
        """
        COMPLETAR DOCSTRING
        """
        ruta = self.output_path
        logging.info("self.output_path:\n%s", ruta)
        predicted_data_df.to_csv(self.output_path)

        return None

    def run(self):

        data = self.load_data()
        self.load_model()
        df_preds = self.make_predictions(data)
        self.write_predictions(df_preds)


if __name__ == "__main__":

    # Parser de argumentos
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", "-i", required=True,
                        help="Path input CSV file")
    parser.add_argument("--model", "-m", required=True,
                        help="Path to the trained model")
    parser.add_argument("--output", "-o", required=True,
                        help="Path to the output CSV file")

    # Parsear los argumentos de la línea de comandos
    args = parser.parse_args()

    # Instancia del modelo
    pipeline = MakePredictionPipeline(input_path=args.input,
                                      model_path=args.model,
                                      output_path=args.output)
    pipeline.run()
