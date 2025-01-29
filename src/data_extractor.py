import pandas as pd
from PyPDF2 import PdfReader
from typing import List, Dict, Any

class DataExtractor:
    def __init__(self, content_map):
        self.content_map = content_map
        
    def extract_tables(self):
        tables = []
        for page_num, content in self.content_map.items():
            for table in content['tables']:
                table_data = self._extract_table_data(table['bbox'], page_num)
                if table_data and len(table_data) > 0:  
                    tables.append(table_data)
        return tables
    
    def extract_text(self):
        text_blocks = []
        for page_num, content in self.content_map.items():
            for block in content['text_blocks']:
                if block['text'].strip():  
                    text_blocks.append({
                        'page': page_num,
                        'text': block['text'].strip()
                    })
        return text_blocks
    
    def _extract_table_data(self, table_bbox: tuple, page_num: int) -> List[Dict[str, Any]]:
        x1, y1, x2, y2 = table_bbox
        table_data = []
        
        for block in self.content_map[page_num]['text_blocks']:
            block_x1, block_y1, block_x2, block_y2 = block['bbox']
            
            if (x1 <= block_x1 and block_x2 <= x2 and 
                y1 <= block_y1 and block_y2 <= y2):
                
                table_data.append({
                    'text': block['text'].strip(),
                    'row': int((block_y1 - y1) / 20),  
                    'col': int((block_x1 - x1) / 100)  
                })
        
        if table_data:
            table_dict = {}
            for cell in table_data:
                row = cell['row']
                col = cell['col']
                if row not in table_dict:
                    table_dict[row] = {}
                table_dict[row][col] = cell['text']
            
            result = []
            if table_dict:
                all_cols = set()
                for row in table_dict.values():
                    all_cols.update(row.keys())
                
                headers = [f'Column_{i}' for i in range(len(all_cols))]
                
                for row in table_dict.values():
                    row_data = {}
                    for col_idx, header in enumerate(headers):
                        row_data[header] = row.get(col_idx, '')
                    result.append(row_data)
                
                return result
        
        return [] 