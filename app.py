from fastapi import FastAPI
from database import get_my_sql_connection
from routers import ormawa, user, kegiatan, super_admin, auth

api = FastAPI()

api.include_router(ormawa.router)
api.include_router(user.router)
api.include_router(kegiatan.router)
api.include_router(super_admin.router)
api.include_router(auth.router)