#!/usr/bin/env python3
# DnD automatique : disponible 9h-18h, DnD sinon
import subprocess
from datetime import datetime

USERS      = ['1001', '1002']
HOUR_START = 9
HOUR_END   = 18

def set_dnd(extension, enabled):
    state = 'YES' if enabled else 'NO'
    subprocess.run(
        ['sudo', 'asterisk', '-rx', f'database put DND {extension} {state}'],
        capture_output=True
    )
    status = 'ACTIF' if enabled else 'INACTIF'
    print(f"DnD {extension}: {status}")

def main():
    now  = datetime.now()
    hour = now.hour
    day  = now.weekday()  # 0=Lundi, 6=Dimanche

    # Weekends et hors horaires = DnD activé
    dnd = day >= 5 or not (HOUR_START <= hour < HOUR_END)

    for user in USERS:
        set_dnd(user, dnd)

if __name__ == '__main__':
    main()
