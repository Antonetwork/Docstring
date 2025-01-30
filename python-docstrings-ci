import ast
import os
import json

def add_docstrings_to_functions(file_path):
    with open(file_path, 'r') as file:
        code = file.read()
    
    tree = ast.parse(code)
    modifications = []
    
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            docstring = f'"""Function to perform {node.name} operation."""'
            # Utiliser ast.Constant pour éviter le warning
            if not node.body or not isinstance(node.body[0], ast.Expr) or not isinstance(node.body[0].value, ast.Constant):
                node.body.insert(0, ast.Expr(value=ast.Constant(value=docstring)))
                modifications.append({'file': file_path, 'line': node.lineno, 'function': node.name, 'docstring': docstring})
    
    modified_code = ast.unparse(tree)
    
    with open(file_path, 'w') as file:
        file.write(modified_code)

    return modifications

def process_directory(directory):
    all_modifications = []
    for filename in os.listdir(directory):
        if filename.endswith('.py'):
            file_path = os.path.join(directory, filename)
            modifications = add_docstrings_to_functions(file_path)
            all_modifications.extend(modifications)
    return all_modifications

# Dossier à parcourir
directory = '.'

# Générer les modifications
modifications = process_directory(directory)

# Sauvegarder le rapport dans un fichier JSON
report_path = 'docstring_report.json'
with open(report_path, 'w') as report_file:
    json.dump(modifications, report_file, indent=4)
