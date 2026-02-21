#!/usr/bin/env python3
# Import utilisateurs depuis LDAP vers Asterisk
import ldap
import subprocess

LDAP_SERVER = "ldap://192.168.204.129"
LDAP_BASE   = "ou=users,dc=datatrust,dc=local"
LDAP_USER   = "cn=admin,dc=datatrust,dc=local"
LDAP_PASS   = "azerty"

PJSIP_FILE  = "/etc/asterisk/pjsip_ldap.conf"
VM_FILE     = "/etc/asterisk/voicemail_ldap.conf"

def get_ldap_users():
    """Récupère les utilisateurs depuis LDAP"""
    conn = ldap.initialize(LDAP_SERVER)
    conn.simple_bind_s(LDAP_USER, LDAP_PASS)
    
    results = conn.search_s(
        LDAP_BASE,
        ldap.SCOPE_SUBTREE,
        '(objectClass=inetOrgPerson)',
        ['cn', 'mail', 'telephoneNumber', 'uid']
    )
    
    users = []
    for dn, attrs in results:
        if 'telephoneNumber' in attrs:
            users.append({
                'extension': attrs['telephoneNumber'][0].decode('utf-8'),
                'name': attrs['cn'][0].decode('utf-8'),
                'email': attrs['mail'][0].decode('utf-8') if 'mail' in attrs else '',
                'uid': attrs['uid'][0].decode('utf-8')
            })
    
    conn.unbind()
    return users

def generate_pjsip_config(users):
    """Génère la config PJSIP"""
    config = []
    for user in users:
        ext = user['extension']
        name = user['name']
        pwd = "azerty"  # Mot de passe généré
        
        config.append(f"""
[{ext}]
type=endpoint
context=internal
disallow=all
allow=ulaw,alaw,g722
auth=auth{ext}
aors={ext}
callerid="{name}" <{ext}>

[auth{ext}]
type=auth
auth_type=userpass
username={ext}
password={pwd}

[{ext}]
type=aor
max_contacts=2
remove_existing=yes
""")
    return '\n'.join(config)

def generate_voicemail_config(users):
    """Génère la config voicemail"""
    config = ["[default]"]
    for user in users:
        ext = user['extension']
        name = user['name']
        email = user['email']
        pin = ext  # PIN = numéro d'extension
        config.append(f"{ext} => {pin},{name},{email}")
    return '\n'.join(config)

def main():
    print("Récupération des utilisateurs LDAP...")
    users = get_ldap_users()
    print(f"✓ {len(users)} utilisateurs trouvés")
    
    print("Génération pjsip_ldap.conf...")
    pjsip_config = generate_pjsip_config(users)
    with open(PJSIP_FILE, 'w') as f:
        f.write(pjsip_config)
    
    print("Génération voicemail_ldap.conf...")
    vm_config = generate_voicemail_config(users)
    with open(VM_FILE, 'w') as f:
        f.write(vm_config)
    
    print("Rechargement Asterisk...")
    subprocess.run(['asterisk', '-rx', 'pjsip reload'])
    subprocess.run(['asterisk', '-rx', 'voicemail reload'])
    
    print("\n✓ Import terminé !")
    print("\nUtilisateurs importés :")
    for user in users:
        print(f"  - {user['name']} (ext {user['extension']}, pwd: azerty")

if __name__ == '__main__':
    main()
