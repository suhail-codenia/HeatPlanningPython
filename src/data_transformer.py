import pandas as pd
import json

class DataTransformer:
    def __init__(self):
        self.structured_data = {}
        
    def transform_text_blocks(self, text_blocks):
        df = pd.DataFrame(text_blocks)[['page', 'text']]
        return df
    
    def transform_tables(self, tables):
        return [pd.DataFrame(table) for table in tables]
    
    def export_to_csv(self, data, filename):
        if isinstance(data, pd.DataFrame):
            data.to_csv(filename, index=False)
            
    def export_to_json(self, data, filename):
        if isinstance(data, pd.DataFrame):
            data_dict = data.to_dict(orient='records')
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data_dict, f, indent=4, ensure_ascii=False)
        elif isinstance(data, list):
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False) 