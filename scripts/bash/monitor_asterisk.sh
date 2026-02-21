#!/bin/bash
# Supervision Asterisk
LOG="/var/log/asterisk/monitoring.log"
TS=$(date '+%Y-%m-%d %H:%M:%S')

# Appels actifs
CALLS=$(asterisk -rx 'core show channels count' 2>/dev/null | grep 'active call' | awk '{print $1}')

# État du service
STATUS=$(systemctl is-active asterisk)

# Peers enregistrés
PEERS=$(asterisk -rx 'pjsip show contacts' 2>/dev/null | grep -c 'Contact:.*sip:')

# Charge système
LOAD=$(uptime | awk -F'load average:' '{print $2}' | cut -d, -f1 | xargs)

# RAM utilisée
MEM=$(free -m | awk 'NR==2{printf "%.1f%%", $3*100/$2 }')

# CPU utilisé
CPU=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)

echo "[$TS] Status=$STATUS | Calls=$CALLS | Peers=$PEERS | Load=$LOAD | CPU=$CPU% | MEM=$MEM" >> $LOG

# Alerte si Asterisk arrêté
if [ "$STATUS" != "active" ]; then
    echo "ALERTE: Asterisk inactif à $TS" | tee -a $LOG
fi

# Alerte si aucun peer connecté
if [ "$PEERS" -eq 0 ]; then
    echo "ALERTE: Aucun peer connecté à $TS" | tee -a $LOG
fi
