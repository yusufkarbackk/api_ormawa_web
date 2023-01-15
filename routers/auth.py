from fastapi import APIRouter
from database import get_my_sql_connection
from pydantic import BaseModel
from werkzeug.security import check_password_hash, generate_password_hash

router = APIRouter()


class AdminIn(BaseModel):
    username: str
    password: str


class AdminRegister(BaseModel):
    username: str
    password: str
    ormawa: str


class AdminOut(BaseModel):
    id: int
    username: str
    role: str
    ormawa: int


@router.post('/ormaweb/api/v1/auth/login', response_model=AdminOut)
async def login(admin: AdminIn):
    db = get_my_sql_connection()
    result = {}
    username = admin.username
    password = admin.password

    try:
        cur = db.cursor()
        sqlstr = f"select * from user where username='{username}'"
        cur.execute(sqlstr)
        account = cur.fetchone()
        if account:
            if password == account[2]:
                result['id'] = account[0]
                result['username'] = account[1]
                result['role'] = account[3]
                result['ormawa'] = account[4]

                return result
    except Exception as e:
        print("Error in SQL:\n", e)
        return {
            'status':'failed',
            'message':'no admin found'
        }




@router.post('/ormaweb/api/v1/auth/register')
async def resgiter(admin: AdminRegister):
    db = get_my_sql_connection()

    username = admin.username
    password = admin.password
    ormawa = admin.ormawa

    try:
        cur = db.cursor()
        sqlstr = f"insert into user (username, password, ormawa) values ('{username}', '{password}', '{ormawa}')"
        cur.execute(sqlstr)
        db.commit()
        return {
            'message': 'sukses'
        }
    except Exception as e:
        print("Error in SQL:\n", e)
        return {
            'status': 'failed',
            'message': e
        }
