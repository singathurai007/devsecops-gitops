pipeline {
    agent any

    environment {
        IMAGE_NAME = 'singathurai/devsecops-app'
        IMAGE_TAG  = "${BUILD_NUMBER}"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build --no-cache \
                      -t ${IMAGE_NAME}:${IMAGE_TAG} \
                      -t ${IMAGE_NAME}:latest \
                      ./app
                '''
            }
        }

        stage('Trivy Security Scan') {
            steps {
                sh '''
                    trivy image \
                      --severity HIGH,CRITICAL \
                      --ignore-unfixed \
                      --exit-code 1 \
                      ${IMAGE_NAME}:${IMAGE_TAG}
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
                                  -Dsonar.host.url=http://15.252.19.115:9000 \
                                  -Dsonar.token=\$SONAR_TOKEN
                            """
                        }
                    }
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
                      ${IMAGE_NAME}:${IMAGE_TAG}

                    sleep 5

                    curl -f http://localhost:5001/health

                    docker rm -f devsecops-test
                '''
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

                        docker push ${IMAGE_NAME}:${IMAGE_TAG}
                        docker push ${IMAGE_NAME}:latest

                        docker logout
                    '''
                }
            }
        }
stage('Update Kubernetes Manifest') {
    steps {
        withCredentials([
            usernamePassword(
                credentialsId: 'github-credentials',
                usernameVariable: 'GITHUB_USERNAME',
                passwordVariable: 'GITHUB_TOKEN'
            )
        ]) {
            sh '''
                git config user.email "cmsingathurai@gmail.com"
                git config user.name "singathurai007"

                sed -i "s#image: singathurai/devsecops-app:.*#image: singathurai/devsecops-app:${BUILD_NUMBER}#" k8s/deployment.yaml

                echo "Updated Kubernetes image:"
                grep "image:" k8s/deployment.yaml

                git add k8s/deployment.yaml

                git commit -m "Update image to ${BUILD_NUMBER}" || true

                git push https://${GITHUB_USERNAME}:${GITHUB_TOKEN}@github.com/singathurai007/devsecops-gitops.git HEAD:main
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

