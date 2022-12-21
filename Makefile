build:
	docker build . -t fastapi-test

run:
	docker run --env-file ./.env fastapi-test

build-and-run:
	make build
	make run
