import subprocess

subprocess.run(['python',
                'feature_engineering.py',
                '--input1',
                'D:\\Github_aledp\\ceia_ApMaq2\\TP-AMq2\\data\\Train_BigMart.csv',
                '--input2',
                'D:\\Github_aledp\\ceia_ApMaq2\\TP-AMq2\\data\\Test_BigMart.csv',
                '--output',
                'D:\\Github_aledp\\ceia_ApMaq2\\TP-AMq2\\data\\FE_InferencePipe_processed_data.csv'],
                check=True)

subprocess.run(['python', 
                'predict.py', 
                '-i',
                'D:\\Github_aledp\\ceia_ApMaq2\\TP-AMq2\\data\\FE_InferencePipe_processed_data.csv',
                '-m',
                'D:\\Github_aledp\\ceia_ApMaq2\\TP-AMq2\\data\\modeloDump.pkl',
                '-o',
                'D:\\Github_aledp\\ceia_ApMaq2\\TP-AMq2\\data\\predicted_data.csv'],
                 check=True)