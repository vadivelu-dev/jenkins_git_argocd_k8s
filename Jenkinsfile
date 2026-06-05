pipeline {

    agent any

    environment {
        IMAGE_NAME = "vadivelu123/parking_app"
        IMAGE_TAG = ""
        GIT_REPO = "https://github.com/vadivelu-dev/Project_Git_to_K8s.git"
    }

    stages {

        stage('Clone Application Code') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    env.IMAGE_TAG = sh(script: "date +%Y%m%d%H%M%S", returnStdout: true).trim()
                }

                sh "docker build -t ${IMAGE_NAME}:${env.IMAGE_TAG} ."
            }
        }

        stage('Push to DockerHub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'USER',
                    passwordVariable: 'PASS'
                )]) {

                    sh """
                    echo $PASS | docker login -u $USER --password-stdin
                    docker push ${IMAGE_NAME}:${env.IMAGE_TAG}
                    """
                }
            }
        }

        stage('Update GitOps Repo (Argo CD Sync Trigger)') {
            steps {

                git url: "${GIT_REPO}", branch: "main"

                sh """
                # Set YOUR git identity (from your config)
                git config user.name "Vadivelu M"
                git config user.email "vadivelumsolo@gmail.com"

                # Update deployment image tag
                sed -i 's|image: .*|image: ${IMAGE_NAME}:${env.IMAGE_TAG}|g' deployment.yaml

                git add deployment.yaml
                git commit -m "Update image to ${IMAGE_NAME}:${env.IMAGE_TAG}"
                git push origin main
                """
            }
        }
    }
}
