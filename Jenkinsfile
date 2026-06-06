pipeline {

    agent any

    environment {
        IMAGE_NAME = "vadivelu123/parking_app"
        GIT_REPO = "https://github.com/vadivelu-dev/jenkins_git_argocd_k8s.git"
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
                    env.IMAGE_TAG = sh(
                        script: "date +%Y%m%d%H%M%S",
                        returnStdout: true
                    ).trim()
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

                withCredentials([usernamePassword(
                    credentialsId: 'github-creds',
                    usernameVariable: 'GIT_USER',
                    passwordVariable: 'GIT_TOKEN'
                )]) {

                    sh """
                    git config user.name "Vadivelu M"
                    git config user.email "vadivelumsolo@gmail.com"

                    # Clone GitOps repo fresh
                    rm -rf gitops-repo
                    git clone https://${GIT_USER}:${GIT_TOKEN}@github.com/vadivelu-dev/jenkins_git_argocd_k8s.git gitops-repo

                    cd gitops-repo

		    echo "BEFORE UPDATE:"
		    cat deployment.yaml

                    # SAFE image update (no greedy regex issues)
                    sed -i 's|image: .*|image: ${IMAGE_NAME}:${env.IMAGE_TAG}|g' deployment.yaml

                    echo "AFTER UPDATE:"
		    cat deployment.yaml

		    git add deployment.yaml
                    git commit -m "Update image to ${IMAGE_NAME}:${env.IMAGE_TAG}"

                    git push origin main
                    """
                }
            }
        }
    }
}
