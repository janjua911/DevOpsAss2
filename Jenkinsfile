// ── Hassan Janjua's Task Board ──────────────────────────────
// Jenkinsfile  →  Part II: Containerized CI/CD Pipeline
// Course: DevOps for Cloud Computing | COMSATS University
// Plugins required: Git, Pipeline, Docker Pipeline
// ─────────────────────────────────────────────────────────────

pipeline {

    agent any

    environment {
        DOCKERHUB_USER  = "hassanjanjua"
        IMAGE_NAME      = "taskboard"
        IMAGE_TAG       = "latest"
        COMPOSE_FILE    = "docker-compose-jenkins.yml"
        CONTAINER_WEB   = "hassan_jenkins_web"
        CONTAINER_DB    = "hassan_jenkins_db"
    }

    stages {

        stage('📥 Clone Repository') {
            steps {
                echo "Cloning Hassan Janjua's Task Board from GitHub..."
                git branch: 'main',
                    url: 'https://github.com/YOUR_GITHUB_USERNAME/hassan-taskboard.git'
            }
        }

        stage('🔍 Verify Workspace') {
            steps {
                echo "Listing cloned files..."
                sh 'ls -la'
                sh 'cat requirements.txt'
            }
        }

        stage('🐳 Build Docker Image') {
            steps {
                echo "Building Docker image: ${DOCKERHUB_USER}/${IMAGE_NAME}:${IMAGE_TAG}"
                sh """
                    docker build -t ${DOCKERHUB_USER}/${IMAGE_NAME}:${IMAGE_TAG} .
                """
            }
        }

        stage('📤 Push to Docker Hub') {
            steps {
                echo "Pushing image to Docker Hub..."
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

        stage('🛑 Tear Down Old Containers') {
            steps {
                echo "Stopping and removing old containers if running..."
                sh """
                    docker compose -f ${COMPOSE_FILE} down --remove-orphans || true
                """
            }
        }

        stage('🚀 Deploy with Docker Compose') {
            steps {
                echo "Launching containerized app via docker-compose-jenkins.yml..."
                sh """
                    docker compose -f ${COMPOSE_FILE} up -d --build
                """
            }
        }

        stage('✅ Verify Deployment') {
            steps {
                echo "Waiting for containers to start..."
                sh 'sleep 15'
                sh 'docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"'
                echo "App should be accessible at http://<EC2-PUBLIC-IP>:5001"
            }
        }
    }

    post {
        success {
            echo """
            ✅ BUILD SUCCESS
            ─────────────────────────────────────────
            Hassan Janjua's Task Board deployed!
            URL: http://<EC2-PUBLIC-IP>:5001
            ─────────────────────────────────────────
            """
        }
        failure {
            echo """
            ❌ BUILD FAILED
            ─────────────────────────────────────────
            Check the console output above for errors.
            ─────────────────────────────────────────
            """
            sh 'docker compose -f ${COMPOSE_FILE} logs || true'
        }
        always {
            echo "Pipeline completed. Cleaning up dangling images..."
            sh 'docker image prune -f || true'
        }
    }
}
