from fastapi import APIRouter
from database import get_my_sql_connection
from pydantic import BaseModel

router = APIRouter()


class Galeri(BaseModel):
    alamat_gambar: str
    deskripsi_gambar: str


class GaleriUpdate(BaseModel):
    alamat_gambar: str
    deskripsi_gambar: str | None = None


@router.get('/ormaweb/api/v1/galeri')
def show_all_galeri():
    db = get_my_sql_connection()
    result = {}
    result['results'] = []
    try:
        sqlstr = f"SELECT * from galeri"
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
                'id_gambar': i[0],
                'id_ormawa': i[1],
                'alamat_gambar': i[2],
                'deskripsi': i[3],
            }
        )
    return result


@router.get('/ormaweb/api/v1/galeri/{id_ormawa}')
def show_galeri(id_ormawa: int):
    db = get_my_sql_connection()
    result = {}
    result['results'] = []
    try:
        sqlstr = f"SELECT * from galeri where id_ormawa={id_ormawa}"
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
                'id_gambar': i[0],
                'id_ormawa': i[1],
                'alamat_gambar': i[2],
                'deskripsi': i[3],
            }
        )
    return result


@router.get('/ormaweb/api/v1/galeri_by_id/{id_gambar}')
def show_galeri_by_id(id_gambar: int):
    db = get_my_sql_connection()
    result = {}

    try:
        sqlstr = f"SELECT * from galeri where id_gambar={id_gambar}"
        cur = db.cursor()
        cur.execute(sqlstr)
        output_json = cur.fetchone()
        # print(output_json)
    except Exception as e:
        print("Error in SQL:\n", e)
    finally:
        db.close()

    result['id_gambar'] = output_json[0]
    result['id_ormawa'] = output_json[1]
    result['alamat_gambar'] = output_json[2]
    result['deskripsi'] = output_json[3]

    return result


@router.post('/ormaweb/api/v1/galeri/{id_ormawa}')
async def tambah_galeri(id_ormawa: int, galeri: Galeri):
    db = get_my_sql_connection()
    try:
        cur = db.cursor()
        sqlstr = f"INSERT INTO galeri (id_ormawa, alamat_gambar, deskripsi_gambar) VALUES({id_ormawa},'{galeri.alamat_gambar}', '{galeri.deskripsi_gambar}')"
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


@router.patch('/ormaweb/api/v1/galeri/{id_gambar}/')
def update_galeri(id_gambar: int, galeri: Galeri):
    db = get_my_sql_connection()

    data_galeri = galeri.dict(exclude_unset=True)
    print(data_galeri)

    for key, value in data_galeri.items():
        print(key)
        print(value)
        if value == None:
            continue
        try:
            sqlstr = f"update galeri set {key} = '{value}' where id_gambar={id_gambar}"
            cur = db.cursor()
            cur.execute(sqlstr)
            db.commit()
            cur.close()
        except Exception as e:
            print("Error in SQL:\n", e)
    db.close()


@router.delete('/ormaweb/api/v1/galeri/{id_gambar}')
def delete_gambar(id_gambar: int):
    db = get_my_sql_connection()
    try:
        sqlstr = f"delete from galeri where id_gambar={id_gambar}"
        cur = db.cursor()
        cur.execute(sqlstr)
        db.commit()
    except Exception as e:
        print("Error in SQL:\n", e)
    finally:
        db.close()
