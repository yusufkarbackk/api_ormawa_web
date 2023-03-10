from fastapi import APIRouter
from database import get_my_sql_connection
from pydantic import BaseModel
from datetime import time
import datetime


router = APIRouter()


class Kegiatan(BaseModel):
    nama_kegiatan: str
    hari: str
    waktu: time
    deskripsi: str


@router.get('/ormaweb/api/v1/kegiatan/{id_ormawa}')
def show_kegiatan(id_ormawa: int):
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
        waktu = str(i[5])

        result['results'].append(
            {
                'id_kegiatan': i[0],
                'nama_kegiatan': i[1],
                'hari': i[2],
                'deskripsi': i[3],
                'id_ormawa': i[4],
                'waktu': waktu
            }
        )
    return result


@router.post('/ormaweb/api/v1/kegiatan/{id_ormawa}')
async def tambah_kegiatan(id_ormawa: int, kegiatan: Kegiatan):
    db = get_my_sql_connection()
    waktu = kegiatan.waktu.strftime('%H:%M')
    try:
        cur = db.cursor()
        sqlstr = f"INSERT INTO kegiatan (nama_kegiatan, hari, deskripsi, id_ormawa, waktu) VALUES('{kegiatan.nama_kegiatan}','{kegiatan.hari}', '{kegiatan.deskripsi}', {id_ormawa}, '{waktu}')"
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


@router.delete('/ormaweb/api/v1/kegiatan/{id_kegiatan}')
def delete_kegiatan(id_kegiatan: int):
    db = get_my_sql_connection()
    try:
        sqlstr = f"delete from kegiatan where id_kegiatan={id_kegiatan}"
        cur = db.cursor()
        cur.execute(sqlstr)
        db.commit()
    except Exception as e:
        print("Error in SQL:\n", e)
    finally:
        db.close()


@router.get('/ormaweb/api/v1/kegiatan_by_id/{id_kegiatan}')
def show_kegiatan_by_id(id_kegiatan: int):
    db = get_my_sql_connection()
    #result = {}
    try:
        sqlstr = f"SELECT * from kegiatan where id_kegiatan={id_kegiatan}"
        cur = db.cursor()
        cur.execute(sqlstr)
        output_json = cur.fetchall()
        # print(output_json)
    except Exception as e:
        print("Error in SQL:\n", e)
    finally:
        db.close()
    for i in output_json:
        waktu = str(i[5])

        return {
            'id_kegiatan': i[0],
            'nama_kegiatan': i[1],
            'hari': i[2],
            'deskripsi': i[3],
            'id_ormawa': i[4],
            'waktu': waktu
        }


@router.patch('/ormaweb/api/v1/kegiatan/{id_kegiatan}/')
def update_kegiatan(id_kegiatan: int, kegiatan: Kegiatan):
    db = get_my_sql_connection()

    data_ormawa = kegiatan.dict(exclude_unset=True)
    print(data_ormawa)

    for key, value in data_ormawa.items():
        if value == None:
            continue
        try:
            sqlstr = f"update kegiatan set {key} = '{value}' where id_kegiatan={id_kegiatan}"
            cur = db.cursor()
            cur.execute(sqlstr)
            db.commit()
            cur.close()
        except Exception as e:
            print("Error in SQL:\n", e)
    db.close()
