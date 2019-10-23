from __future__ import print_function

from pypandas.text_cleaner import clean_text


class BpSamplePySpark():

    def __init__(self, spark, env):
        self.spark = spark
        self.data_lake = env["s3_data_lake"]
     
        
    def process_data(self, df):
        if df is None or df.count() == 0:
            error = 'No records to process'
            print(error)
            return None

        # Mask all numbers with _number_
        df = clean_text(df, '*')
        return df
