import xml.etree.ElementTree as ET
import re
import chardet
import argparse
import os.path

# Create an argument parser
parser = argparse.ArgumentParser(description='ADMX Policy Parser')

# Add a command-line argument for the input filename
parser.add_argument('filename', help='Path to the ADMX file')

# Parse the command-line arguments
args = parser.parse_args()

# Validate the input filename
if not os.path.isfile(args.filename):
    print(f"Error: The provided file '{args.filename}' does not exist.")
    exit(1)

# Detect the encoding of the XML file
with open(args.filename, 'rb') as file:
    detector = chardet.universaldetector.UniversalDetector()
    for line in file.readlines():
        detector.feed(line)
        if detector.done:
            break
    encoding = detector.result['encoding']

# Read the XML file
with open(args.filename, 'r', encoding=encoding) as file:
    xml_data = file.read()

# Remove the entire xmlns attribute using regular expressions
modified_xml_data = re.sub(r'\s?xmlns="[^"]+"', '', xml_data)

# Parse the modified XML
root = ET.fromstring(modified_xml_data)

# Initialiser un dictionnaire pour stocker les policies par catégorie
policies_by_category = {}

# Parcourir toutes les catégories
for category in root.iter('category'):
    category_name = category.attrib['name']
    
    # Créer une liste pour chaque catégorie dans le dictionnaire
    if category_name not in policies_by_category:
        policies_by_category[category_name] = []
        
    # Parcourir toutes les policies qui ont cette catégorie comme parentCategory
    for policy in root.iter('policy'):
        parent_category = policy.find('parentCategory')
        
        # Si la policy appartient à la catégorie courante, ajouter son nom à la liste
        if parent_category is not None and parent_category.attrib['ref'] == category_name:
            policies_by_category[category_name].append(policy.attrib['name'])

# Afficher les policies triées par catégorie
for category, policies in policies_by_category.items():
    print(f'Category: {category}')
    for policy in policies:
        print(f' - {policy}')
