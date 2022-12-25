from fastapi import APIRouter
from database import get_my_sql_connection
from pydantic import BaseModel

router = APIRouter()


class User(BaseModel):
    username: str
    password: str
    role: str
    ormawa: str


@router.get('/ormaweb/api/v1/user/')
def show_user():
    db = get_my_sql_connection()
    result = {}
    result['results'] = []
    try:
        sqlstr = f"SELECT * from user"
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
        })
    return result


@router.post('/ormaweb/api/v1/user/')
async def tambah_user(user: User):
    db = get_my_sql_connection()
    try:
        cur = db.cursor()
        sqlstr = f"INSERT INTO user (username, password, role) VALUES('{user.username}','{user.password}', '{user.role}')"
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
