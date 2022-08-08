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
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import settings
from ldap3 import Server, Connection, ALL, ObjectDef, Reader, Writer
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from ldap3.core.exceptions import LDAPException

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

security = HTTPBasic()
LDAP_HOST = 'ipa.demo1.freeipa.org'
# LDAP_HOST = 'mur-api.icam.disa.mil'
# LDAP_PORT = 2636
LDAP_PORT = 389

def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    server = Server(host=LDAP_HOST, use_ssl=False, get_info=ALL)
    conn = Connection(server,'uid=admin,cn=users,cn=accounts,dc=demo1,dc=freeipa,dc=org', 'Secret123', auto_bind=True)

    # Create a container for new entries
    conn.add('ou=ldap3-tutorial,dc=demo1,dc=freeipa,dc=org', \
    'organizationalUnit')

    # Add a new user
    conn.add('cn=b.young,ou=ldap3-tutorial,dc=demo1,dc=freeipa,dc=org', 'inetOrgPerson', \
        {'givenName': 'Beatrix', 
        'sn': 'Young', 
        'departmentNumber': 'Dev', 
        'telephoneNumber': 1111})

    conn.modify_dn('cn=b.young,ou=ldap3-tutorial,dc=demo1,dc=freeipa,dc=org', \
    'cn=b.smith')

    # print(server.info)
    # print(server.schema)
    print(server.schema.object_classes['inetOrgPerson'])
    print(server.schema.object_classes['organizationalPerson'])
    print(server.schema.object_classes['Person'])
    print(server.schema.object_classes['top'])

    # Reading the objectClass attribute of the user created above.
    conn.search('ou=ldap3-tutorial,dc=demo1,dc=freeipa,dc=org', \
    '(cn=*)', attributes=['objectclass'])
    print(conn.entries[0])

    conn.search('dc=demo1,dc=freeipa,dc=org', '(&(objectclass=person)(uid=admin))', attributes=['sn','krbLastPwdChange', 'objectclass'])

    entries = conn.extend.standard.paged_search('dc=demo1,dc=freeipa,dc=org', '(objectClass=person)', attributes=['cn', 'givenName'], paged_size=5)
    # for entry in entries:
    #     print(entry)
    # print(conn.entries[0])
    # print(conn.entries[0].entry_to_ldif())
    entry = conn.entries[0]
    print(entry.entry_to_json())

    searchParameters = { 'search_base': 'dc=demo1,dc=freeipa,dc=org',
                      'search_filter': '(&(objectClass=inetuser)(cn=*))',
                      'attributes': ['cn', 'givenName','sn','departmentNumber','telephoneNumber'],
                      'paged_size': 5 }
    while True:
        conn.search(**searchParameters)
        for entry in conn.entries:
            print(entry)
        cookie = conn.result['controls']['1.2.840.113556.1.4.319']['value']['cookie']
        if cookie:
            searchParameters['paged_cookie'] = cookie
        else:
            break

    # conn.search('ou=ldap3-tutorial,dc=demo1,dc=freeipa,dc=org', \
    #         '(cn=b.smith)',
    #         attributes=['objectclass', 'sn', 'cn', 'givenname'])
    # print(conn.entries)

    # conn.search('dc=demo1,dc=freeipa,dc=org', '(&(objectclass=person)(uid=admin))', attributes=['sn','krbLastPwdChange', 'objectclass'])
    # conn.search('ou=ldap3-tutorial,dc=demo1,dc=freeipa,dc=org', \
    # '(cn=*)', attributes=['objectclass'])
    # print(conn.entries)
    # inputs = conn.extend.standard.paged_search('dc=demo1,dc=freeipa,dc=org', '(objectClass=person)', attributes=['cn', 'givenName'], paged_size=5)
    # return inputs
    obj_person = ObjectDef('person', conn)
    obj_inetorgperson = ObjectDef('inetOrgPerson', conn)

    r = Reader(conn, obj_inetorgperson, 'ou=ldap3-tutorial,dc=demo1,dc=freeipa,dc=org')
    r.search()

    # Print a useful representation of an Entry
    print(r[0])
    print('-' * 30)
    # Get the DN of an entry.
    print(r[0].entry_dn)
    print('-' * 30)
    # Query the attributes in the Entry as a list of names.
    # Then loop through the schema.
    for attrib in r[0].entry_attributes:
        print(attrib)
    print('-' * 30)
    # Query the attributes in the Entry as a dict of key/value pairs
    print(r[0].entry_attributes_as_dict)
    print('-' * 30)
    # Check for mandatory attributes
    print('-' * 30)
    print(r[0].entry_mandatory_attributes)
    print('-' * 30)
    # Convert the Entry to LDIF
    print('-' * 30)
    print(r[0].entry_to_ldif())
    print('-' * 30)
    # Convert the Entry to JSON
    print('-' * 30)
    print(r[0].entry_to_json(include_empty=False))  # Use include_empty=True to include empty attributes
    print('-' * 30)

    print('-' * 30)
    print('-' * 30)

    # Show that obj_person doesn't have the uid attribute
    print('-' * 30)
    print(obj_person)
    print('-' * 30)
    # Add the UID attribute to the container
    obj_person += 'uid' # implicitly creates a new AttrDef
    print(obj_person)
    print('-' * 30)

    # Build the Reader cursor, using the Simplified Query Language.
    r = Reader(conn, obj_person,\
    'cn=users,cn=accounts,dc=demo1,dc=freeipa,dc=org',
    'uid:=admin')
    print(r)
    print('-' * 30)
    print(r.search())
    print('-' * 30)

    obj_person = ObjectDef(['person', 'posixAccount', 'krbprincipalaux'], conn)
    r = Reader(conn, obj_person,\
    'cn=users,cn=accounts,dc=demo1,dc=freeipa,dc=org',
    'uid:=admin')
    print(r)
    print('-' * 30)
    print(r.search())
    print('-' * 30)
    print(r[0]) 
    print('-' * 30)
    return conn.entries
    
# @ == Decorator | fastapi variable | HTTP Method | Path operation or route
# Function must immediately follow Decorator.

@app.get("/")
def root(username: str = Depends(get_current_username)):
    return {"message": f"Welcome {username}, Keep L'Dappen like a Boss!"}
'''    
    return {"message": f"{list(data)}"}

@app.get("/")
def root():
    return {"message": "Hello World!"}

'''

