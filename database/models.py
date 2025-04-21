from typing import Literal, Optional
from pydantic import BaseModel


class User(BaseModel):
    telegram_id: int
    telegram_username: Optional[str]
    is_verified: bool
    is_banned: bool


class Post(BaseModel):
    id: int
    author_id: int
    author_username: Optional[str]
    post_type: Literal['Помогите советом', 'Обратите внимание']
    is_published: bool


class CommentSub(BaseModel):
    comment_id: int
    subscriber_id: int