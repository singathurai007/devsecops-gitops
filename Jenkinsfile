pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build --no-cache -t devsecops-app:jenkins ./app'
            }
        }

        stage('Trivy Security Scan') {
            steps {
                sh '''
                    trivy image \
                    --severity HIGH,CRITICAL \
                    --ignore-unfixed \
                    --exit-code 1 \
                    devsecops-app:jenkins
                '''
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('sonarqube') {
                    withCredentials([
                        string(
                            credentialsId: 'sonarqube-token',
                            variable: 'SONAR_TOKEN'
                        )
                    ]) {
                        script {
                            def scannerHome = tool 'sonar-scanner'

                            sh """
                                ${scannerHome}/bin/sonar-scanner \
                                  -Dsonar.projectKey=devsecops-app \
                                  -Dsonar.sources=app \
                                  -Dsonar.host.url=\$SONAR_HOST_URL \
                                  -Dsonar.token=\$SONAR_TOKEN
                            """
                        }
                    }
                }
            }
        }

        stage('Quality Gate') {
            steps {
                timeout(time: 5, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }
        stage('Push Docker Image') {
    steps {
        withCredentials([
            usernamePassword(
                credentialsId: 'dockerhub-credentials',
                usernameVariable: 'DOCKER_USERNAME',
                passwordVariable: 'DOCKER_PASSWORD'
            )
        ]) {
            sh '''
                echo "$DOCKER_PASSWORD" | docker login \
                    -u "$DOCKER_USERNAME" \
                    --password-stdin

                docker tag devsecops-app:jenkins \
                    $DOCKER_USERNAME/devsecops-app:latest

                docker push \
                    $DOCKER_USERNAME/devsecops-app:latest

                docker logout
            '''
        }
    }
}

        stage('Test Application') {
            steps {
                sh '''
                    docker rm -f devsecops-test 2>/dev/null || true

                    docker run -d \
                      --name devsecops-test \
                      -p 5001:5000 \
                      devsecops-app:jenkins

                    sleep 5

                    curl -f http://localhost:5001/health

                    docker rm -f devsecops-test
                '''
            }
        }
    }

    post {
        always {
            sh '''
                docker rm -f devsecops-test 2>/dev/null || true
            '''
        }
    }
}
