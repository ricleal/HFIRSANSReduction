# HFIR SANS Reduction

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

### Classes

`sans.data.Data`
Generic data class. 
Here should go all data reduction routines common to SANS!
It has the attributes:
- `df`: Dataframe where we going to put for every single detector: x,y,z,I,Sigma(I),Q,etc....
- `meta`: Dictionary with metadata usefull for the reduction

`sans.parser.Parser`
Generic parser. Base class. Every facility or instrument should implement this class with routines:
- `getMetadata(self, xpath)`
- `getData(self, xpath)`
Those routines are used to get a value from the data file using `xpath` concept.

`sans.data.<facility>.parser.Parser`
Specific parser to a facility
It fills the generic class Data attibutes `df` and `meta`.

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

```
Y
^
|
|   ^ Z
|  /
| /
|/
---------->X
```

Z - Will be from the sample to the detector


