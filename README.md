# Text_Analyzer

## Install
```commandline
python.exe -m pip install --upgrade pip
pip install poetry
poetry install
```
## Download model
```commandline
python src/download_model.py
```

## Run
```commandline
uvicorn src.api:app --port 8000
```

go to /docs