import ast
import os

def add_docstrings(file_path):
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

def add_docstrings_to_files(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.py'):
            file_path = os.path.join(directory, filename)
            add_docstrings(file_path)

if __name__ == "__main__":
    add_docstrings_to_files('.')
