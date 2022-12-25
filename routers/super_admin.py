from fastapi import APIRouter
from database import get_my_sql_connection
from pydantic import BaseModel
from flask import jsonify
from typing import Optional

router = APIRouter()

