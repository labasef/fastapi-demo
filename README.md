docker build . -t fastapi-test

docker run --env-file ./.env -p 80:80 fastapi-test
