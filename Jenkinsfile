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
                    // Créer un environnement virtuel et installer les dépendances
                    bat 'python -m venv %PYTHON_ENV%'
                    bat '%PYTHON_ENV%\\Scripts\\pip install -r requirements.txt'
                }
            }
        }

        stage('Add Docstrings') {
            steps {
                script {
                    // Créer le script add_docstrings.py qui ajoute des docstrings
                    writeFile file: 'add_docstrings.py', text: '''<code Python ci-dessus>'''

                    // Exécuter le script pour ajouter les docstrings
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
