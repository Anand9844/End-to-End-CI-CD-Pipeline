pipeline {
    agent any
    options { timestamps(); disableConcurrentBuilds() }
    environment {
        IMAGE_NAME = 'end-to-end-cicd-demo'
        CONTAINER_NAME = 'end-to-end-cicd-demo'
        APP_PORT = '5000'
    }
    stages {
        stage('Checkout') { steps { checkout scm } }
        stage('Install Dependencies') {
            steps {
                script {
                    if (isUnix()) {
                        sh 'python3 -m venv .venv'
                        sh '.venv/bin/pip install -r requirements.txt -r requirements-dev.txt'
                    } else {
                        bat 'py -m venv .venv'
                        bat '.venv\\Scripts\\python.exe -m pip install -r requirements.txt -r requirements-dev.txt'
                    }
                }
            }
        }
        stage('Test') {
            steps {
                script {
                    if (isUnix()) { sh '.venv/bin/python -m pytest -v' }
                    else { bat '.venv\\Scripts\\python.exe -m pytest -v' }
                }
            }
        }
        stage('Build Docker Image') {
            steps {
                script {
                    if (isUnix()) {
                        sh 'docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} .'
                        sh 'docker tag ${IMAGE_NAME}:${BUILD_NUMBER} ${IMAGE_NAME}:latest'
                    } else {
                        bat 'docker build -t %IMAGE_NAME%:%BUILD_NUMBER% .'
                        bat 'docker tag %IMAGE_NAME%:%BUILD_NUMBER% %IMAGE_NAME%:latest'
                    }
                }
            }
        }
        stage('Local Demo Deploy') {
            steps {
                script {
                    if (isUnix()) {
                        sh 'docker rm -f ${CONTAINER_NAME} || true'
                        sh 'docker run -d --name ${CONTAINER_NAME} -p ${APP_PORT}:5000 ${IMAGE_NAME}:${BUILD_NUMBER}'
                    } else {
                        bat 'docker rm -f %CONTAINER_NAME%'
                        bat 'docker run -d --name %CONTAINER_NAME% -p %APP_PORT%:5000 %IMAGE_NAME%:%BUILD_NUMBER%'
                    }
                }
            }
        }
        stage('Verify Deployment') {
            steps {
                script {
                    if (isUnix()) {
                        sh 'python3 -c "import time, urllib.request; time.sleep(3); print(urllib.request.urlopen(\"http://127.0.0.1:${APP_PORT}/health\", timeout=10).read().decode())"'
                    } else {
                        bat 'powershell -NoProfile -Command "Start-Sleep -Seconds 3; $r=Invoke-WebRequest -UseBasicParsing http://127.0.0.1:%APP_PORT%/health -TimeoutSec 10; if ($r.StatusCode -ne 200) { exit 1 }; Write-Output $r.Content"'
                    }
                }
            }
        }
    }
    post {
        success { echo 'Pipeline succeeded. Demo app should be available at http://localhost:5000' }
        failure { echo 'Pipeline failed. Review the first failed stage and its console output.' }
    }
}
