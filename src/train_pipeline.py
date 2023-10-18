import subprocess

#subprocess.run(['Python', 'feature_engineering.py'])

#subprocess.run(['Python', 'train.py'])

subprocess.run(['python',
                'feature_engineering.py',
                '--input1',
                'D:\\Github_aledp\\ceia_ApMaq2\\TP-AMq2\\data\\Train_BigMart.csv',
                '--input2',
                'D:\\Github_aledp\\ceia_ApMaq2\\TP-AMq2\\data\\Test_BigMart.csv',
                '--output',
                'D:\\Github_aledp\\ceia_ApMaq2\\TP-AMq2\\data\\FE_TrainPipe_processed_data.csv'],
               check=True)

subprocess.run(['python',
        'train.py',
        '--input',
        'D:\\Github_aledp\\ceia_ApMaq2\\TP-AMq2\\data\\FE_TrainPipe_processed_data.csv',
        '--model',
        'D:\\Github_aledp\\ceia_ApMaq2\\TP-AMq2\\data\\modeloDump.pkl'],
    check=True)
