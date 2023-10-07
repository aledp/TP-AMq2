"""
train.py

COMPLETAR DOCSTRING

DESCRIPCIÓN:
AUTOR:
FECHA:
"""

# Imports
import logging
import pandas as pd

class ModelTrainingPipeline(object):

    # Configuración del sistema de logs
    logging.basicConfig(
        filename='./logging_info_ModelTrain.log',
        level=logging.INFO,
        filemode='w',
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S')

    def __init__(self, input_path, model_path):
        self.input_path = input_path
        self.model_path = model_path

    def read_data(self) -> pd.DataFrame:
        """
        COMPLETAR DOCSTRING 
        
        :return pandas_df: The desired DataLake table as a DataFrame
        :rtype: pd.DataFrame
        """
            
        # Cargar los datos de input
        train_data = pd.read_csv(self.input_path)

        # loggin
        logging.info("Carga de datos completa")

        return train_data

    
    def model_training(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        COMPLETAR DOCSTRING
        
        """
        
        # COMPLETAR CON CÓDIGO
        
        return 1 #df_transformed

    def model_dump(self, model_trained) -> None:
        """
        COMPLETAR DOCSTRING
        
        """
        
        # COMPLETAR CON CÓDIGO
        
        return None

    def run(self):
    
        df = self.read_data()
        model_trained = self.model_training(df)
        self.model_dump(model_trained)

if __name__ == "__main__":

    # Parser de argumentos
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", "-i", required=True,
                        help="Path to the first input")
    parser.add_argument("--output", "-o", required=True,
                        help="Path to the output CSV file")

    # Parsear los argumentos de la línea de comandos
    args = parser.parse_args()

    # run ModelTrainingPipeline
    ModelTrainingPipeline(
        input_path=args.input,
        output_path=args.output).run()
