#  Create a new virtual environment
#  py -3 -m venv venv
#  python -m ensurepip --upgrade 

#  Activate the .ps1 file for terminal window to use the venv.
#  & D:\MyPythonProjects\FastAPI\venv\Scripts\Activate.ps1
#  venv\Scripts\Activate.ps1

#  To see all pkgs installed after running a "pip install <anything>":
#  pip freeze

#  Start the server, on the local box, by running the following command:
#  uvicorn app.main:app --reload
#  Open a web browser and type in http://127.0.0.1:8000, 127.0.0.1:8000/docs, 127.0.0.1:8000/redoc
#  Then come back into VSCode to see the server reponses returned.

#  Object Relational Mapper (ORM)
#  Sqlalchemy most popular ORM and stand alone module.
#  Provides a layer of abstraction.
#  FastAPI no longer has to speak to SQL.

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import settings

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# "*" allows anyone access to api.  
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

# @ == Decorator | fastapi variable | HTTP Method | Path operation or route
# Function must immediately follow Decorator.

@app.get("/")
def root():
    return {"message": "Hello World!"}

