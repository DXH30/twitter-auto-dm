install:
	@echo "Building application"
	docker-compose build

logs:
	@echo "Printing logs"
	docker-compose logs

up:
	@echo "Turn on application"
	docker-compose up -d

down:
	@echo "Turn off application"
	docker-compose down

ps:
	@echo "Show process"
	docker-compose ps

build:
	@echo "building $(service) services"
	docker-compose build $(service)

remove:
	@echo "remove images"
	docker-compose rm
