pipeline {

    agent any

    environment {
        DOCKER_IMAGE = 'singathurai/devsecops-app'
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

        stage('Test Application') {
            steps {
                sh '''
                    docker rm -f devsecops-test 2>/dev/null || true

                    docker run -d \
                      --name devsecops-test \
                      -p 5001:5000 \
                      ${DOCKER_IMAGE}:${BUILD_NUMBER}

                    sleep 5

                    echo "Testing application health..."

                    curl -f http://localhost:5001/health

                    echo "Application test successful!"

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
                    usernamePassword(
                        credentialsId: 'github-credentials',
                        usernameVariable: 'GITHUB_USERNAME',
                        passwordVariable: 'GITHUB_TOKEN'
                    )
                ]) {
                    sh '''
                        git config user.name "Jenkins"
                        git config user.email "jenkins@localhost"

                        echo "Fetching latest main branch..."

                        git fetch origin main

                        git reset --hard origin/main

                        echo "Updating Kubernetes image..."

                        sed -i "s#image: singathurai/devsecops-app:.*#image: singathurai/devsecops-app:${BUILD_NUMBER}#" k8s/deployment.yaml

                        echo "Current Kubernetes image:"
                        grep "image:" k8s/deployment.yaml

                        if git diff --quiet k8s/deployment.yaml; then
                            echo "No Kubernetes manifest changes"
                        else
                            git add k8s/deployment.yaml

                            git commit -m "Update image to ${BUILD_NUMBER} [skip ci]"

                            git push \
                              https://${GITHUB_USERNAME}:${GITHUB_TOKEN}@github.com/singathurai007/devsecops-gitops.git \
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
            echo '=========================================='
            echo 'DevSecOps Pipeline completed successfully!'
            echo '=========================================='
        }

        failure {
            echo '=========================================='
            echo 'DevSecOps Pipeline failed!'
            echo '=========================================='
        }
    }
}
