# Colab Notebook Conversion (scaffold)

This repository contains a scaffold to convert and run a Google Colab notebook inside this workspace.

What I added:
- `notebooks/COLAB_LINK.txt` — contains the original Colab/Drive link you provided.
- `requirements.txt` — basic dependencies to download/convert notebooks.
- `run_step.py` — helper to run a converted script (if present) via `runpy`.
- `scripts/` — directory for converted scripts.

Next steps (pick one):
1. Make the Drive file public (Anyone with the link can view) and I will retry downloading and converting it.
2. Upload the `.ipynb` file into `notebooks/` (drag into the repo) and I'll convert and refactor it.

Commands to retry (once the notebook is accessible):
```bash
pip install gdown nbconvert jupyter
gdown --id 1qO7GrqZTPzxDlfBRiijJvQT6tzEFm3GZ -O notebooks/colab_notebook.ipynb
jupyter nbconvert --to script --output-dir=scripts notebooks/colab_notebook.ipynb
python run_step.py --script scripts/colab_notebook.py
```

If you want me to proceed now, make the file public or upload it here and tell me to continue.
# LLM