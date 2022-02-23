from typing import Optional
from fastapi import FastAPI, File, UploadFile, status, Request
from pydantic import BaseModel

import sqlite3
from sqlite3 import Error

import uuid
import shutil
import aiofiles
import os

app = FastAPI()

LIMIT_IMAGE_SIZE = 15000000

###__INPUT FORM__###
class GetItem(BaseModel):
    id: str

class UpdateItem(BaseModel):
    id: str
    name: str

###__DATABASE__###
## Connecto to database
def create_connection(db_file):
    conn = None 
    try:
        conn = sqlite3.connect(db_file) 
        return conn
    except Error as e:
        print(e) 
    return conn 

## insert information to database
def insert_data(conn, information):
    sql_script = '''INSERT INTO image(uuid, path, image_name) VALUES(?,?,?)'''
    cur = conn.cursor()
    cur.execute(sql_script, information)
    conn.commit()
    return cur.lastrowid

## Get information from database
def get_data(conn, id):
    sql_script = "SELECT * FROM image WHERE uuid=?"
    cur = conn.cursor()
    cur.execute(sql_script, (id, ))
    rows = cur.fetchall()
    return rows

## Update information for database
def update_data(conn, id, name):
    sql_script = "UPDATE image SET path=?, image_name=? WHERE uuid=?"
    cur = conn.cursor()
    path = 'images/' + name 
    cur.execute(sql_script, (path, name, id))
    conn.commit()

## Delete information from database
def delete_data(conn, id):
    sql_script = "DELETE FROM image WHERE uuid=?"
    cur = conn.cursor()
    cur.execute(sql_script, (id,))
    conn.commit()

conn = create_connection('image_database.db') 

###__API__###
## API add image to database
@app.post("/CREATE")
async def upload_image(image: UploadFile = File(...)):
    # print(image.filename)
    # print(image.content_type)
    # print(image.file.read())
    try:
         ## Check Uploaded file format
        if image.content_type not in ["image/jpeg", "image/png", "image/jpg"]:
            print(image.filename)
            return {
                "status": status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                "message": "Unsupported Media Type"
            }

        ## Check size of uploaded file.
        content = image.file.read()
        if len(content) > LIMIT_IMAGE_SIZE:
            return {
                "status": status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                "message": "Size of uploaded image is too large"
            }

        ##Storage Image.
        save_path = f"images/{image.filename}"
        image_name = image.filename
        id = str(uuid.uuid4()).replace('-', '')
        while len(get_data(conn, id)) != 0:
            id = str(uuid.uuid4()).replace('-', '')

        with open(save_path, "wb") as f:
            f.write(content)
            f.close()
        information = (id, save_path, image_name)
        insert_data(conn, information)
    except:
        return {
            "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": "Internal Server Error"
        }

    return {
        "status": status.HTTP_200_OK,
        "message": "OK"
    }

## API get info of image from database
@app.post("/READ")
async def read_information(item: GetItem):
    try:
        id = item.id
        rows = get_data(conn, id)
        if len(rows) == 0:
            result = {
                "id": None,
                "image_path": None,
                "image_name": None
            }
        else:
            image_id = rows[0][0]
            path = rows[0][1]
            image_name = rows[0][2]
            result = {
                "image_id": image_id,
                "image_path": path,
                "image_name": image_name
            }
    except:
        return {
            "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": "Internal Server Error"
        }

    return {
        "status": status.HTTP_200_OK,
        "message": "OK",
        "result": result
    } 

## API Update info of image
@app.post("/UPDATE")
async def update_image(item: UpdateItem):
    try:
        id = item.id
        new_name = item.name
        if new_name.split('.')[-1] not in ['jpg', 'png', 'jpeg', 'JPG', 'PNG', 'JPEG']:
            return {
                "status": status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                "message": "Unsupported Media Type"
            }
        else:
            rows = get_data(conn, id)
            old_path = rows[0][1]
            new_path = 'images/' + new_name
            update_data(conn, id, new_name)
            os.rename(old_path, new_path)
            
    except:
        return {
            "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": "Internal Server Error"
        }
    
    return {
        "status": status.HTTP_200_OK,
        "message": "OK"
    }

## API delete image
@app.post("/DELETE")
async def delete_image(item: GetItem):

    try:
        id = item.id
        rows = get_data(conn, id)
        if len(rows)==0:
            return {
                "status": status.HTTP_200_OK,
                "message": "No items match with the given ID"
            }
        else:
            image_path = rows[0][1]
            delete_data(conn, id)
            os.remove(image_path)
    except:
        return {
            "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": "Internal Server Error"
        }
    
    return {
        "status": status.HTTP_200_OK,
        "message": "OK"
    }
