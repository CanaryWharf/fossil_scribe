dev:
	npm exec --prefix frontend concurrently 'yarn --cwd frontend/ dev --port 8080' 'python backend/app.py'

frontend-dist:
	yarn --cwd frontend/ build
