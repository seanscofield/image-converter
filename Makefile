.DEFAULT_GOAL := build

IMAGE_NAME = image_converter
STACK_NAME = image_converter

build:
	docker build -t $(IMAGE_NAME) .

deploy:
	docker stack deploy \
		-c docker-compose.yml \
		$(STACK_NAME)

clean:
	docker stack rm $(STACK_NAME)
