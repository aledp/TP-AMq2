"""
feature_engineering.py

This module performs various data preprocessing and feature engineering steps on a CSV dataset.

Input data must be in a .csv file.

AUTHOR: [Your Name]
FECHA: [Date]

"""
# Imports
import argparse
from io import StringIO
import logging
import pandas as pd


class FeatureEngineeringPipeline(object):
    """
    Perform imput load, transformation steps to obtain the dataset for training
      or prediction and return the output.

    :return transformed_df: The desired dataset
    :rtype: .csv file
    """

    def __init__(self, input_path_1, output_path, input_path_2=None):

        # Configuración del sistema de logs
        logging.basicConfig(
            filename='./logs/logging_info_FE.log',
            level=logging.INFO,
            filemode='w',
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S')

        # seteo de las rutas de input y output
        self.input_path_1 = input_path_1
        self.input_path_2 = input_path_2
        self.output_path = output_path

    def read_data(self) -> pd.DataFrame:
        """
        Read the input data from the specified path and return it as a DataFrame.

        :return raw_df: The desired DataLake table as a DataFrame
        :rtype: pd.DataFrame
        """

        # Cargar los datos de input_1
        raw_data_df_1 = pd.read_csv(self.input_path_1)
        raw_data_df_1['Set'] = 'train'

        # Verificar si input_2 fue proporcionado
        if args.input2:
            raw_data_df_2 = pd.read_csv(self.input_path_2)
            raw_data_df_2['Set'] = 'test'
            # Concatenar los DataFrames solo si raw_data_2 fue cargado
            # exitosamente
            raw_data_df = pd.concat(
                [raw_data_df_1, raw_data_df_2], ignore_index=True)
        else:
            # Si no se proporcionó input_path_2, raw_data será igual a data1
            raw_data_df = raw_data_df_1
        # ver >>> eso se podria haber hecho con manejo de errores??

        # loggin
        logging.info("Carga de datos completa")

        return raw_data_df

    def data_transformation(
            self,
            raw_data_df: pd.DataFrame) -> pd.DataFrame:
        """
        Perform data transformation steps.
        :return df: return procecced data. Columns: 'Item_Identifier',
        'Item_Weight', 'Item_Fat_Content', 'Item_Visibility','Item_Type',
        'Item_MRP', 'Outlet_Identifier', 'establishment_age','Outlet_Size',
        'Outlet_Location_Type', 'Item_Outlet_Sales', 'Item_MRP_Categories',
        'Outlet_Type_Grocery Store', 'Outlet_Type_Supermarket Type1',
        'Outlet_Type_Supermarket Type2','Outlet_Type_Supermarket Type3'.
        :rtype: pd.DataFrame
        """
        # loggin
        logging.info("Iniciando transformación de datos")

        # -------- Age of establishment --------

        reference_year = 2019

        raw_data_df['Outlet_Establishment_Year'] = (
            reference_year - raw_data_df['Outlet_Establishment_Year'])
        raw_data_df = raw_data_df.rename(columns={'Outlet_Establishment_Year':
                                                  'establishment_age'})

        # loggin
        description = raw_data_df['establishment_age'].describe()
        logging.info("Variable 'establishment_age':\n%s", description)

        # -------- labels unification:'Item_Fat_Content' --------
        raw_data_df['Item_Fat_Content'] = raw_data_df['Item_Fat_Content'].replace(
            {'low fat': 'Low Fat', 'LF': 'Low Fat', 'reg': 'Regular'})

        # loggin
        labels = raw_data_df['Item_Fat_Content'].unique()
        logging.info("Variable 'Item_Fat_Content' labels:\n%s", labels)

        # -------- missing values imputation: 'Item_Weight' --------

        # loggin
        logging.info(
            '% inicial de valores perdidos en "Item_Weight":',
            raw_data_df['Item_Weight'].isnull().sum() /
            len(raw_data_df) *
            100)

        null_rows = raw_data_df[raw_data_df['Item_Weight'].isnull()]
        null_labels = list(null_rows['Item_Identifier'].unique())

        for product in null_labels:
            mode = raw_data_df.loc[raw_data_df['Item_Identifier'] == product,
                                   'Item_Weight'].mode()
            mode = mode.max()
            raw_data_df.loc[raw_data_df['Item_Identifier'] == product,
                            'Item_Weight'] = mode

        logging.info(
            '% final de valores perdidos en "Item_Weight":',
            raw_data_df['Item_Weight'].isnull().sum() /
            len(raw_data_df) *
            100)

        # -------- missing values imputation: 'Outlet_Size' --------

        outlets_size_null = list(
            raw_data_df[raw_data_df['Outlet_Size'].isnull()]['Outlet_Identifier'].unique())

        raw_data_df.loc[raw_data_df['Outlet_Identifier']
                        .isin(outlets_size_null), 'Outlet_Size'] = 'Small'

        # loggin
        unique_pairs = raw_data_df.loc[raw_data_df['Outlet_Identifier'].isin(
            outlets_size_null), ['Outlet_Identifier', 'Outlet_Size']].drop_duplicates()
        logging.info("missing values imputation: 'Outlet_Size':\n%s",
                     unique_pairs)

        # ver / propuesta de mejora: reemplazar simplemente por small segun
        # identificador no es conveniente dado que no automatiza.
        # propongo probar reemplazar por el valor de mayor frecuecuencia
        # correspondiente al tipo de tienda.

        # -------- 'Item_Fat_Content': new category --------

        # Lista de items donde no aplica el fat_content
        item_type_list = ['Household',
                          'Health and Hygiene',
                          'Hard Drinks',
                          'Soft Drinks',
                          'Fruits and Vegetables']

        # Recategorización
        raw_data_df.loc[raw_data_df['Item_Type']
                        .isin(item_type_list), 'Item_Fat_Content'] = 'NA'

        # loggin
        unique_pairs = raw_data_df.loc[raw_data_df['Item_Type'].isin(
            item_type_list), ['Item_Type', 'Item_Fat_Content']].drop_duplicates()
        logging.info("'Item_Fat_Content': new category NA':\n%s", unique_pairs)

        # -------- 'Item_Type': new categories --------

        # Recatogarizando 'Item_Type'
        raw_data_df['Item_Type'] = raw_data_df['Item_Type'].replace(
            {
                'Others': 'Non perishable',
                'Health and Hygiene': 'Non perishable',
                'Household': 'Non perishable',
                'Seafood': 'Meats',
                'Meat': 'Meats',
                'Baking Goods': 'Processed Foods',
                'Frozen Foods': 'Processed Foods',
                'Canned': 'Processed Foods',
                'Snack Foods': 'Processed Foods',
                'Breads': 'Starchy Foods',
                'Breakfast': 'Starchy Foods',
                'Soft Drinks': 'Drinks',
                'Hard Drinks': 'Drinks',
                'Dairy': 'Drinks'})

        # Recategorización segun 'Item_Fat_Content'
        raw_data_df.loc[raw_data_df['Item_Type'] ==
                        'Non perishable', 'Item_Fat_Content'] = 'NA'

        # ver / propuesta de mejora: se propone que este bloque esté antes
        # del bloque de "'Item_Fat_Content': new category" porque sino la
        # ultima linea tiene que ver con eso, es decir que se mezclan conceptos
        # dentro del bloque (no queda bien modularizado).

        # loggin
        logging.info(
            "'Item_Type': new categories list:\n%s",
            raw_data_df['Item_Type'].unique())

        # -------- Encodding: 'Item_MRP' --------
        n_bins = 4

        categories = [i + 1 for i in range(n_bins)]
        percentiles = [i * (100 / n_bins) for i in range(n_bins + 1)]
        boundaries = raw_data_df['Item_MRP'].quantile(
            [p / 100 for p in percentiles])

        raw_data_df['Item_MRP'] = pd.cut(
            raw_data_df['Item_MRP'],
            bins=boundaries,
            labels=categories,
            include_lowest=True
        )

        # loggin
        logging.info("Item_MRP:\n%s",
                     raw_data_df['Item_MRP'].unique())

        logging.info("Categories boundaries:\n%s", boundaries)

        # -------- Encodding: ordinal features --------

        raw_data_df_2 = raw_data_df.drop(
            columns=['Item_Type', 'Item_Fat_Content']).copy()
        # ver: no entiendo para qué crea el dataframe raw_data_df_2.
        # Tampoco por qué esta operación está en este bloque.

        # diccionario de mapeo para 'Outlet_Size'y 'Outlet_Location_Type'
        size_dicc = {'High': 2, 'Medium': 1, 'Small': 0}
        location_dicc = {'Tier 1': 2, 'Tier 2': 1, 'Tier 3': 0}

        # Encodding
        raw_data_df_2['Outlet_Size'] = raw_data_df_2['Outlet_Size'].replace(
            size_dicc)
        raw_data_df_2['Outlet_Location_Type'] = raw_data_df_2['Outlet_Location_Type'].replace(
            location_dicc)

        # loggin
        logging.info("Outlet_Size dicctionary:\n%s", size_dicc)
        logging.info("Labels Outlet_Size encodded:\n%s",
                     raw_data_df_2['Outlet_Size'].unique())
        logging.info("Outlet_Location_Type dicctionary:\n%s", location_dicc)
        logging.info("Labels Outlet_Location_Type encodded:\n%s",
                     raw_data_df_2['Outlet_Location_Type'].unique())

        # -------- Encodding: nominal features --------

        raw_data_df_2 = pd.get_dummies(
            raw_data_df_2,
            columns=['Outlet_Type'],
            dtype='uint8')

        # loggin
        logging.info(
            "columns after 'Outlet_Type' encoding:\n%s",
            raw_data_df_2.columns)

        # -------- End of FeatureEngineering --------

        df_transformed = raw_data_df_2

        # loggin
        buf = StringIO()
        raw_data_df_2.info(buf=buf)
        logging.info("Transformación de datos completa:\n%s",
                     buf.getvalue())

        return df_transformed

    def write_prepared_data(self, transformed_dataframe: pd.DataFrame) -> None:
        """
        Write the output data as .cvs file in the specified path.

        :return df: Output oh the FeatureEngineeringPipeline
        :rtype: .csv
        """

        transformed_dataframe.to_csv(self.output_path, index=False)

        return None

    def run(self):
        """
        Run the script to transfom imput data.

        :return raw_df: None
        :rtype: None
        """
        raw_data_df = self.read_data()
        df_transformed = self.data_transformation(raw_data_df)
        self.write_prepared_data(df_transformed)


if __name__ == "__main__":

    # Parser de argumentos
    parser = argparse.ArgumentParser()
    parser.add_argument("--input1", "-i1", required=True,
                        help="Path to the first input")
    parser.add_argument("--input2", "-i2", default=None,
                        help="Path to the second input")
    parser.add_argument("--output", "-o", required=True,
                        help="Path to the output CSV file")

    # Parsear los argumentos de la línea de comandos
    args = parser.parse_args()

    # run FeatureEngineeringPipeline
    FeatureEngineeringPipeline(
        input_path_1=args.input1,
        output_path=args.output,
        input_path_2=args.input2).run()
