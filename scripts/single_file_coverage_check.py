import xml.etree.ElementTree as ET
from pathlib import Path
import sys

# Define the threshold (X) for line-rate
threshold = 0.90  # Adjust as needed

# Get the directory of the script (where the script is located)
script_dir = Path(__file__).resolve().parent

# Specify the path to the coverage.xml file in the root of the project
coverage_file_path = script_dir.parent / "coverage.xml"

# Check if the coverage.xml file exists
if not coverage_file_path.exists():
    print("Coverage report not found, failing the workflow")
    sys.exit(1)

tree = ET.parse(coverage_file_path)
root = tree.getroot()

failed_files = []

for class_element in root.findall('.//class[@filename]'):
    filename = class_element.get('filename')
    line_rate = float(class_element.get('line-rate'))

    if line_rate < threshold:
        failed_files.append((filename, line_rate))

if failed_files:
    print('The following files have coverage below the threshold:')
    for filename, line_rate in failed_files:
        print(f'- {filename}: {line_rate * 100:.2f}% coverage')  # Convert line_rate to percentage
    sys.exit(1)
