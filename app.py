from fastapi import FastAPI
from routers import ormawa, user, kegiatan, super_admin, auth, galeri, prestasi

api = FastAPI()
api.include_router(ormawa.router)
api.include_router(user.router)
api.include_router(kegiatan.router)
api.include_router(super_admin.router)
api.include_router(auth.router)
api.include_router(galeri.router)
api.include_router(prestasi.router)