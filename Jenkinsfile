pipeline {
    agent any

    environment {
        // Securely pulls the Groq API key from Jenkins Vault
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
                echo 'Checking Python syntax...'
                sh 'python3 -m compileall .'
            }
        }
        
        stage('3. Build Docker Image') {
            steps {
                echo 'Building updated Docker image...'
                sh 'docker build -t real-estate-ai-backend:latest .'
            }
        }
        
        stage('4. Local Cleanup') {
            steps {
                echo 'Removing old dangling images...'
                sh 'docker image prune -f'
            }
        }
        
        stage('5. Deploy Locally') {
            steps {
                echo 'Deploying container with active AI brain...'
                // Force remove any conflicting container safely
                sh 'docker rm -f real_estate_ai_backend || true'
                sh 'docker-compose down'
                sh 'docker-compose up -d --build'
            }
        }
    }
}