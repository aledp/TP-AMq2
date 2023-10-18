import subprocess

subprocess.run(['python',
                'feature_engineering.py',
                '--input1',
                '..\\data\\Train_BigMart.csv',
                '--input2',
                '..\\data\\Test_BigMart.csv',
                '--output',
                '..\\data\\FE_InferencePipe_processed_data.csv',
                '--logfilename',
                'logging_info_FE_InferencePipe'],
               check=True)

subprocess.run(['python',
                'predict.py',
                '-i',
                '..\\data\\FE_InferencePipe_processed_data.csv',
                '-m',
                '..\\data\\modeloDump.pkl',
                '-o',
                '..\\data\\predicted_data.csv'],
               check=True)
