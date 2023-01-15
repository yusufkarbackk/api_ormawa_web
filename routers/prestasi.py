from fastapi import APIRouter
from database import get_my_sql_connection
from pydantic import BaseModel
from datetime import time
import datetime


router = APIRouter()


class Prestasi(BaseModel):
    nama_prestasi: str


@router.get('/ormaweb/api/v1/prestasi/{id_ormawa}')
def show_prestasi_by_id_ormawa(id_ormawa: int):
    db = get_my_sql_connection()
    result = {}
    result['results'] = []
    try:
        sqlstr = f"SELECT * from prestasi where id_ormawa={id_ormawa}"
        cur = db.cursor()
        cur.execute(sqlstr)
        output_json = cur.fetchall()
        # print(output_json)
    except Exception as e:
        print("Error in SQL:\n", e)
    finally:
        db.close()
    for i in output_json:

        result['results'].append(
            {
                'id_prestasi': i[0],
                'nama_prestasi': i[1],
                'id_ormawa': i[2],
            }
        )
    return result


@router.post('/ormaweb/api/v1/prestasi/{id_ormawa}')
async def tambah_prestasi(id_ormawa: int, prestasi: Prestasi):
    db = get_my_sql_connection()
    try:
        cur = db.cursor()
        sqlstr = f"INSERT INTO prestasi (nama_prestasi, id_ormawa) VALUES('{prestasi.nama_prestasi}',{id_ormawa})"
        cur.execute(sqlstr)
        db.commit()
        cur.close()
        # output_json = cur.fetchall()
        return {
            "message": "sukses"
        }
    except Exception as e:
        print("Error in SQL:\n", e)
    finally:
        db.close()
    # print(genre)


@router.delete('/ormaweb/api/v1/prestasi/{id_prestasi}')
def delete_prestasi(id_prestasi: int):
    db = get_my_sql_connection()
    try:
        sqlstr = f"delete from prestasi where id_prestasi={id_prestasi}"
        cur = db.cursor()
        cur.execute(sqlstr)
        db.commit()
    except Exception as e:
        print("Error in SQL:\n", e)
    finally:
        db.close()


@router.get('/ormaweb/api/v1/prestasi_by_id/{id_prestasi}')
def show_prestasi_by_id(id_prestasi: int):
    db = get_my_sql_connection()
    #result = {}
    try:
        sqlstr = f"SELECT * from prestasi where id_prestasi={id_prestasi}"
        cur = db.cursor()
        cur.execute(sqlstr)
        output_json = cur.fetchall()
        # print(output_json)
    except Exception as e:
        print("Error in SQL:\n", e)
    finally:
        db.close()
    for i in output_json:

        return {
            'id_prestasi': i[0],
            'nama_prestasi': i[1],
            'id_ormawa': i[2],
        }


@router.patch('/ormaweb/api/v1/prestasi/{id_prestasi}/')
def update_prestasi(id_prestasi: int, kegiatan: Prestasi):
    db = get_my_sql_connection()

    data_prestasi = kegiatan.dict(exclude_unset=True)
    print(data_prestasi)

    for key, value in data_prestasi.items():
        if value == None:
            continue
        try:
            sqlstr = f"update prestasi set nama_prestasi = '{value}' where id_prestasi={id_prestasi}"
            cur = db.cursor()
            cur.execute(sqlstr)
            db.commit()
            cur.close()
        except Exception as e:
            print("Error in SQL:\n", e)
    db.close()
