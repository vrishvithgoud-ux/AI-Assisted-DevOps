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
                        "$IMAGE_NAME:$BUILD_NUMBER"

                    container_ip="$(docker inspect --format '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' "$CONTAINER_NAME")"
                    test -n "$container_ip"

                    for attempt in $(seq 1 30); do
                        if response="$(curl --fail --silent --connect-timeout 2 --max-time 2 \
                            "http://${container_ip}:5000/health")"; then

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
