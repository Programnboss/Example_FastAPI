from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from pydantic.types import conint

from sqlalchemy.sql.sqltypes import String


"""
This class is used to validate that a user post contains the attribute / value expected.  Along with the proper data type.
The published attribute is an example of a default value being assigned.
The rating attribute is an example of an attribute that can either be populated or not.  If not, None is assigned to the attribute.
"""
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    #rating: Optional[int] = None

#Determines the attributes needed to perform the GET/POST for users.
#Using inheritance in this instance, just because.
class PostCreate(PostBase):
    pass

#Determines the attributes needed to perform the GET/POST for users.
#Ref in the create of user.py
class UserCreate(BaseModel):
    email: EmailStr
    password: str

#Response back to the user when performing GETS/POSTS for users.
#Ref in create and get_user in user.py
class UserOut(BaseModel):
    id: int 
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True 


#Response back to the user when performing GETS/POSTS for posts.
#Using inheritance in this instance, just because.
#Ref in post.py
class Post(PostCreate):
    id: int
    # title: str
    # content: str
    # published: bool
    created_at: datetime
    owner_id: int
    owner: UserOut 

    class Config:
        orm_mode = True 

#Ref in post.py under the get all posts router
class PostOut(BaseModel): 
    Post: Post 
    votes: int   
    
    class Config:
        orm_mode = True
    
#Ref in auth.py to validate user credentials.
class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None 


# Ref in the vote.py file.
class Vote(BaseModel):
    post_id: int
    dir: conint(ge=0,le=1)

    