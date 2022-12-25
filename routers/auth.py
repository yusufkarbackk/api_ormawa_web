from fastapi import APIRouter
from database import get_my_sql_connection
from pydantic import BaseModel
from werkzeug.security import check_password_hash, generate_password_hash

router = APIRouter()


class AdminIn(BaseModel):
    username: str
    password: str


class AdminOut(BaseModel):
    id:int
    username: str
    role: str
    ormawa: str


@router.post('/ormaweb/api/v1/auth/', response_model=AdminOut)
async def login(admin: AdminIn):
    db = get_my_sql_connection()

    username = admin.username
    password = admin.password

    try:
        cur = db.cursor()
        sqlstr = f"select * from user where username='{username}'"
        cur.execute(sqlstr)
        account = cur.fetchone()
    except Exception as e:
        print("Error in SQL:\n", e)

    if account:
        if password == account[2]:
            return {
                "id": account[0],
                "username": account[1],
                "role": account[3],
                "ormawa": account[4]
            }
