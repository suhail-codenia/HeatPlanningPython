import argparse
from src.pdf_analyzer import PDFAnalyzer
from src.content_classifier import ContentClassifier
from src.data_extractor import DataExtractor
from src.data_transformer import DataTransformer
import os

def parse_args():
    parser = argparse.ArgumentParser(description="PDF Analysis and Data Extraction Tool")
    parser.add_argument(
        "--input",
        required=True,
        help="Path to input PDF file"
    )
    parser.add_argument(
        "--output",
        help="Base name for output files (without extension). If not provided, uses input filename"
    )
    return parser.parse_args()

def main():
    args = parse_args()
    
    if not os.path.exists(args.input):
        print(f"Error: Input file '{args.input}' does not exist")
        return 1
    
    if args.output:
        output_base = args.output
    else:
        output_base = os.path.splitext(os.path.basename(args.input))[0]
    
    analyzer = PDFAnalyzer(args.input)
    classifier = ContentClassifier()
    
    content_map = analyzer.analyze_structure()
    
    extractor = DataExtractor(content_map)
    tables = extractor.extract_tables()
    text_blocks = extractor.extract_text()
    
    transformer = DataTransformer()
    structured_text = transformer.transform_text_blocks(text_blocks)
    structured_tables = transformer.transform_tables(tables)
    
    # Only output JSON files
    transformer.export_to_json(structured_text, f"{output_base}.json")
    
    for i, table in enumerate(structured_tables):
        transformer.export_to_json(table, f"{output_base}_table_{i}.json")
    
    print(f"Processing complete. JSON files saved with base name: {output_base}")
    return 0

if __name__ == "__main__":
    exit(main()) 