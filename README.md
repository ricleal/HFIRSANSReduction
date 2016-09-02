# HFIR SANS REduction

Under development.


## Architecture

```
├── src
│   └── sans
│       ├── beam_center.py
│       ├── data.py
│       ├── hfir
│       │   ├── biosans
│       │   │   └── data.py
│       │   ├── data.py
│       │   ├── gpsans
│       │   │   └── data.py
│       │   └── parser.py
│       └── parser.py
```

`sans.data`
Generic data class
`sans.parser`
Generic parser

## Instalation

**Requisites**:
- python3
- pip + virtualenv
- jupyter


```
virtualenv -p /usr/bin/python3 venv
source venv/bin/activate
pip install -r requirements.txt
```

## Left-Handed Coordinate Systems

'''
Y
^
|
|   ^ Z
|  /
| /
|/
---------->X
'''

Z - Will be from the sample to the detector


