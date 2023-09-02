import xml.etree.ElementTree as ET
from pathlib import Path
import sys

# Check if the correct number of arguments is provided
if len(sys.argv) != 2:
    print("Usage: python check_coverage.py <threshold_percentage>")
    sys.exit(1)

# Get the threshold value from the command-line argument (in percentage format)
try:
    threshold_percentage = float(sys.argv[1])
except ValueError:
    print("Threshold must be a valid float value in percentage format")
    sys.exit(1)

# Convert the percentage to a fraction (e.g., 90% to 0.9)
threshold = threshold_percentage / 100.0

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
    print(f'Files with coverage below the threshold ({threshold_percentage}):')
    for filename, line_rate in failed_files:
        print(f'- {filename}: {line_rate * 100:.2f}% coverage')
    sys.exit(1)
