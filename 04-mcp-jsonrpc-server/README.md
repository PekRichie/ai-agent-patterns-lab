# MCP (Model Context Protocol) JSON-RPC 2.0 Mini-szerver

## Miért értékes ez éles AI rendszerekben?
Szabványos MCP `initialize`, `tools/list` és `tools/call` kérések feldolgozása tiszta JSON-RPC 2.0 rétegen.

## Fájlok
- `app.py` — tiszta, függőségmentes Python 3 referencia-implementáció
- `test_app.py` — automatikus `unittest` tesztkészlet

## Futtatás
```bash
python3 -m unittest test_app.py -v
```
