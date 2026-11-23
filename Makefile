PYTHON ?= python

.PHONY: setup seed pipeline app test demo eval clean

setup:
	$(PYTHON) -m pip install -r requirements.txt

seed:
	$(PYTHON) scripts/make_seed.py

pipeline:
	$(PYTHON) -m pipeline

app:
	$(PYTHON) -m streamlit run app/streamlit_app.py

test:
	$(PYTHON) -m pytest -q

eval:
	$(PYTHON) -m detect.eval

demo: seed pipeline app

clean:
	$(PYTHON) -c "import pathlib; [f.unlink() for f in pathlib.Path('data/db').glob('*') if f.name != '.gitkeep']"
