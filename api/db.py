from fastapi import HTTPException
import mysql.connector

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "uiccafesystem",
    "port": 3306,
}


def get_db():
    try:   
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()
        return db, cursor
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
