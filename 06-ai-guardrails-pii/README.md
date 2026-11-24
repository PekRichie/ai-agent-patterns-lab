# AI Guardrails: PII-maszkoló & Prompt-Injection Szűrő

## Miért értékes ez éles AI rendszerekben?
Személyes adatok (e-mail, telefon, bankkártya) redaktálása LLM-hívás előtt és tipikus prompt-injection minták blokkolása.

## Fájlok
- `app.py` — tiszta, függőségmentes Python 3 referencia-implementáció
- `test_app.py` — automatikus `unittest` tesztkészlet

## Futtatás
```bash
python3 -m unittest test_app.py -v
```
