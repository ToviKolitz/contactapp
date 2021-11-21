pipeline{
    agent any
    stages{
        stage ("pull"){
            steps {
                echo "-------pull from git-------"
            }
        }
        stage('Build'){
            steps{
                sh ' docker-compose -p project up --build -d'
            }
        }
        stage('Unit test'){
            steps {
                sh '''
                    chmod +x ./scripts/wait-for-docker-compose.sh
                    ./scripts/wait-for-docker-compose.sh 60
                 
                    docker exec flask pytest -v > testResult.txt 
                    chmod +x ./scripts/unit-test.sh
                    ./scripts/unit-test.sh

                 '''
            }
        }
        stage('E2E test'){
            steps {
                sh '''

                    chmod +x ./scripts/e2e-test.sh
                    ./scripts/e2e-test.sh

                 '''
            }
        }
        stage('Tag and Publish'){
            steps{
                sh '''
                    chmod +x ./scripts/tagandpublish.sh
                    ./scripts/tagandpublish.sh
                '''
            }
        }
    }
    post{
        cleanup{
            sh '''
                docker-compose down -v
            '''
            emailext (
                subject: "Status of  ${env.JOB_NAME} - Build # ${env.BUILD_NUMBER} ",
                body: """ Tests input in the atteched file.\nFor more information, check console output at <a href="${env.BUILD_URL}">${env.JOB_NAME}</a>""",
                to: "sk0533146128@gmail.com", 
                from: "tovikolitz@gmail.com",
                attachLog: true, attachmentsPattern: 'testResult.txt'
            )
        }
    }
}