from fastapi import APIRouter
from database import get_my_sql_connection
from pydantic import BaseModel

router = APIRouter()


class User(BaseModel):
    username: str
    password: str
    id_ormawa: int


class Admin(BaseModel):
    username: str


@router.get('/ormaweb/api/v1/admin/')
def show_admin():
    db = get_my_sql_connection()
    result = {}
    result['results'] = []
    try:
        sqlstr = f"SELECT * from user where role != 'super admin'"
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
            'id': i[0],
            'username': i[1],
            'password': i[2],
            'role': i[3],
            'ormawa': i[4],
        })
    return result


@router.get('/ormaweb/api/v1/admin/{id}/')
def show_admin_by_id(id: int):
    db = get_my_sql_connection()
    result = {}

    try:
        sqlstr = f"SELECT * from user where id = {id}"
        cur = db.cursor()
        cur.execute(sqlstr)
        output_json = cur.fetchall()
        # print(output_json)
    except Exception as e:
        print("Error in SQL:\n", e)
    finally:
        db.close()
    for i in output_json:
        result['id'] = i[0]
        result['username'] = i[1]
        result['role'] = i[3]
        result['id_ormawa'] = i[4]
    return result


@router.post('/ormaweb/api/v1/admin/')
async def tambah_admin(user: User):
    db = get_my_sql_connection()
    try:
        cur = db.cursor()
        sqlstr = f"INSERT INTO user (username, password, id_ormawa) VALUES('{user.username}','{user.password}',{user.id_ormawa})"
        cur.execute(sqlstr)
        db.commit()
        cur.close()
        print('sukses')
        # output_json = cur.fetchall()
    except Exception as e:
        print("Error in SQL:\n", e)
    finally:
        db.close()
    # print(genre)
    return {
        "message": "sukses"
    }


@router.patch('/ormaweb/api/v1/admin/{id}/')
def update_admin(id: int, admin: Admin):
    db = get_my_sql_connection()

    data_ormawa = admin.dict(exclude_unset=True)
    print(data_ormawa)

    try:
        sqlstr = f"update user set username = '{data_ormawa['username']}' where id={id}"
        cur = db.cursor()
        cur.execute(sqlstr)
        db.commit()
        cur.close()
    except Exception as e:
        print("Error in SQL:\n", e)
    db.close()

@router.delete('/ormaweb/api/v1/admin/{id}')
def delete_admin(id: int):
    db = get_my_sql_connection()
    try:
        sqlstr = f"delete from user where id={id}"
        cur = db.cursor()
        cur.execute(sqlstr)
        db.commit()
    except Exception as e:
        print("Error in SQL:\n", e)
    finally:
        db.close()
