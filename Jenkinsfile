pipeline {
    agent { label 'windowsSlave' }

    environment {
        PYTHON_ENV = 'venv'
        DOCSTRING_REPORT = 'C:\\Jenkins\\workspace\\workspace\\Docstrings\\docstring_report.json'  // Chemin du rapport
        SLAVE_REPORT_DIR = 'C:\\Jenkins\\workspace\\workspace\\TESTPython CICD' // Répertoire sur le slave où sauvegarder le rapport
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
                    // Créer un code Python valide pour ajouter des docstrings
                    def code = '''
import ast
import os

def add_docstrings(file_path):
    with open(file_path, 'r') as file:
        tree = ast.parse(file.read())
    
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            if not ast.get_docstring(node):
                docstring = f'\"\"\"Function {node.name} description.\"\"\"'
                node.body.insert(0, ast.Expr(value=ast.Str(s=docstring)))
    
    with open(file_path, 'w') as file:
        file.write(ast.unparse(tree))

if __name__ == "__main__":
    directory = '.'
    for filename in os.listdir(directory):
        if filename.endswith('.py'):
            file_path = os.path.join(directory, filename)
            add_docstrings(file_path)
                    '''

                    // Créer le fichier add_docstrings.py avec ce code
                    writeFile file: 'add_docstrings.py', text: code

                    // Exécuter le script Python
                    bat '%PYTHON_ENV%\\Scripts\\python add_docstrings.py'
                }
            }
        }

        stage('Generate and Archive Docstring Report') {
            steps {
                script {
                    // Vérifier que le fichier du rapport existe
                    if (fileExists(DOCSTRING_REPORT)) {
                        // Archiver le fichier docstring_report.json dans Jenkins
                        archiveArtifacts allowEmptyArchive: true, artifacts: DOCSTRING_REPORT

                        // Copier le rapport vers le répertoire du slave
                        bat "copy %DOCSTRING_REPORT% %SLAVE_REPORT_DIR%\\docstring_report.json"
                    } else {
                        // Si le rapport n'existe pas, afficher une erreur
                        error "Le fichier docstring_report.json n'a pas été trouvé."
                    }
                }
            }
        }
    }

    post {
        always {
            echo "Le rapport des docstrings est disponible dans Jenkins et sur le slave."
        }
    }
}
