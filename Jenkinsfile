pipeline {
    agent any

    environment {
        APP_NAME = 'real-estate-ai-backend'
    }

    stages {
        stage('1. Code Checkout') {
            steps {
                echo 'Cloning the latest automation code from Git...'
                checkout scm
            }
        }

        stage('2. Code Analysis & Test') {
            steps {
                echo 'Verifying FastAPI application structure...'
                // This ensures your code passes basic structural syntax checks
                sh 'python3 -m compileall .'
            }
        }

        stage('3. Build Docker Image') {
            steps {
                echo "Building production Docker image for version: ${BUILD_NUMBER}..."
                sh "docker build -t ${APP_NAME}:${BUILD_NUMBER} ."
                sh "docker tag ${APP_NAME}:${BUILD_NUMBER} ${APP_NAME}:latest"
            }
        }

        stage('4. Local Cleanup') {
            steps {
                echo 'Cleaning up old dangling images on your machine...'
                sh 'docker image prune -f'
            }
        }

        stage('5. Deploy Locally') {
            steps {
                echo "Deploying container version ${BUILD_NUMBER} to your local machine..."
                // Spins down the old container and boots up the fresh build
                sh """
                    docker-compose down || true
                    docker-compose up -d --build
                """
            }
        }
    }

    post {
        success {
            echo "Deployment successful! The automated lead engine is live locally."
        }
        failure {
            echo "Pipeline failed. Check the stage logs above to troubleshoot the error."
        }
    }
}