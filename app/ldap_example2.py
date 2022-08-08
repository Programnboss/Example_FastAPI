from ldap3 import Server, Connection, ObjectDef, AttrDef, Reader, Writer, ALL

server = Server('ipa.demo1.freeipa.org', get_info=ALL)
conn = Connection(server, \
    'uid=admin,cn=users,cn=accounts,dc=demo1,dc=freeipa,dc=org',
    'Secret123', 
    auto_bind=True)

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

'''
Working with the Reader Cursor

'''

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

'''
Working with the Writer Cursor.
'''
r = Reader(conn, obj_person,\
    'cn=users,cn=accounts,dc=demo1,dc=freeipa,dc=org')

r.search()
w = Writer.from_cursor(r)
print(w)
print('-' * 30)
print(w[0])
print('-' * 30)
