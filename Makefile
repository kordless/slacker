# makefile

kill: 
	$(eval KILLME = $(shell docker ps -q -f ancestor=slacker))
	-docker kill $(KILLME)

build: kill
	docker build -t slacker .

run: build
	docker run -d slacker

exec: run
	docker exec -ti slacker sh 

logs:
	$(eval LOGGME = $(shell docker ps -q -f ancestor=slacker))
	-docker logs $(LOGGME) 
