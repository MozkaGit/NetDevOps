pipeline {
    // environment {
    // }
    agent none
    stages {
        stage('Lint Playbook files in test env') {
            agent {
                docker { image 'pipelinecomponents/ansible-lint' }
            }
            steps {
                script {
                    sh 'ansible-lint network-management.yml'
                }
            }
        }
        stage('Start and configure the test network environment') {
            agent {
                docker { image 'python:3.9.17' }
            }
            steps {
                script {
                    sh '''
                    pip3 install requests
                    python3.9 topology/provisioning.py
                    '''
                }
            }
        }
        stage('Run playbook in test env') {
            agent {
                docker { image 'cytopia/ansible:latest-tools' }
            }
            steps {
                script {
                    sh 'ansible-playbook network-management.yml'
                }
            }
        }
        stage('Run tests reachability in test env') {
            agent {
                docker { image 'cytopia/ansible:latest-tools' }
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
                    sh '''
                    pip3 install requests
                    python3.9 topology/destroy.py
                    '''
                }
            }
        }
        stage('Merge to master') {
            agent {
                docker { image 'bitnami/git' }
            }
            steps {
                script {
                    sh '''
                    git checkout main
                    git merge dev
                    '''
                }
            }
        }
        stage('Lint Playbook files for prod env') {
            agent {
                docker { image 'pipelinecomponents/ansible-lint' }
            }
            steps {
                script {
                    sh 'ansible-lint network-management.yml'
                }
            }
        }
        stage('Start the production network environment') {
            agent {
                docker { image 'python:3.9.17' }
            }
            steps {
                script {
                    sh '''
                    curl -s -b /tmp/cookie -c /tmp/cookie -X POST -d '{"username":"admin","password":"eve"}' http://10.154.0.12/api/auth/login
                    curl -s -c /tmp/cookie -b /tmp/cookie -X GET -H 'Content-type: application/json' http://10.154.0.12/api/labs/Prod%20-%20Network%20Automation%20Routing.unl/nodes/1/start
                    curl -s -c /tmp/cookie -b /tmp/cookie -X GET -H 'Content-type: application/json' http://10.154.0.12/api/labs/Prod%20-%20Network%20Automation%20Routing.unl/nodes/2/start
                    '''
                }
            }
        }
        stage('Run playbook in prod env') {
            agent {
                docker { image 'cytopia/ansible:latest-tools' }
            }
            steps {
                script {
                    sh 'ansible-playbook network-management.yml'
                }
            }
        }
        stage('Run tests reachability in prod env') {
            agent {
                docker { image 'cytopia/ansible:latest-tools' }
            }
            steps {
                script {
                    sh 'ansible-playbook roles/ansible_network_routing/tests/test.yml'
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