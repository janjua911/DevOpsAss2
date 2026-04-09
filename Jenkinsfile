pipeline {

    agent any

    environment {
        DOCKERHUB_USER  = "hassan911123"
        IMAGE_NAME      = "taskboard"
        IMAGE_TAG       = "latest"
        COMPOSE_FILE    = "docker-compose-jenkins.yml"
    }

    stages {

        stage('📥 Clone Repository') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/janjua911/DevOpsAss2.git'
            }
        }

        stage('🐳 Build Docker Image') {
            steps {
                sh """
                    docker build -t ${DOCKERHUB_USER}/${IMAGE_NAME}:${IMAGE_TAG} .
                """
            }
        }

        stage('📤 Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-credentials',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh """
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                        docker push ${DOCKERHUB_USER}/${IMAGE_NAME}:${IMAGE_TAG}
                        docker logout
                    """
                }
            }
        }

        stage('🛑 Stop Old Containers') {
            steps {
                sh """
                    docker-compose -f ${COMPOSE_FILE} down || true
                """
            }
        }

        stage('🚀 Deploy App') {
            steps {
                sh """
                    docker-compose -f ${COMPOSE_FILE} up -d
                """
            }
        }

        stage('✅ Verify') {
            steps {
                sh 'sleep 10'
                sh 'docker ps'
            }
        }
    }
}
