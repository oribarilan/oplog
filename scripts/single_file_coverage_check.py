import xml.etree.ElementTree as ET
from pathlib import Path
import sys

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
    lines = float(class_element.find('lines').get('percent'))
    if lines < 90:  # Individual threshold per file (adjust as needed)
        failed_files.append((filename, lines))

if failed_files:
    print('The following files have coverage below the threshold:')
    for filename, lines in failed_files:
        print(f'- {filename}: {lines}%')
    sys.exit(1)
