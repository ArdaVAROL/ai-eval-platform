PYTHON=python
PIP=$(PYTHON) -m pip

.PHONY: backend-install backend-migrate backend-run backend-seed frontend-install frontend-run

backend-install:
	$(PIP) install -r backend/requirements.txt

backend-migrate:
	cd backend && alembic upgrade head

backend-run:
	uvicorn app.main:app --app-dir backend --reload

backend-seed:
	cd backend && $(PYTHON) -m app.scripts.seed_sample_data

frontend-install:
	cd frontend && npm install

frontend-run:
	cd frontend && npm run dev
