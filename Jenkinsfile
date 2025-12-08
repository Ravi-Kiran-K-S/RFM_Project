pipeline {
  agent any
  
  options {
    // Prevent concurrent builds
    disableConcurrentBuilds()
    // Keep last 10 builds
    buildDiscarder(logRotator(numToKeepStr: '10'))
    // Set timeout to 30 minutes
    timeout(time: 30, unit: 'MINUTES')
  }
  
  environment {
    // Use Jenkins credentials instead of hardcoding
    DOCKER_REGISTRY = credentials('docker-registry-url')
    DOCKER_CREDENTIALS = credentials('dockerlogin')
    ANSIBLE_INVENTORY = credentials('ansible-inventory-path')
  }

  stages {
    stage('Validate') {
      steps {
        script {
          echo "Validating docker-compose.yaml..."
          sh 'docker-compose -f docker-compose.yaml config > /dev/null'
          echo "✓ docker-compose.yaml is valid"
        }
      }
    }

    stage('DockerBuildPublish frontend') {
      steps {
        script {
          withCredentials([usernamePassword(credentialsId: 'dockerlogin', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
            sh '''
              echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
              docker build -t ${DOCKER_USER}/rfm_frontend:${BUILD_NUMBER} ./frontend
              docker tag ${DOCKER_USER}/rfm_frontend:${BUILD_NUMBER} ${DOCKER_USER}/rfm_frontend:latest
              docker push ${DOCKER_USER}/rfm_frontend:${BUILD_NUMBER}
              docker push ${DOCKER_USER}/rfm_frontend:latest
              docker logout
            '''
          }
        }
      }
    }

    stage('DockerBuildPublish backend') {
      steps {
        script {
          withCredentials([usernamePassword(credentialsId: 'dockerlogin', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
            sh '''
              echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
              docker build -t ${DOCKER_USER}/rfm_backend:${BUILD_NUMBER} ./backend
              docker tag ${DOCKER_USER}/rfm_backend:${BUILD_NUMBER} ${DOCKER_USER}/rfm_backend:latest
              docker push ${DOCKER_USER}/rfm_backend:${BUILD_NUMBER}
              docker push ${DOCKER_USER}/rfm_backend:latest
              docker logout
            '''
          }
        }
      }
    }

    stage('Deploy') {
      steps {
        script {
          sh '''
            # Copy configuration files to Ansible workspace
            cp docker-compose.yaml /var/jenkins_home/jenkins_workspace/ansible/.
            cp -r db /var/jenkins_home/jenkins_workspace/ansible/.
            
            # Verify secrets are properly configured before deployment
            if [ ! -f /var/jenkins_home/jenkins_workspace/ansible/db/password.txt ]; then
              echo "ERROR: Database password secret is not configured!"
              exit 1
            fi
            
            # Verify .env files exist
            if [ ! -f backend/.env ]; then
              echo "ERROR: Backend .env file is not configured!"
              exit 1
            fi
            
            # Run Ansible deployment
            ansible-playbook -i ${ANSIBLE_INVENTORY} /var/jenkins_home/jenkins_workspace/ansible/deploy.yml
          '''
        }
      }
    }
  }
  
  post {
    always {
      // Clean up sensitive data
      sh 'docker logout || true'
      cleanWs()
    }
    success {
      echo "✓ Pipeline completed successfully"
    }
    failure {
      echo "✗ Pipeline failed. Check logs for details."
    }
  }
}
