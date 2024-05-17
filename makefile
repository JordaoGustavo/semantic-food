requirements:
	pip3 install -r ./apps/requirements.txt


server: 
	python3 ./apps/manage.py runserver 8080

venv:
	source ./venv/bin/activate