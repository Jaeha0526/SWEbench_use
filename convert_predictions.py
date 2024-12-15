import json
from pathlib import Path
from typing import List, Dict, Any
import sys
import argparse

def read_jsonl_predictions(input_file: str) -> List[Dict[str, Any]]:
    """
    Reads a JSONL file and extracts specified fields from each line.
    
    This function processes each line of the JSONL file individually, making it memory
    efficient even for very large files. It extracts only the essential fields we need:
    instance_id, model_patch, and model_name_or_path.
    
    Parameters:
    -----------
    input_file : str
        Path to the input JSONL file containing model predictions
    
    Returns:
    --------
    List[Dict[str, Any]]
        A list of dictionaries, where each dictionary contains the extracted fields
        from a single prediction
    """
    predictions = []
    required_fields = {'instance_id', 'model_patch', 'model_name_or_path'}
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                try:
                    # Parse each line as a JSON object
                    entry = json.loads(line)
                    
                    # Verify all required fields are present
                    missing_fields = required_fields - set(entry.keys())
                    if missing_fields:
                        print(f"Warning: Line {line_num} is missing fields: {missing_fields}")
                        continue
                    
                    # Extract only the fields we want
                    prediction = {
                        'instance_id': entry['instance_id'],
                        'model_patch': entry['model_patch'],
                        'model_name_or_path': entry['model_name_or_path']
                    }
                    
                    predictions.append(prediction)
                    
                except json.JSONDecodeError:
                    print(f"Warning: Failed to parse JSON at line {line_num}")
                    continue
                
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found")
        sys.exit(1)
    
    return predictions

def write_predictions_json(predictions: List[Dict[str, Any]], output_file: str) -> None:
    """
    Writes the predictions to a single JSON file in a structured array format.
    
    This function takes the processed predictions and writes them to a JSON file
    as an array of prediction objects. It creates any necessary parent directories
    and handles potential writing errors.
    
    Parameters:
    -----------
    predictions : List[Dict[str, Any]]
        List of prediction dictionaries to write to the file
    output_file : str
        Path where the output JSON file should be saved
    """
    try:
        # Create parent directories if they don't exist
        Path(output_file).parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(predictions, f, indent=2, ensure_ascii=False)
        print(f"Successfully processed {len(predictions)} predictions")
        print(f"Output written to: {output_file}")
        
    except IOError as e:
        print(f"Error writing to output file: {str(e)}")
        sys.exit(1)


def parse_arguments():
    """
    Parses and validates command line arguments using named parameters.
    
    Returns:
    --------
    argparse.Namespace
        The parsed command-line arguments
    """
    parser = argparse.ArgumentParser(
        description='Convert JSONL predictions to a single JSON file with selected fields.',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # Changed to use named arguments with -- prefix
    parser.add_argument(
        '--input_file',
        required=True,
        help='Path to the input JSONL file containing predictions'
    )
    
    parser.add_argument(
        '--output_file',
        required=True,
        help='Path where the output JSON file should be saved'
    )
    
    return parser.parse_args()


def main():
    """
    Main function that orchestrates the conversion process.
    """
    # Parse command line arguments
    args = parse_arguments()
    
    print(f"Starting conversion from {args.input_file} to {args.output_file}")
    
    # Process the JSONL file
    predictions = read_jsonl_predictions(args.input_file)
    
    # Write the results
    write_predictions_json(predictions, args.output_file)
    
    print("Conversion completed successfully")

if __name__ == "__main__":
    main()