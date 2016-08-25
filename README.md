#



##


```
virtualenv -p /usr/bin/python3 venv
source venv/bin/activate
pip install -r requirements.txt 
```

## Generate IDF:

```
cd ~/git/HFIRSANSReduction/src 
python3 -m "instrument.generator"
```