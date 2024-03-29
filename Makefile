up:
	docker-compose \
	  -f docker-compose-python.yml \
		-f docker-compose-mysql.yml \
		-f docker-compose-redis.yml \
		up

upd:
	docker-compose \
	  -f docker-compose-python.yml \
		-f docker-compose-mysql.yml \
		-f docker-compose-redis.yml \
		up -d

upRelease:
	docker-compose \
	  -f docker-compose-release.yml \
		-f docker-compose-redis.yml \
		up

updRelease:
	docker-compose \
	  -f docker-compose-release.yml \
		-f docker-compose-redis.yml \
		up -d

down:
	docker-compose \
	  -f docker-compose-python.yml \
		-f docker-compose-mysql.yml \
		-f docker-compose-redis.yml \
		down

downRelease:
	docker-compose \
	  -f docker-compose-release.yml \
		-f docker-compose-redis.yml \
		down
