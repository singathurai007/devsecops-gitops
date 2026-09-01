pipeline {

    agent any

    environment {
        DOCKER_IMAGE = 'singathurai/devsecops-app'
        SONARQUBE_SERVER = 'sonarqube'
        SONAR_HOST_URL = 'http://15.252.19.115:9000'
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
                      -t ${DOCKER_IMAGE}:${BUILD_NUMBER} \
                      -t ${DOCKER_IMAGE}:latest \
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
                      ${DOCKER_IMAGE}:${BUILD_NUMBER}
                '''
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv("${SONARQUBE_SERVER}") {
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
                                  -Dsonar.host.url=${SONAR_HOST_URL} \
                                  -Dsonar.token=${SONAR_TOKEN}
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
                      ${DOCKER_IMAGE}:${BUILD_NUMBER}

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

                        docker push ${DOCKER_IMAGE}:${BUILD_NUMBER}

                        docker push ${DOCKER_IMAGE}:latest

                        docker logout
                    '''
                }
            }
        }

        stage('Update Kubernetes Manifest') {
            steps {
                withCredentials([
                    string(
                        credentialsId: 'github-token',
                        variable: 'GITHUB_TOKEN'
                    )
                ]) {
                    sh '''
                        git config user.email "cmsingathurai@gmail.com"
                        git config user.name "singathurai007"

                        sed -i "s#image: ${DOCKER_IMAGE}:.*#image: ${DOCKER_IMAGE}:${BUILD_NUMBER}#" \
                          k8s/deployment.yaml

                        echo "Updated Kubernetes image:"
                        grep "image:" k8s/deployment.yaml

                        git add k8s/deployment.yaml

                        if git diff --cached --quiet; then
                            echo "No Kubernetes manifest changes"
                        else
                            git commit -m "Update image to ${BUILD_NUMBER} [skip ci]"

                            git push \
                              https://${GITHUB_TOKEN}@github.com/singathurai007/devsecops-gitops.git \
                              HEAD:main
                        fi
                    '''
                }
            }
        }
    }

    post {
        always {
            sh '''
                docker rm -f devsecops-test 2>/dev/null || true
            '''
        }

        success {
            echo 'DevSecOps Pipeline completed successfully!'
        }

        failure {
            echo 'DevSecOps Pipeline failed!'
        }
    }
}
