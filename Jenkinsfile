pipeline {
    agent any
    stages {
        stage('Clone') {
            steps {
                git 'https://github.com/1234620/DeepFake-Detection.git'
            }
        }
        stage('Build Docker Image') {
            steps {
                sh 'docker build -t deepfake-detection:latest .'
            }
        }
        stage('Run Container') {
            steps {
                sh 'docker stop deepfake-app || true'
                sh 'docker rm deepfake-app || true'
                sh 'docker run -d -p 5000:5000 --name deepfake-app deepfake-detection:latest'
            }
        }
    }
}
