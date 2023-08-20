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
        stage('Start and configure the network test environment') {
            agent {
                docker { image 'python:3.9.17' }
            }
            steps {
                script {
                    sh 'python3.9 topology/provisioning.py'
                }
            }
        }
        stage('Run playbook') {
            agent {
                docker { image 'webdevops/ansible' }
            }
            steps {
                script {
                    sh 'ansible-playbook network-management.yml'
                }
            }
        }
        stage('Run tests reachability') {
            agent {
                docker { image 'webdevops/ansible' }
            }
            steps {
                script {
                    sh 'ansible-playbook roles/ansible_network_routing/tests/test.yml'
                }
            }
        }
        stage('Destroy the network test environmnent') {
            agent {
                docker { image 'python:3.9.17' }
            }
            steps {
                script {
                sh 'python3.9 topology/delete.py'
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