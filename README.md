# API Image

## Installation requirements
- Create virtual venv
- install all requirement libraries:
```bash
pip install -r requirements.txt
```

## Run API
- Create database:
```bash
python create_database.py
```
- Run API:
```bash
uvicorn api_image:app
```
In this repo have a temp database with 3 images for testing, if you want to create your own database, you can delete file image_database.db and 3 images in the folder images

## API Endpoint
- Add image: http://[your_local_host]/CREATE
- Get image: http://[your_local_host]/READ
- Update image: http://[your_local_host]/UPDATE
- Delete image: http://[your_local_host]/DELETE