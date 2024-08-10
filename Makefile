dev:
	parallel --lb ::: 'yarn --cwd frontend/ dev --port 8080' 'fastapi dev backend/fossil_scribe/endpoints.py'

frontend-dist:
	yarn --cwd frontend/ build
