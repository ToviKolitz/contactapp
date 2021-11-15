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
                    chmod +x ./wait-for-docker-compose.sh
                    ./wait-for-docker-compose.sh 60
                 
                    docker exec flask pytest -v > testResult.txt 
                    chmod +x unit-test.sh
                    ./unit-test.sh

                 '''
            }
        }
        stage('E2E test'){
            steps {
                sh '''

                    chmod +x ./e2e-test.sh
                    ./e2e-test.sh

                 '''
            }
        }
        stage('Tag and Publish'){
            steps{
                sh '''
                    chmod +x tag.sh
                    ./tag.sh
                '''
            }
        }
    }
    post{
        cleanup{
            sh '''
                chmod +x cleanUp.sh
                ./cleanUp.sh
            '''
            emailext (
                subject: "Status of  ${env.JOB_NAME} - Build # ${env.BUILD_NUMBER} ",
                body: """ Tests input in the atteched file.\nFor more information, check console output at <a href="${env.BUILD_URL}">${env.JOB_NAME}</a>""",
                to: "tovikolitz@gmail.com", 
                from: "sk0533461282@gmail.com",
                attachLog: true, attachmentsPattern: 'testResult.txt'
            )
        }
    }
}