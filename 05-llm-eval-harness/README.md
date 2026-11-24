# LLM Prompt-értékelő és Regressziós Tesztelő (Eval Harness)

## Miért értékes ez éles AI rendszerekben?
Automatikus prompt-minőségmérés arany tesztesetekkel (kötelező kulcsszavak, tiltott minták, max hossz, összesített pontszám).

## Fájlok
- `app.py` — tiszta, függőségmentes Python 3 referencia-implementáció
- `test_app.py` — automatikus `unittest` tesztkészlet

## Futtatás
```bash
python3 -m unittest test_app.py -v
```
