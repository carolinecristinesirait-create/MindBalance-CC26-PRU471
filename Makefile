.PHONY: run test verify compile docker

run:
	streamlit run app.py

test:
	pytest -q

verify:
	python scripts/verify_repository.py

compile:
	python -m compileall -q app.py mindbalance tests scripts

docker:
	docker build -t mindbalance .
