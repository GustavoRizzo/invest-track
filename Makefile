#!make
include .env

# Set the project variables
BACKEND_SERVICE ?= django-application
REPO_BRANCH ?= develop
DJANGO_PROJECT_DIR ?= core
DB_DIR = ./

PYTHON_VERSION ?= $(shell cat ./.python-version)
SYSTEM_VERSION ?= $(shell cat ./.version)

DOCKER=PYTHON_VERSION=${PYTHON_VERSION} docker
DOCKER_COMPOSE=PYTHON_VERSION=${PYTHON_VERSION} DJANGO_PROJECT_DIR=${DJANGO_PROJECT_DIR} COMPOSE_PROJECT_NAME=${COMPOSE_PROJECT_NAME} docker compose -f docker-compose.yml
DOCKER_COMPOSE_DEV=${DOCKER_COMPOSE} -f docker-compose-dev.yml

SERVICES ?= ${BACKEND_SERVICE} nginx
SERVICES_DEV ?= ${BACKEND_SERVICE}-dev

all: help

checkout:  ## Checkout a new source version. Using: REPO_BRANCH
	@echo "Checkout to new version"
	@git fetch; git stash; git checkout ${REPO_BRANCH}; git pull; git stash pop; cd ../

build: deploy  ## Build services images. Using: BUILD_SERVICES
	@echo "Building docker image for version ${SYSTEM_VERSION}..."
	@echo "Systems: Python [${PYTHON_VERSION}]"
	@echo "${DOCKER_COMPOSE} build ${BUILD_SERVICES}"
	@${DOCKER_COMPOSE} build ${BUILD_SERVICES}

build-dev: deploy-dev ## Build development services images. Using: BUILD_SERVICES
	@echo "Building development docker images."
	@${DOCKER_COMPOSE_DEV} build ${BUILD_SERVICES}


rebuild-dev:  ## Force a rebuild of development services images. Using: BUILD_SERVICES
	@echo "Building development docker images"
	@${DOCKER_COMPOSE_DEV} build ${BUILD_SERVICES} --no-cache

up:  ## Start containers. Using: SERVICES
	@echo "Starting containers..."
	@${DOCKER_COMPOSE} up -d --force-recreate ${SERVICES}

up-dev:  ## Start development containers. Using: SERVICES_DEV
	@echo "Starting development containers"
	@${DOCKER_COMPOSE_DEV} up -d --force-recreate ${SERVICES_DEV}

restart-dev:  ## Restart services (or one service specified). Using: SERVICES_DEV
	@${DOCKER_COMPOSE_DEV} restart ${SERVICES_DEV}

stop-dev:  ## Restart service service. Using: SERVICES_DEV
	@${DOCKER_COMPOSE_DEV} stop ${SERVICES_DEV}

test:  ## Run tests
	@echo ${DOCKER_COMPOSE_DEV} run --rm ${BACKEND_SERVICE} python manage.py test --settings=kernel.settings_test
	@${DOCKER_COMPOSE_DEV} run --rm ${BACKEND_SERVICE} python manage.py test --settings=kernel.settings_test

reset-local-db:
	@echo "Reset database..."
	@${DOCKER_COMPOSE} run --rm ${BACKEND_SERVICE} python manage.py reset_db

reset-db: reset-local-db migrate seed create-superuser  ## Reset and restore initial DB
	@echo "Resetting and restoring initial database..."

create-superuser: ## Create a superuser
	@${DOCKER_COMPOSE} run --rm ${BACKEND_SERVICE} python manage.py createsuperuser

static-dir:  ## Create the static directory
	@echo "Create statics files..."
	@${DOCKER_COMPOSE} run --rm ${BACKEND_SERVICE} python manage.py collectstatic --noinput

setup: migrate create-superuser static-dir  ## Setup the database container and data
	@echo "Running project setup"

migrate: ## Run migrations
	@${DOCKER_COMPOSE} run --rm ${BACKEND_SERVICE} python manage.py migrate

create: build setup up  ## Create an environment
	@echo "Create docker environment"

restart: build migrate up  ## Restart docker environment
	@echo "Restarting docker environment"

stop:  ## Stop environment
	@echo "Shutting down..."
	@${DOCKER_COMPOSE} down
	@echo "Done."

deploy-dev: version  ## Deploy/update service DEV container/service
	@echo "Deploy/update service site"
	@${DOCKER_COMPOSE_DEV} build --no-cache ${SERVICES_DEV}
	@${DOCKER_COMPOSE_DEV} up -d --force-recreate ${SERVICES_DEV}

deploy: version  ## Deploy/update service container/service
	@echo "Deploy/update service site"
	@${DOCKER_COMPOSE} build --no-cache ${SERVICES}
	@${DOCKER_COMPOSE} up -d --force-recreate ${SERVICES}

version:  ## Get version
	@$(eval SYSTEM_VERSION = $(shell git describe --tag --dirty=-local-changes --always))
	@$(eval PYTHON_VERSION = $(shell cat ./.python-version))
	@echo "${SYSTEM_VERSION}" > ./.version
	@sed -i -e "s|^SYSTEM_VERSION=.*|SYSTEM_VERSION=${SYSTEM_VERSION}|" ./.env
	@sed -i -e "s|^PYTHON_VERSION=.*|PYTHON_VERSION=${PYTHON_VERSION}|" ./.env
	@echo "Systems Versions: System ${SYSTEM_VERSION} Python ${PYTHON_VERSION}"

help:  ## Show this help
	@echo "\nAvailable commands:"
	@echo
	@sed -n -E -e 's|^([a-zA-Z|\d\_-]+):.+## (.+)|\1@\2|p' $(MAKEFILE_LIST) | column -s '@' -t
	@echo
