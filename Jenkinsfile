pipeline {
    agent any

    environment {
        APP_NAME       = 'real-estate-ai-backend'
        // This securely grabs the secret from Jenkins and maps it to a variable
        OPENAI_API_KEY = credentials('openai-api-key') 
    }

    stages {
        stage('1. Code Checkout') {
            steps {
                checkout scm
            }
        }

        stage('2. Code Analysis & Test') {
            steps {
                sh 'python3 -m compileall .'
            }
        }

        stage('3. Build Docker Image') {
            steps {
                sh "docker build -t ${APP_NAME}:${BUILD_NUMBER} ."
                sh "docker tag ${APP_NAME}:${BUILD_NUMBER} ${APP_NAME}:latest"
            }
        }

        stage('4. Local Cleanup') {
            steps {
                sh 'docker image prune -f'
            }
        }

        stage('5. Deploy Locally') {
            steps {
                echo "Deploying container with active AI brain..."
                // Docker Compose automatically inherits variables from the environment
                sh """
                    docker-compose down || true
                    docker-compose up -d --build
                """
            }
        }
    }
}