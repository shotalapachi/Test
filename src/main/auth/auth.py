from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database.database import get_db
from starlette import status
from .schema import UserCreateSchema
from ..database.models import Users
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import timedelta, datetime


router = APIRouter(
    prefix='/auth',
    tags=['auth']
)


SECRET_KEY = '0074e59e20931b4f4025a3f127e9d4a6f4f7d915ad9432f94dc976d96a0bf5f8'
ALGORITHM = 'HS256'

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
bearer = OAuth2PasswordBearer(tokenUrl='/auth/token')


@router.post('/', status_code=status.HTTP_201_CREATED)
async def crete_new_user(new_user: UserCreateSchema, db: Session = Depends(get_db)):
    user = Users()
    user.username = new_user.username
    user.hashed_password = bcrypt_context.hash(new_user.password)

    db.add(user)
    db.commit()
    db.refresh(user)


@router.post('/token')
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                                 db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Wrong Credentials')
    token = create_access_token(user.username, user.id, timedelta(minutes=30))

    return {"access_token": token, "token_type": "bearer"}


async def get_current_user(token: str = Depends(bearer)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('username')
        user_id: str = payload.get('id')

        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Wrong Credentials')
        return {'username': username, 'id': user_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Wrong Credentials')
def authenticate_user(username: str, password: str, db):
    user = db.query(Users).filter(Users.username == username).first()

    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user


def create_access_token(username: str, user_id: int, expire_date: timedelta):
    encode = {'username': username, 'id': user_id}
    expires = datetime.utcnow() + expire_date
    encode.update({'expiration': str(expires)})

    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)



