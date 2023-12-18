# Text_Analyzer

## Install in local

### Install environment

```commandline
python.exe -m pip install --upgrade pip
pip install poetry
poetry install
```
### Download model
```commandline
python app/src/download_model.py
```

### Run
```commandline
uvicorn app.src.api:app --port 8000
```

## Install in docker
1. После установки Docker нужно открыть консоль и перейти в расположение проекта, создать образ (image)

```bash
docker build -t your_image_name .
```

2. Далее создаётся контейнер

```bash
docker run -d --name your_container_name -p your_port_number:80 your_image_name
```

## Работа

Для работы с API после запуска контейнера необходимо перейти по одному из адресов в браузере:

- **http://localhost:container_port_number/docs** на локальной машине,

- **http://your_local_IP:container_port_number/docs** на другом компьютере в локальной сети,

- **http://global_IP:container_port_number/docs** при хостинге.