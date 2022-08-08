from ldap3 import Server, Connection, ALL
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from ldap3.core.exceptions import LDAPException

app = FastAPI()
security = HTTPBasic()
LDAP_HOST = "ipa.demo1.freeipa.org"
LDAP_PORT = 389


def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    server = Server(host=LDAP_HOST, port=LDAP_PORT, use_ssl=False, get_info=ALL)
    try:
        with Connection(
            server=server,
            authentication="SIMPLE",
            user='uid=admin,cn=users,cn=accounts,dc=demo1,dc=freeipa,dc=org',# credentials.username,
            password='Secret123', # credentials.password,
            read_only=True,
        ) as connection:
            print(connection.result)  # "success" if bind is ok 
            print(server.info)           
            return credentials.username
    except LDAPException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials"
        )

    
   

# @ == Decorator | fastapi variable | HTTP Method | Path operation or route
# Function must immediately follow Decorator.

@app.get("/")
def root(username: str = Depends(get_current_username)):
    return {"message": f"Welcome {username}, Keep L'Dappen like a Boss!"}



