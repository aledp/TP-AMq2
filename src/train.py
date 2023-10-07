"""
train.py

COMPLETAR DOCSTRING

DESCRIPCIÓN:
AUTOR:
FECHA:
"""

# Imports
import argparse
import logging
import pandas as pd
from sklearn.model_selection import train_test_split, cross_validate, cross_val_score
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
        processed_data = pd.read_csv(self.input_path)

        # loggin
        logging.info("Carga de datos completa. Columnas del dataset:\n%s", processed_data.columns)

        return processed_data

    
    def model_training(self, processed_data_df: pd.DataFrame) -> pd.DataFrame:
        """
        COMPLETAR DOCSTRING
        
        """

        #----- division en train y test -----

        # Elimnar columnas que son muy específicas
        df_dataset = processed_data_df.drop(columns=['Item_Identifier', 'Outlet_Identifier'])

        # División del dataset de train y test
        df_train = df_dataset.loc[df_dataset['Set'] == 'train']
        df_test = df_dataset.loc[df_dataset['Set'] == 'test']

        # Eliminando columnas sin datos
        df_train.drop(['Set'], axis=1, inplace=True)
        df_test.drop(['Item_Outlet_Sales','Set'], axis=1, inplace=True)
        
        #----- entrenamiento del modelo -----


        
        # COMPLETAR CON CÓDIGO
        
        return 1 #df_transformed

    def model_dump(self, model_trained) -> None:
        """
        COMPLETAR DOCSTRING
        
        """
        
        # COMPLETAR CON CÓDIGO
        
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
    