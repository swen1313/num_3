from functools import lru_cache
from fastapi import Depends
from sqlmodel import Session
from jose import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from src.api.v1.schemas import UserCreate, UserLogin, User, UserEmail
from src.db import AbstractCache, get_cache, get_session
from src.models import User
from src.services import ServiceMixin
from src.core import config, config_all
from fastapi_jwt_auth import AuthJWT

__all__ = ("UserService", "get_user_service")


class UserService(ServiceMixin):

    def get_payload(self, payload: dict) -> str:
        return jwt.encode(payload, config_all.JWT_SECRET_KEY, config_all.JWT_ALGORITHM)

    def create_user(self, user_data: UserCreate) -> dict:
        if self.session.query(User).filter(User.username == user_data.username).first():
            return {"error": f"User {user_data.username} already registered"}
        user = User(
            email=user_data.email,
            username=user_data.username,
            password=generate_password_hash(user_data.password),
        )

        self.session.add(user)
        self.session.commit()



        return {"msg": "User Created.", "user": user}

    def login(self, _jwt: AuthJWT, user: UserLogin) -> dict:
        _user = (
            self.session.query(User).filter(User.username == user.username).first()
        )
        if not _user:
            return {'error': 'User does not exist'}
        if not check_password_hash(_user.password, user.password):
            return {'error': 'Wrong password'}

        refresh_token = _jwt.create_refresh_token(subject=_user.username)
        config.active_refresh_tokens.sadd(_user.uuid, refresh_token)
        return {'access_token': _jwt.create_access_token(subject=_user.username),
                'refresh_token': refresh_token}

    def refresh_token(self, _jwt: AuthJWT) -> dict:
        _jwt.jwt_refresh_token_required()
        _username = _jwt.get_jwt_subject()
        user_uuid = (self.session.query(User)
                     .filter(User.username == _username).first().uuid
                     )
        payload = _jwt.get_raw_jwt()
        new_refresh_token = _jwt.create_refresh_token(subject=_username)
        config.active_refresh_tokens.sadd(user_uuid, new_refresh_token)
        config.active_refresh_tokens.srem(user_uuid, self.get_payload(payload))
        return {"access_token": _jwt.create_access_token(subject=_username),
                "refresh_token": new_refresh_token}

    def user_info(self, jwt) -> dict:
        jwt.jwt_required()
        user_data = (
            self.session.query(User).filter(
                User.username == jwt.get_jwt_subject())
                .first()
        )
        return {"user": User.from_orm(user_data)}

    def user_modify(self, _jwt, user: UserEmail) -> dict:
        _jwt.jwt_required()
        _username = _jwt.get_jwt_subject()
        _user = (
            self.session.query(User).filter(User.username == _username).first()
        )
        if self.session.query(User).filter(User.username == user.username).first():
            return {"error": "User exists"}
        for key, value in user.dict().items():
            setattr(_user, key, value)

        self.session.add(_user)
        self.session.commit()
        self.session.refresh(_user)
        config.blocked_access_tokens.setex(_jwt.get_raw_jwt()["jti"],
                                                config.config.JWT_ACCESS_EXPIRES_S, "true"
                                                )
        return {"user": User.from_orm(_user),
                "access_token": _jwt.create_access_token(subject=user.username)
                }


@lru_cache()
def get_user_service(
        cache: AbstractCache = Depends(get_cache),
        session: Session = Depends(get_session),
) -> UserService:
    return UserService(cache=cache, session=session)