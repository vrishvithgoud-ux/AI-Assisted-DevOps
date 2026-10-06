pipeline {
    agent any

    environment {
        IMAGE_NAME = 'ai-assisted-devops-platform'
        CONTAINER_NAME = "ai-assisted-devops-${BUILD_NUMBER}"
    }

    stages {
        stage('Build Docker Image') {
            steps {
                sh 'docker build --tag "$IMAGE_NAME:$BUILD_NUMBER" .'
            }
        }

        stage('Run Container Validation') {
            steps {
                sh '''
                    set -eu
                    trap 'docker rm --force "$CONTAINER_NAME" >/dev/null 2>&1 || true' EXIT

                    docker run --detach \
                        --name "$CONTAINER_NAME" \
                        --publish 127.0.0.1::5000 \
                        "$IMAGE_NAME:$BUILD_NUMBER"

                    host_port="$(docker port "$CONTAINER_NAME" 5000/tcp | sed 's/.*://')"

                    for attempt in $(seq 1 30); do
                        if response="$(curl --fail --silent \
                            "http://127.0.0.1:${host_port}/health")"; then

                            printf '%s\n' "$response"

                            printf '%s\n' "$response" |
                                grep -Eq '"status"[[:space:]]*:[[:space:]]*"healthy"'

                            exit 0
                        fi

                        if [ "$(docker inspect --format '{{.State.Running}}' "$CONTAINER_NAME")" != 'true' ]; then
                            docker logs "$CONTAINER_NAME"
                            exit 1
                        fi

                        sleep 2
                    done

                    docker logs "$CONTAINER_NAME"
                    echo 'Container health check did not succeed within 60 seconds.'
                    exit 1
                '''
            }
        }
    } 
}

