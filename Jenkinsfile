pipeline{
    agent any
    stages{
        stage ("pull"){
            steps {
                echo "-------pull from git---------"
                checkout scm
            }
        }
        stage('Build'){
            steps{
                sh ' docker-compose up --build -d'
            }
    }
}