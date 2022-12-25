from fastapi import APIRouter
from database import get_my_sql_connection
from pydantic import BaseModel
from flask import jsonify
from typing import Optional

router = APIRouter()


class Kegiatan(BaseModel):
    nama_kegiatan: str
    jadwal_kegiatan: str
    deskripsi: str
    id_ormawa: int


@router.get('/ormaweb/api/v1/kegiatan/{id_ormawa}')
def show_kegiatan(id_ormawa:int):
    db = get_my_sql_connection()
    result = {}
    result['results'] = []
    try:
        sqlstr = f"SELECT * from kegiatan where id_ormawa={id_ormawa}"
        cur = db.cursor()
        cur.execute(sqlstr)
        output_json = cur.fetchall()
        # print(output_json)
    except Exception as e:
        print("Error in SQL:\n", e)
    finally:
        db.close()
    for i in output_json:
        result['results'].append({
            'id_kegiata': i[0],
            'nama_kegiatan': i[1],
            'jadwal_kegiatan': i[2],
            'deskripsi': i[3],
            'id_ormawa': i[4],
        })
    return result

@router.post('/ormaweb/api/v1/kegiatan/')
async def tambah_ormawa(kegiatan: Kegiatan):
    db = get_my_sql_connection()
    try:
        cur = db.cursor()
        sqlstr = f"INSERT INTO kegiatan (nama_kegiatan, jadwal_kegiatan, deskripsi, id_ormawa) VALUES('{kegiatan.nama_kegiatan}','{kegiatan.jadwal_kegiatan}', '{kegiatan.deskripsi}', {kegiatan.id_ormawa})"
        cur.execute(sqlstr)
        db.commit()
        cur.close()
        # output_json = cur.fetchall()
    except Exception as e:
        print("Error in SQL:\n", e)
    finally:
        db.close()
    # print(genre)
    return {
        "message": "sukses"
    }
