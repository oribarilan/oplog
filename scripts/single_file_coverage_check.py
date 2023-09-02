import xml.etree.ElementTree as ET

tree = ET.parse('coverage.xml')
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
    exit(1)
