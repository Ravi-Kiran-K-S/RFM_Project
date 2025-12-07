pipeline {
  agent any
  stages {
    stage('DockerBuildPublish frontend') {
      steps {
        script {
          docker.withRegistry('https://index.docker.io/v1/', 'dockerlogin') {
            def dockerImage = docker.build("graves869/rfm_frontend:latest", "./frontend")
            dockerImage.push()
          }
        }
      }
    }
    stage('DockerBuildPublish backend') {
      steps {
        script {
          docker.withRegistry('https://index.docker.io/v1/', 'dockerlogin') {
            def dockerImage = docker.build("graves869/rfm_backend:latest", "./backend")
            dockerImage.push()
          }
        }
      }
    }
    stage('Deploy') {
      steps {
        sh '''cp docker-compose.yaml /var/jenkins_home/jenkins_workspace/ansible/.
        ansible-playbook -i /var/jenkins_home/jenkins_workspace/ansible/hosts.ini /var/jenkins_home/jenkins_workspace/ansible/deploy.yml
        '''
      }
    }
  }
}
