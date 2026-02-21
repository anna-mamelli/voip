#!/bin/bash
while true; do
    clear
    echo "=========================================="
    echo "    ASTERISK MONITORING DASHBOARD"
    echo "=========================================="
    echo ""
    echo "Service Status : $(systemctl is-active asterisk)"
    echo "Uptime         : $(asterisk -rx 'core show uptime' 2>/dev/null | grep 'System uptime' | cut -d: -f2-)"
    echo ""
    echo "Active Calls   : $(asterisk -rx 'core show channels count' 2>/dev/null | grep 'active call' | awk '{print $1}')"
    echo "Peers Online   : $(asterisk -rx 'pjsip show contacts' 2>/dev/null | grep -c 'Contact:.*sip:')"
    echo ""
    echo "CPU Load       : $(uptime | awk -F'load average:' '{print $2}')"
    echo "Memory Used    : $(free -m | awk 'NR==2{printf "%s/%sMB (%.1f%%)", $3,$2,$3*100/$2 }')"
    echo ""
    echo "=========================================="
    echo "Press Ctrl+C to exit"
    sleep 5
done
