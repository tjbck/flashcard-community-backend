docker build -t flashcard-community-backend .
docker stop flashcard-community-backend || true
docker rm flashcard-community-backend || true
docker run --env-file ./env -d -p 5055:5055 --add-host=host.docker.internal:host-gateway  --name flashcard-community-backend --restart always flashcard-community-backend
docker image prune -f