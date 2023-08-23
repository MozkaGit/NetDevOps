pipeline {
    environment {
        DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1143345873309413447/CP2upEWbggVA4T3vShFrz280xJhAHHkti_UVG0g5FPJ0ZWwD4B57MijN_TAagLbKRh-J"
    }
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
                sshagent(credentials: ['ssh-credentials']) {
                    script {
                        sh '''
                        git checkout main
                        git branch -u origin/main
                        git merge ${BRANCH_NAME}
                        git remote set-url origin git@github.com:MozkaGit/ansible-network-routing.git
                        git push origin main
                        '''
                    }
                }
            }
        }

        stage('Lint Playbook files for prod env') {
            when {
                expression { GIT_BRANCH == 'origin/main' }
            }
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
            environment {
                EVE_NG_HOST = "http://10.154.0.19"
                EVE_NG_CREDS = credentials('eve-ng-creds')
            }
            when {
                expression { GIT_BRANCH == 'origin/main' }
            }
            agent {
                docker { image 'python:3.9.17' }
            }
            steps {
                script {
                    sh '''
                    curl -s -b /tmp/cookie -c /tmp/cookie -X POST -d '{"username":"${EVE-NG_CREDS_USR}","password":"${EVE-NG_CREDS_PSW}"}' ${EVE-NG_HOST}/api/auth/login
                    curl -s -c /tmp/cookie -b /tmp/cookie -X GET -H 'Content-type: application/json' ${EVE-NG_HOST}/api/labs/Prod%20-%20Network%20Automation%20Routing.unl/nodes/1/start
                    curl -s -c /tmp/cookie -b /tmp/cookie -X GET -H 'Content-type: application/json' ${EVE-NG_HOST}/api/labs/Prod%20-%20Network%20Automation%20Routing.unl/nodes/2/start
                    curl -s -c /tmp/cookie -b /tmp/cookie -X GET -H 'Content-type: application/json' ${EVE-NG_HOST}/api/labs/Prod%20-%20Network%20Automation%20Routing.unl/nodes/3/start
                    curl -s -c /tmp/cookie -b /tmp/cookie -X GET -H 'Content-type: application/json' ${EVE-NG_HOST}/api/labs/Prod%20-%20Network%20Automation%20Routing.unl/nodes/4/start
                    '''
                }
            }
        }
        stage('Run playbook in prod env') {
            when {
                expression { GIT_BRANCH == 'origin/main' }
            }
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
            when {
                expression { GIT_BRANCH == 'origin/main' }
            }
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
            discordSend (description: "NetDevOps pipeline succeed", title: "${JOB_NAME}", result: "SUCCESS", webhookURL: "${DISCORD_WEBHOOK_URL}")
            slackSend (color: "#028000", message: "Pipeline succeed")
        }
        failure {
            discordSend (description: "NetDevOps pipeline failed", title: "${JOB_NAME}", result: "FAILURE", webhookURL: "${DISCORD_WEBHOOK_URL}")
            slackSend (color: "#c70039", message: "Pipeline failed")
        }
        aborted {
            discordSend (description: "NetDevOps pipeline aborted", title: "${JOB_NAME}", result: "ABORTED", webhookURL: "${DISCORD_WEBHOOK_URL}")
            slackSend (color: "#8c8e92", message: "Pipeline aborted")
        }
    }
}
