import ast
import os

def add_docstrings_to_file(file_path):
    with open(file_path, 'r') as file:
        code = file.read()

    tree = ast.parse(code)
    modified_code = code

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            if ast.get_docstring(node) is None:
                # Ajouter un docstring si aucune n'existe
                docstring = f'"""Docstring for function {node.name}."""\n'
                modified_code = modified_code.replace(
                    f"def {node.name}(", f"def {node.name}({docstring}("
                )

    if modified_code != code:
        with open(file_path, 'w') as file:
            file.write(modified_code)

def add_docstrings_to_directory(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.py'):
            file_path = os.path.join(directory, filename)
            add_docstrings_to_file(file_path)

# Usage : Ajouter des docstrings à tous les fichiers Python dans un répertoire
directory = 'C:/Jenkins/workspace/workspace/Docstrings/local_copy'  # répertoire local
add_docstrings_to_directory(directory)
