from fastapi import APIRouter, Depends, status
from src.api.v1.schemas import UserCreate, UserLogin
from src.services import UserService, get_user_service
from fastapi_jwt_auth import AuthJWT

router = APIRouter()


@router.post(
    path="/signup",
    status_code=status.HTTP_201_CREATED,
    summary="Регистрация",
    tags=["use"],
)
def sign_up(
    user_data: UserCreate,
    user_service: UserService = Depends(get_user_service),
):
    return user_service.create_user(user_data)


@router.post(
    path="/login",
    summary="Войти",
    tags=["use"],
)
def sign_in(
    user_data: UserLogin,
    auth_service: UserService = Depends(get_user_service),
    auth: AuthJWT = Depends(),
):
    return auth_service.login(auth, user_data)


@router.post(
    path='/refresh',
    summary='Обновить токен токена',
    tags=['use'],
)
def refresh_token(
    user_service: UserService = Depends(get_user_service),
    auth: AuthJWT = Depends(),
):
    return user_service.refresh_token(auth)