pipeline {
    agent { label 'windowsSlave' }  // Utilisation du slave Windows

    environment {
        PYTHON_ENV = 'venv'  // Nom de l'environnement virtuel Python
        DOCSTRING_REPORT = 'C:\\Jenkins\\workspace\\workspace\\Docstrings\\docstring_report.json'  // Répertoire sur le slave pour le rapport des docstrings
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm  // Récupérer le code depuis GitHub
            }
        }

        stage('Setup Python Environment') {
            steps {
                script {
                    // Créer un environnement virtuel Python
                    bat 'python -m venv %PYTHON_ENV%'
                    // Installer les dépendances si elles sont présentes dans requirements.txt
                    bat '%PYTHON_ENV%\\Scripts\\pip install -r requirements.txt'
                }
            }
        }

        stage('Add Docstrings') {
            steps {
                script {
                    // Créer un fichier Python séparé pour ajouter les docstrings
                    writeFile file: 'add_docstrings.py', text: '''
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
            docstring = f'\"\"\"Function to perform {node.name} operation.\"\"\"'
            if not node.body or not isinstance(node.body[0], ast.Expr) or not isinstance(node.body[0].value, ast.Str):
                node.body.insert(0, ast.Expr(value=ast.Str(s=docstring)))
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

modifications = process_directory('.')

with open('%DOCSTRING_REPORT%', 'w') as report_file:
    json.dump(modifications, report_file, indent=4)
                    '''
                    
                    // Exécuter le fichier Python qui ajoute les docstrings
                    bat '%PYTHON_ENV%\\Scripts\\python add_docstrings.py'
                }
            }
        }

        stage('Archive Docstring Report') {
            steps {
                // Archiver le rapport des docstrings dans Jenkins
                archiveArtifacts allowEmptyArchive: true, artifacts: '%DOCSTRING_REPORT%'
            }
        }

        stage('Move Report to Slave Directory') {
            steps {
                script {
                    // Copier le rapport dans un dossier sur le slave
                    bat 'copy %DOCSTRING_REPORT% C:\\Jenkins\\workspace\\workspace\\TESTPython CICD\\docstring_report.json'
                }
            }
        }
    }

    post {
        always {
            echo "Rapport des docstrings est disponible à la fois dans Jenkins et sur le slave."
        }
    }
}
