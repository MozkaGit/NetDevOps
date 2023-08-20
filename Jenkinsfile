pipeline {
    // environment {
    // }
    agent none
    stages {
        stage('Lint Playbook files') {
            agent {
                docker { image 'pipelinecomponents/ansible-lint' }
            }
            steps {
                script {
                    sh 'ansible-lint network-management.yml'
                }
            }
        }
    }
    post {
        success {
            slackSend (color: "#028000", message: "Pipeline succeed")
        }
        failure {
            slackSend (color: "#c70039", message: "Pipeline failed")
        }
    }
}