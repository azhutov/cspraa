# Crystal Structure Prediction with Rydberg Atom Arrays

## Setting up the Python Environment

1. Create a python environment on your device using .venv or conda.

```bash
mkdir <PATH>/reGenerativeQuantumChallenge/.venv
python -m venv <PATH>/reGenerativeQuantumChallenge/.venv
```

2. Enter the environment.

```bash
<PATH>/reGenerativeQuantumChallenge/.venv/Scripts/activate
```

3. Install the requirements for the environment.

```bash
pip install -e .
```


## Updating the Setup.py File

If you intend to add dependencies to the repository by installing packages through pip, please consider updating `requirements.txt` and `setup.py` so that the entire team can use a consistent set of packages.

Use https://pypi.org/project/setuppy-generator/

```bash
cd <PATH>/reGenerativeQuantumChallenge/
pip install -e .
pip freeze > requirements.txt
python -m setuppy_generator > setup.py
```
