build:
	 docker compose build

run: build
	 docker compose up

daemon: build
	 docker compose up -d
	 @echo http://localhost:$$(docker port judge-host 8964 | awk -F: '{print $$2}')/

stop:
	 docker compose down

run-test:
	 @docker compose -f docker-compose-test.yaml up -d
	 @docker events --filter 'event=die' > .event & echo $$! > .pidfile
	 @while [ -z "$$(cat .event | grep 'flask_app_test')" ]; do \
	 	 	 sleep 1; \
	 done
	 @docker compose -f docker-compose-test.yaml ps -a | grep flask_app_test | egrep -o "Exited \(.*\)" | egrep -o "\(.*\)" | tr -d '()' > .test_result 
	 @docker compose -f docker-compose-test.yaml logs flask_app_test
	 @docker compose -f docker-compose-test.yaml down
	 @test_result=$$(cat .test_result)
	 @kill -9 `cat .pidfile`
	 @rm .pidfile
	 @rm .event
