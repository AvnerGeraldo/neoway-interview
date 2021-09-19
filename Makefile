PROJECT = neoway
APP_ENV ?= production
DOCKER_COMPOSE_PATH = .docker/docker-compose.yml
API_CONTAINER = "api_${PROJECT}_container"

ifeq ("${APP_ENV}", "dev")
	DOCKER_COMPOSE_PATH = .docker/docker-compose.dev.yml -p ${PROJECT}
endif

run:
	docker-compose -f ${DOCKER_COMPOSE_PATH} --compatibility up -d

build:
	docker-compose -f ${DOCKER_COMPOSE_PATH} --compatibility up -d --build

docker-restart: docker-stop docker-start

docker-start:
	@docker start $$(docker ps -a -f "name=${PROJECT}" | grep ${PROJECT} | awk '{print $$1}')

docker-stop:
	@docker stop $$(docker ps -f "name=${PROJECT}" | grep ${PROJECT} | awk '{print $$1}')

create-db: db-init migrate

db:
	@docker exec -i ${API_CONTAINER} pipenv run flask db $(cmd)

db-init:
	@$(MAKE) db cmd=init
	@$(MAKE) db cmd=upgrade

migrate:
	@$(MAKE) db cmd=migrate
	@$(MAKE) db cmd=upgrade