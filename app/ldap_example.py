from ldap3 import Server, Connection, ALL, MODIFY_ADD, MODIFY_DELETE, MODIFY_REPLACE
from ldap3 import Tls
import ssl
from ldap3.utils.dn import safe_rdn

'''
Operators allowed in an assertion are:
= (equal), 
<= (less than or equal), 
>= (greater than or equal), 
=* (present), 
~= (approximate),
:= (extensible).

Different Server operations:
server.info
server.schema
server.schema.object_classes['inetOrgPerson']
server.schema.object_classes['organizationalPerson']
server.schema.object_classes['Person']

'''

# Using the Search operation to perform a Pages search.
server = Server('ipa.demo1.freeipa.org', get_info=ALL)
conn = Connection(server, 'uid=admin,cn=users,cn=accounts,dc=demo1,dc=freeipa,dc=org', 'Secret123', auto_bind=True)

# Create a container for new entries
conn.add('ou=ldap3-tutorial,dc=demo1,dc=freeipa,dc=org', \
    'organizationalUnit')
conn.add('ou=moved,ou=ldap3-tutorial,dc=demo1,dc=freeipa,dc=org', \
    'organizationalUnit')
# Add a new user
conn.add('cn=b.young,ou=ldap3-tutorial,dc=demo1,dc=freeipa,dc=org', 'inetOrgPerson', \
    {'givenName': 'Beatrix', 
    'sn': 'Young', 
    'departmentNumber': 'Dev', 
    'telephoneNumber': 1111})

conn.add('cn=m.johnson,ou=ldap3-tutorial,dc=demo1,dc=freeipa,dc=org', \
    'inetOrgPerson', 
    {'givenName': 'Mary Ann', 
    'sn': 'Johnson', 
    'departmentNumber': 'DEV', 
    'telephoneNumber': 2222})

conn.add('cn=q.gray,ou=ldap3-tutorial,dc=demo1,dc=freeipa,dc=org', \
    'inetOrgPerson', 
    {'givenName': 'Quentin', 
    'sn': 'Gray', 
    'departmentNumber': 'QA', 
    'telephoneNumber': 3333})

searchParameters = { 'search_base': 'dc=demo1,dc=freeipa,dc=org',
                      'search_filter': '(objectClass=Person)',
                      'attributes': ['cn', 'givenName','sn','departmentNumber','telephoneNumber'],
                      'paged_size': 5 }
while True:
    conn.search(**searchParameters)
    for entry in conn.entries:
        pass# print(entry)
    cookie = conn.result['controls']['1.2.840.113556.1.4.319']['value']['cookie']
    if cookie:
        searchParameters['paged_cookie'] = cookie
    else:
        break

# print(server.schema.object_classes['inetOrgPerson'])
# print(server.schema.object_classes['organizationalPerson'])
# Person provides the "Must contain attributes: sn, cn"
# print(server.schema.object_classes['Person'])
# Top provides the "Must contain attributes: objectClass"
# print(server.schema.object_classes['top'])

# Reading the objectClass attribute of the user created above.
conn.search('ou=ldap3-tutorial,dc=demo1,dc=freeipa,dc=org', \
    '(cn=*)', attributes=['objectclass'])
# print(conn.entries[0])

# Changing the 'Relative Distinguished Name (RDN)' with ModifyDN
conn.modify_dn('cn=b.young,ou=ldap3-tutorial,dc=demo1,dc=freeipa,dc=org', \
    'cn=b.smith')
conn.search('ou=ldap3-tutorial,dc=demo1,dc=freeipa,dc=org', \
    '(cn=b.smith)', 
    attributes=['objectclass', 'sn', 'cn', 'givenname'])
# print(conn.entries[0])

# ModifyDN is also used to move an entry to another container.
conn.modify_dn('cn=b.smith,ou=ldap3-tutorial,dc=demo1,dc=freeipa,dc=org', \
    'cn=b.smith', 
    new_superior='ou=moved,ou=ldap3-tutorial,dc=demo1,dc=freeipa,dc=org')
conn.search('ou=moved,ou=ldap3-tutorial,dc=demo1,dc=freeipa,dc=org', \
    '(cn=b.smith)', 
    attributes=['objectclass', 'sn', 'cn', 'givenname'])
# print(conn.entries[0])

# print(safe_rdn('cn=b.smith,ou=moved,ou=ldap3-tutorial,dc=demo1,dc=freeipa,dc=org'))
# print(safe_rdn('cn=b.smith+sn=young,ou=moved,ou=ldap3-tutorial,dc=demo1,dc=freeipa,dc=org'))

# Although I changed the cn=b.young to cn=b.smith the sn=Young
# is still in the container.  It takes these operations to 
# change sn=Young to sn=Smyth.
conn.modify('cn=b.smith,ou=moved,ou=ldap3-tutorial,dc=demo1,dc=freeipa,dc=org', \
    {'sn': [(MODIFY_ADD, ['Smyth'])]})
conn.search('ou=moved,ou=ldap3-tutorial,dc=demo1,dc=freeipa,dc=org', '(cn=b.smith)', attributes=['cn', 'sn'])
# Now we can delete the sn=Young
conn.modify('cn=b.smith,ou=moved,ou=ldap3-tutorial,dc=demo1,dc=freeipa,dc=org', \
    {'sn': [(MODIFY_DELETE, ['Young'])]})
