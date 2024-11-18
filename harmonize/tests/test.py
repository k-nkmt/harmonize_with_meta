import unittest
import pandas as pd
import json

class TestIPUMSData(unittest.TestCase):
    def setUp(self):
        self.ipums_dict = {}
        with open('code/ipums_dict.json', 'r') as f:
            self.ipums_dict = json.load(f)

    def test_csv_files(self):
        csv_files = [
            'ipums_data/2000kokucho_ipums.csv',
            'ipums_data/2005kokucho_ipums.csv',
            'ipums_data/2010kokucho_ipums.csv',
            'ipums_data/2015kokucho_ipums.csv'
            ]
        for csv_file in csv_files:
            with self.subTest(csv_file=csv_file):
                df = pd.read_csv(csv_file, dtype=str)
                for col in df.columns:
                    if col in ["country", "year", "sample", "pref_jp","munic_jp", "persons","serial","pernum"]:
                        continue

                    if col not in self.ipums_dict:
                        self.fail(f"Column '{col}' not found in ipums_dict")
                    else:
                        values = set(df[col].unique())
                        dict_keys = set(self.ipums_dict[col].keys())
                        diff = values - dict_keys
                        if len(diff) > 0:
                            self.fail(f"Column '{col}' contains values not found in ipums_dict: {diff}")

if __name__ == '__main__':
    unittest.main()