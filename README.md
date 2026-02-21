# 📡 Projet VoIP Asterisk

Infrastructure VoIP complète avec Asterisk 22.8.2, LDAP, IVR, DnD et Docker.

## Fonctionnalités

- Serveur Asterisk 22.8.2 (PJSIP)
- Messagerie vocale sécurisée par PIN
- Menu IVR interactif en français
- Automate d'appels CSV
- Mode DnD automatique (9h-18h)
- Intégration LDAP
- Supervision et monitoring
- Conteneurisation Docker

## Structure
```
voip/
├── configs/asterisk/    # Configurations Asterisk
├── scripts/python/      # Scripts d'automatisation
├── scripts/bash/        # Scripts de supervision
├── docker/             # Solution Docker
└── docs/               # Documentation
```

## Installation

Voir la documentation dans `docs/`

## Licence

MIT
