from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt
from fastapi import HTTPException, Security, status
from decouple import config

SECRET_KEY = config('SECRET_KEY')
ALGORITHM = config('ALGORITHM')

def verify_token(token):
    '''Metodo responsavel por verificar se o token enviado é válido'''
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload['sub']
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Signature has expired'
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid Token'
        )

def auth_wrapper(auth: HTTPAuthorizationCredentials = Security(HTTPBearer())):
    '''Metodo responsavel por ler o token passado como parametro no header das requisições é válido
    Deve ser passado como Depends para os endpoints que precisam de autenticação'''
    return verify_token(auth.credentials)