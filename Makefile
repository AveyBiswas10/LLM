PY=python3

.PHONY: convert run-all

convert:
	$(PY) tools/convert_notebook.py notebooks/colab_notebook.ipynb

run-all:
	bash run_all.sh
