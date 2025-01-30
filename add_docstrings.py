import ast
import os
import json

def add_docstrings(file_path):
    """Ajoute des docstrings aux fonctions qui n'en ont pas."""
    with open(file_path, 'r') as file:
        tree = ast.parse(file.read())
    
    modified_functions = []
    
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            if not ast.get_docstring(node):
                docstring = f'\"\"\"Function {node.name} description.\"\"\"'
                node.body.insert(0, ast.Expr(value=ast.Constant(value=docstring)))
                modified_functions.append(node.name)
    
    with open(file_path, 'w') as file:
        file.write(ast.unparse(tree))
    
    return modified_functions

def generate_report():
    """Génère un rapport JSON des fichiers modifiés."""
    report = {}
    directory = '.'
    for filename in os.listdir(directory):
        if filename.endswith('.py'):
            file_path = os.path.join(directory, filename)
            modified_functions = add_docstrings(file_path)
            if modified_functions:
                report[filename] = modified_functions
    
    # Enregistrer le rapport dans un fichier JSON
    with open('docstring_report.json', 'w') as report_file:
        json.dump(report, report_file, indent=4)

if __name__ == "__main__":
    generate_report()
