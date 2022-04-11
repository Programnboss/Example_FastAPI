import ldap3 

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