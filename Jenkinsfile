pipeline {
    agent any // Tells Jenkins to run this on any available server space

    environment {
        // Variables we can reuse in our steps
        IMAGE_NAME = "ai-study-buddy"
        IMAGE_TAG = "${env.BUILD_ID}" // Automatically tags the image with the Jenkins run number (e.g., 1, 2, 3)
    }

    stages {
        stage('Checkout Code') {
            steps {
                echo 'Downloading the latest code from GitHub...'
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building the Docker Image...'
                // This is the exact command you ran locally, but now Jenkins runs it!
                sh 'docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .'
                sh 'docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${IMAGE_NAME}:latest'
            }
        }

        stage('Clean Up Space') {
            steps {
                echo 'Removing dangling images to save server memory...'
                sh 'docker image prune -f'
            }
        }
    }
}