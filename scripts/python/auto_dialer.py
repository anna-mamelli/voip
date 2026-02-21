#!/usr/bin/env python3
# Automate d'appels sortants depuis fichier CSV
import csv, random, time, os, sys
from datetime import datetime

SPOOL_DIR = "/var/spool/asterisk/outgoing"
CONTEXT   = "internal"
EXTENSION = "s"
PRIORITY  = "1"
WAIT_TIME = 30
DELAY_MIN = 5
DELAY_MAX = 15

def load_contacts(csv_path):
    contacts = []
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            contacts.append(row)
    return contacts

def create_call_file(contact):
    number = contact['phone']
    name   = contact.get('name', 'Contact')
    ts     = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    fname  = f"{SPOOL_DIR}/{ts}_{number}.call"

    content = f"""Channel: PJSIP/{number}
CallerID: "Automate" <0000>
MaxRetries: 1
RetryTime: 30
WaitTime: {WAIT_TIME}
Context: {CONTEXT}
Extension: {number}
Priority: 1
SetVar: CONTACT_NAME={name}
"""
    tmp = fname + '.tmp'
    with open(tmp, 'w') as f:
        f.write(content)
    os.rename(tmp, fname)
    print(f"[{datetime.now():%H:%M:%S}] Appel créé : {name} ({number})")

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 auto_dialer.py contacts.csv")
        sys.exit(1)

    contacts = load_contacts(sys.argv[1])
    random.shuffle(contacts)
    print(f"Chargé {len(contacts)} contacts — début campagne")

    for contact in contacts:
        create_call_file(contact)
        delay = random.uniform(DELAY_MIN, DELAY_MAX)
        print(f"Prochain appel dans {delay:.1f} secondes...")
        time.sleep(delay)

    print("Campagne terminée.")

if __name__ == '__main__':
    main()
