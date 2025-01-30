pipeline {
    agent { label 'windowsSlave' }

    environment {
        PYTHON_ENV = 'venv'
        PYTHON_FILES_DIR = '.'  // Répertoire contenant les fichiers Python
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Python Environment') {
            steps {
                script {
                    bat 'python -m venv %PYTHON_ENV%'
                    bat '%PYTHON_ENV%\\Scripts\\pip install -r requirements.txt'
                }
            }
        }

        stage('Add Docstrings') {
            steps {
                script {
                    // Créer le fichier add_docstrings.py avec le code Python
                    def code = '''
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
                    '''

                    // Créer le fichier add_docstrings.py avec ce code
                    writeFile file: 'add_docstrings.py', text: code

                    // Exécuter le script Python
                    bat '%PYTHON_ENV%\\Scripts\\python add_docstrings.py'
                }
            }
        }

        stage('Transfer Python Files to Slave') {
            steps {
                script {
                    // Copier tous les fichiers Python modifiés dans le répertoire du slave
                    bat 'xcopy /E /I /Y *.py "C:\\Jenkins\\workspace\\workspace\\TESTPython CICD\\"'
                }
            }
        }
    }

    post {
        always {
            echo "Les fichiers Python modifiés ont été transférés au slave."
        }
    }
}
