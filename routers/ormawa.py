from fastapi import APIRouter, status
from database import get_my_sql_connection
from pydantic import BaseModel
from flask import jsonify
from typing import Optional

router = APIRouter()


class Ormawa(BaseModel):
    nama_ormawa: str
    deskripsi: str
    visi: str
    misi: str
    ketua: str
    alamat_gambar: str


class OrmawaUpdate(BaseModel):
    nama_ormawa: str | None = None
    deskripsi: str | None = None
    visi: str | None = None
    misi: str | None = None
    ketua: str | None = None
    alamat_gambar: str | None = None


@router.get('/ormaweb/api/v1/ormawa/')
def show_ormawa():
    db = get_my_sql_connection()
    result = {}
    result['results'] = []
    try:
        sqlstr = f"SELECT * from ormawa"
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
            'id_ormawa': i[0],
            'nama_ormawa': i[1],
            'deskripsi': i[2],
            'visi': i[3],
            'misi': i[4],
            'ketua': i[5],
            'alamat_gambar': i[6]
        })
    return result


@router.get('/ormaweb/api/v1/ormawa/{id_ormawa}')
def show_ormawa(id_ormawa: int):
    db = get_my_sql_connection()
    result = {}
    try:
        sqlstr = f"SELECT * from ormawa where id_ormawa={id_ormawa}"
        cur = db.cursor()
        cur.execute(sqlstr)
        output_json = cur.fetchall()
        # print(output_json)
    except Exception as e:
        print("Error in SQL:\n", e)
    finally:
        db.close()
    # return OrmawaOut(result=output_json[0])
    for i in output_json:
        result['id_ormawa'] = i[0]
        result['nama_ormawa'] = i[1]
        result['deskripsi'] = i[2]
        result['visi'] = i[3]
        result['misi'] = i[4]
        result['ketua'] = i[5]
        result['alamat_gambar'] = i[6]

    return result


@router.post('/ormaweb/api/v1/ormawa/', status_code=status.HTTP_201_CREATED)
async def tambah_ormawa(ormawa: Ormawa):
    db = get_my_sql_connection()
    try:
        cur = db.cursor()
        sqlstr = f"INSERT INTO ormawa (nama_ormawa, deskripsi, visi, misi, ketua, alamat_gambar) VALUES('{ormawa.nama_ormawa}','{ormawa.deskripsi}', '{ormawa.visi}', '{ormawa.misi}', '{ormawa.ketua}', '{ormawa.alamat_gambar}')"
        cur.execute(sqlstr)
        db.commit()
        cur.close()
        print('sukses')
        # output_json = cur.fetchall()
    except Exception as e:
        print("Error in SQL:\n", e)
        return status.HTTP_500_INTERNAL_SERVER_ERROR
    finally:
        db.close()
    # print(genre)
    return {
        "message": "sukses"
    }


@router.patch('/ormaweb/api/v1/ormawa/{id_ormawa}')
def update_ormawa(id_ormawa: int, ormawa: OrmawaUpdate):
    db = get_my_sql_connection()

    data_ormawa = ormawa.dict(exclude_unset=True)
    print(data_ormawa)

    for key, value in data_ormawa.items():
        if value == None:
            continue
        try:
            sqlstr = f"update ormawa set {key} = '{value}' where id_ormawa={id_ormawa}"
            cur = db.cursor()
            cur.execute(sqlstr)
            db.commit()
            cur.close()
        except Exception as e:
            print("Error in SQL:\n", e)
    db.close()


@router.delete('/ormaweb/api/v1/ormawa/{id_ormawa}')
def delete_ormawa(id_ormawa: int):
    db = get_my_sql_connection()
    try:
        sqlstr = f"delete from ormawa where id_ormawa={id_ormawa}"
        cur = db.cursor()
        cur.execute(sqlstr)
        db.commit()
    except Exception as e:
        print("Error in SQL:\n", e)
    finally:
        db.close()
