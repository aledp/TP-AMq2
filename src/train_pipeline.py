import subprocess

subprocess.run(['python',
                'feature_engineering.py',
                '--input1',
                '..\\data\\Train_BigMart.csv',
                '--input2',
                '..\\data\\Test_BigMart.csv',
                '--output',
                '..\\data\\FE_TrainPipe_processed_data.csv',
                '--logfilename',
                'logging_info_FE_TrainPipe'],
               check=True)

subprocess.run(['python',
                'train.py',
                '--input',
                '..\\data\\FE_TrainPipe_processed_data.csv',
                '--model',
                '..\\data\\modeloDump.pkl'],
               check=True)
