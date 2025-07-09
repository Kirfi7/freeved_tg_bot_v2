from typing import Literal, Optional, List
from pydantic import BaseModel



class User(BaseModel):
    telegram_id: int
    is_verified: bool = False
    is_banned: bool = False


class PostAttachment(BaseModel):
    file_type: str
    file_id: str


class PostInit(BaseModel):
    author_id: int
    author_username: Optional[str]
    post_type: Literal['Помогите советом', 'Обратите внимание']
    attachment: Optional[PostAttachment] = None
    post_text: str
    comment_subscribers: List[int]


class Post(PostInit):
    id: int
    telegram_id: Optional[int] = None
    is_published: bool = False