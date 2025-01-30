pipeline {
    agent { label 'windowsSlave' }

    environment {
        PYTHON_ENV = 'venv'
        DOCSTRING_REPORT = 'C:\\Jenkins\\workspace\\workspace\\Docstrings\\docstring_report.json'  // Chemin du rapport
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
                    writeFile file: 'add_docstrings.py', text: '''<code Python ci-dessus>'''
                    bat '%PYTHON_ENV%\\Scripts\\python add_docstrings.py'
                }
            }
        }

        stage('Archive Docstring Report') {
            steps {
                script {
                    if (fileExists(DOCSTRING_REPORT)) {
                        archiveArtifacts allowEmptyArchive: true, artifacts: DOCSTRING_REPORT
                    } else {
                        error "Le fichier docstring_report.json n'a pas été trouvé."
                    }
                }
            }
        }

        stage('Move Report to Slave Directory') {
            steps {
                script {
                    // Vérifier que le fichier existe avant de tenter de le déplacer
                    if (fileExists(DOCSTRING_REPORT)) {
                        bat "copy %DOCSTRING_REPORT% C:\\Jenkins\\workspace\\workspace\\TESTPython CICD\\docstring_report.json"
                    } else {
                        error "Le fichier docstring_report.json n'a pas été trouvé pour le déplacer."
                    }
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
