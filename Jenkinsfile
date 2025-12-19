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

    stage('Build and Publish Images') {
      parallel {
        stage('Frontend') {
          steps {
            script {
              withCredentials([usernamePassword(credentialsId: 'dockerlogin', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                sh '''
                  echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                  docker build -t ${DOCKER_USER}/rfm_frontend:${BUILD_NUMBER} ./frontend
                  docker tag ${DOCKER_USER}/rfm_frontend:${BUILD_NUMBER} ${DOCKER_USER}/rfm_frontend:latest
                  docker push ${DOCKER_USER}/rfm_frontend:${BUILD_NUMBER}
                  docker push ${DOCKER_USER}/rfm_frontend:latest
                '''
              }
            }
          }
        }

        stage('Backend') {
          steps {
            script {
              withCredentials([usernamePassword(credentialsId: 'dockerlogin', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                sh '''
                  echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                  docker build -t ${DOCKER_USER}/rfm_backend:${BUILD_NUMBER} ./backend
                  docker tag ${DOCKER_USER}/rfm_backend:${BUILD_NUMBER} ${DOCKER_USER}/rfm_backend:latest
                  docker push ${DOCKER_USER}/rfm_backend:${BUILD_NUMBER}
                  docker push ${DOCKER_USER}/rfm_backend:latest
                '''
              }
            }
          }
        }
      }
    }

    stage('Deploy') {
      steps {
        script {
          // Using ${WORKSPACE} ensures this works regardless of the Jenkins install path
          def ansibleDir = "${WORKSPACE}/ansible_deploy"
          sh "mkdir -p ${ansibleDir}"
          
          sh """
            # Copy configuration files
            cp docker-compose.yaml ${ansibleDir}/
            cp -r db ${ansibleDir}/
            
            # Check for required secrets/configs
            if [ ! -f ${ansibleDir}/db/password.txt ]; then
              echo 'ERROR: Database password secret is missing!'
              exit 1
            fi
            
            if [ ! -f backend/.env ]; then
              echo 'ERROR: Backend .env file is missing!'
              exit 1
            fi
            
            # Run Ansible deployment using the environment variable from credentials
            ansible-playbook -i ${ANSIBLE_INVENTORY} ${ansibleDir}/deploy.yml
          """
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
