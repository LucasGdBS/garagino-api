from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from models.users import User, UserAuth
from config.database import db
from passlib.context import CryptContext
from datetime import datetime, timedelta, UTC
import jwt
from decouple import config
from schema.schemas import to_dict

router = APIRouter()

crypt_context = CryptContext(schemes=['sha256_crypt'])
SECRET_KEY = config('SECRET_KEY')
ALGORITHM = config('ALGORITHM')

collection_name = db["garagino_users_collection"]

# TODO: Implementar validação de dados do usuario
@router.post("/register")
async def register(user: User):
    '''Metodo responsavel por registrar um novo usuario'''
    user_db = User(
        username=user.username,
        password=crypt_context.hash(user.password),
        email=user.email,
        full_name=user.full_name
    )
    try:
        collection_name.insert_one(user_db.model_dump())
        return JSONResponse(
                content={'Registro': 'Sucesso'},
                status_code=status.HTTP_201_CREATED
            )
    except Exception as e:
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/login")
async def login(user: UserAuth):
    '''Metodo responsavel por autenticar um usuario'''
    user_db = collection_name.find_one({'username': user.username})
    user_db = to_dict(user_db)
    

    if user_db is None:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Email ou Senha incorretos'
        )
    
    if not crypt_context.verify(user.password, user_db['password']):
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Email ou senha invalido'
        )
    
    expires_in = 5
    exp = datetime.now(UTC) + timedelta(hours=expires_in)

    payload = {
        'exp': exp,
        'iat': datetime.now(UTC),
        'sub': user.username
    }

    token = {'token': jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM), 'username': user_db['username']}

    response = JSONResponse(content={'Message': 'Login Realizado com sucesso'})
    response.set_cookie(
        key='access_token',
        value=f'Bearer {token["token"]}',
        httponly=True,
        secure=True,
        samesite='Strict',
    )

    return response




