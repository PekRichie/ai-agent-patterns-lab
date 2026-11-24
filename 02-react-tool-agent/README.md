# ReAct Tool-Calling Ügynök-hurok (Safe Sandbox)

## Miért értékes ez éles AI rendszerekben?
Eszköz-regiszter, lépéskorlát (`max_steps`), strukturált tool-meghívás és megfigyelhetőségi nyomkövetés (trace).

## Fájlok
- `app.py` — tiszta, függőségmentes Python 3 referencia-implementáció
- `test_app.py` — automatikus `unittest` tesztkészlet

## Futtatás
```bash
python3 -m unittest test_app.py -v
```
