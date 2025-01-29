from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTRect, LTFigure
import PyPDF2

class PDFAnalyzer:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.content_map = {}
        
    def _is_likely_table(self, rect):
        width = rect.bbox[2] - rect.bbox[0]
        height = rect.bbox[3] - rect.bbox[1]
        
        min_width = 200
        min_height = 100
        
        aspect_ratio = width / height if height > 0 else 0
        valid_aspect_ratio = 0.2 < aspect_ratio < 5
        
        return width > min_width and height > min_height and valid_aspect_ratio
    
    def _rectangles_overlap(self, rect1, rect2):
        x1, y1, x2, y2 = rect1.bbox
        x3, y3, x4, y4 = rect2.bbox
        
        overlap_x = max(0, min(x2, x4) - max(x1, x3))
        overlap_y = max(0, min(y2, y4) - max(y1, y3))
        overlap_area = overlap_x * overlap_y
        
        area1 = (x2 - x1) * (y2 - y1)
        area2 = (x4 - x3) * (y4 - y3)
        
        return overlap_area > 0.5 * min(area1, area2)
    
    def analyze_structure(self):
        for page_layout in extract_pages(self.pdf_path):
            page_num = page_layout.pageid
            self.content_map[page_num] = {
                'text_blocks': [],
                'tables': [],
                'figures': []
            }
            
            potential_tables = []
            for element in page_layout:
                if isinstance(element, LTTextContainer):
                    self.content_map[page_num]['text_blocks'].append({
                        'bbox': element.bbox,
                        'text': element.get_text().strip()
                    })
                elif isinstance(element, LTRect) and self._is_likely_table(element):
                    potential_tables.append(element)
                elif isinstance(element, LTFigure):
                    self.content_map[page_num]['figures'].append({
                        'bbox': element.bbox
                    })
            
            final_tables = []
            for rect in potential_tables:
                if not any(self._rectangles_overlap(rect, existing) for existing in final_tables):
                    final_tables.append(rect)
            
            for table in final_tables:
                self.content_map[page_num]['tables'].append({
                    'bbox': table.bbox
                })
        
        return self.content_map 