conn.search('ou=moved,ou=ldap3-tutorial,dc=demo1,dc=freeipa,dc=org', '(cn=b.smith)', attributes=['cn', 'sn'])
# Correct the misspelling of Smyth to Smith.
conn.modify('cn=b.smith,ou=moved,ou=ldap3-tutorial,dc=demo1,dc=freeipa,dc=org', \
    {'sn': [(MODIFY_REPLACE, ['Smith'])]})
conn.search('ou=moved,ou=ldap3-tutorial,dc=demo1,dc=freeipa,dc=org', '(cn=b.smith)', attributes=['cn', 'sn'])

# Showing all three MODIFY_'s can be used in one query
conn.modify('cn=b.smith,ou=moved,ou=ldap3-tutorial,dc=demo1,dc=freeipa,dc=org', {'sn': [(MODIFY_ADD, ['Young', 'Johnson']), (MODIFY_DELETE, ['Smith'])], 'givenname': [(MODIFY_REPLACE, ['Mary', 'Jane'])]})
conn.search('ou=moved,ou=ldap3-tutorial,dc=demo1,dc=freeipa,dc=org', '(cn=b.smith)', attributes=['cn', 'sn', 'givenName'])

# Moving b.smith back to its original context and values.
# Adding a couple more entries.
conn.modify_dn('cn=b.smith,ou=moved,ou=ldap3-tutorial,dc=demo1,dc=freeipa,dc=org', \
    'cn=b.smith', 
    new_superior='ou=ldap3-tutorial,dc=demo1,dc=freeipa,dc=org')

conn.modify('cn=b.smith,ou=ldap3-tutorial,dc=demo1,dc=freeipa,dc=org', \
    {'sn': [(MODIFY_DELETE, ['Johnson'])], 
    'givenname': [(MODIFY_REPLACE, ['Beatrix'])]})

conn.modify_dn('cn=b.smith,ou=ldap3-tutorial,dc=demo1,dc=freeipa,dc=org', \
    'cn=b.young')

conn.search('ou=ldap3-tutorial,dc=demo1,dc=freeipa,dc=org', \
    '(cn=*)', attributes=['objectclass'])
print(conn.entries)



# server = Server('ipa.demo1.freeipa.org', get_info=ALL)
# conn = Connection(server, 'uid=admin,cn=users,cn=accounts,dc=demo1,dc=freeipa,dc=org', 'Secret123', auto_bind=True)
# conn.search('dc=demo1,dc=freeipa,dc=org', '(&(objectclass=person)(uid=admin))', attributes=['sn','krbLastPwdChange', 'objectclass'])

# entries = conn.extend.standard.paged_search('dc=demo1,dc=freeipa,dc=org', '(objectClass=person)', attributes=['cn', 'givenName'], paged_size=5)
# for entry in entries:
#     print(entry)

# print(conn.entries[0].entry_to_ldif())
# entry = conn.entries[0]
# print(entry.entry_to_json())

# tls_configuration = Tls()
# server = Server('ipa.demo1.freeipa.org', use_ssl=True, get_info=ALL)
# tls_configuration.validate = ssl.CERT_NONE
# with Connection(server, 'uid=admin,cn=users,cn=accounts,dc=demo1,dc=freeipa,dc=org', 'Secret123') as conn:
#     conn.search('dc=demo1,dc=freeipa,dc=org', '(&(objectclass=person)(uid=admin))', attributes=['sn','krbLastPwdChange', 'objectclass'])
#     entry = conn.entries[0]

# conn.bound 
# print(entry)

# conn = Connection('ipa.demo1.freeipa.org', auto_bind= True)
#server = Server('ipa.demo1.freeipa.org', use_ssl=True, get_info=ALL)
#conn = Connection(server, 'uid=admin,cn=users,cn=accounts,dc=demo1,dc=freeipa,dc=org', 'Secret123', auto_bind=True)
#conn.start_tls()
#print(conn.extend.standard.who_am_i())
#print(conn)

#conn.bind 
# conn.__repr__()
#print(server.info)
#print(server.schema)


#tls_configuration = Tls(validate=ssl.CERT_REQUIRED, version=ssl.PROTOCOL_TLSv1)
# conn.open()

"""
tls_configuration = Tls(validate=ssl.CERT_NONE, version=ssl.PROTOCOL_TLSv1)
server = Server('ipa.demo1.freeipa.org', use_ssl=True, tls=tls_configuration)
conn = Connection(server)
print(conn)
"""



'''
LDAP_SERVER = 'ldap://example.com'
BASE_DN = 'dc=example,dc=com'  # base dn to search in
LDAP_LOGIN = 'ldap_login'
LDAP_PASSWORD = 'ldap_password'
OBJECT_TO_SEARCH = 'userPrincipalName=user@example.com'
ATTRIBUTES_TO_SEARCH = ['isMemberOf']

connect = ldap3.initialize(LDAP_SERVER)
connect.set_option(ldap3.OPT_REFERRALS, 0)  # to search the object and all its descendants
connect.simple_bind_s(LDAP_LOGIN, LDAP_PASSWORD)
result = connect.search_s(BASE_DN, ldap3.SCOPE_SUBTREE, OBJECT_TO_SEARCH, ATTRIBUTES_TO_SEARCH)
'''