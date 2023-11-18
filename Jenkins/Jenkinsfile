pipeline {
    agent {
        docker {
            image 'morphocraft-django:1.1'
            args '--volume /home/student75/github/3103-e-Commerce-Project-1:/home/env -e VIRTUAL_HOST=gracious-poincare.cloud -e VIRTUAL_PORT=80'
        }
    }
    environment {
        JAVA_HOME = "/opt/java/openjdk"
    }

    stages {
        stage('Build') {
            steps {
                sh 'pip install -r requirements.txt'
                sh 'cp /home/env/.env .env'
                sh 'cp /home/env/db.sqlite3 db.sqlite3'
            }
        }

        stage('OWASP Dependency-Check Vulnerabilities') {
            steps {
                dependencyCheck additionalArguments: ''' 
                    --enableExperimental
                    -o './'
                    -s './'
                    -f 'ALL' 
                    --prettyPrint
                    ''', odcInstallation: 'OWASP Dependency-Check Vulnerabilities'
                
                dependencyCheckPublisher pattern: 'dependency-check-report.xml'
            }
        }

        stage('Unit Test') {
            steps {
                sh 'pip install pytest-django==4.5.2'
                sh 'py.test --junitxml reports/results.xml --maxfail=1000 || exit 0'
            }

            post {
                always {
                    junit testResults: 'reports/results.xml', skipPublishingChecks: true
                }
            }
        }

        // Clean up reports before deploying to server
        stage('Report Cleanup') {
            steps {
                sh 'ls -la'
                sh 'rm -r reports'
                sh 'rm .coverage || exit 0'
                sh 'rm pytest.ini'
            }
        }

        stage('Deploy') {
            steps {
                sh 'python3 manage.py runserver 0.0.0.0:80 &'
                input message: 'Finished using the website? (Click "Proceed" to continue)'
                sh 'pkill -f runserver'
            }
        }
    }
}