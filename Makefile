run:
	uvicorn src.main:app --reload --host 0.0.0.0

require:
	poetry export --without-hashes --with dev --output requirements.txt
