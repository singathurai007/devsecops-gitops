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
                sh 'docker build -t devsecops-app:jenkins ./app'
            }
        }
        stage('Trivy Security Scan') {
    steps {
        sh 'trivy image --severity HIGH,CRITICAL --exit-code 1 devsecops-app:jenkins'
    }
}

        stage('Test Application') {
            steps {
                sh 'docker run -d --name devsecops-test -p 5001:5000 devsecops-app:jenkins'
                sh 'sleep 5'
                sh 'curl -f http://localhost:5001/health'
            }
        }
    }

    post {
        always {
            sh 'docker rm -f devsecops-test || true'
        }
    }
}
