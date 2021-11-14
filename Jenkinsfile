pipeline{
    agent any
    stages{
        stage ("pull"){
            steps {
                echo "-------pull from git---------"
                checkout scm
                git pull
            }
        }
        stage('Build'){
            steps{
                sh ' docker-compose up --build -d'
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
    }
}