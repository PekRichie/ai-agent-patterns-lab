# Strukturált LLM Kimenet Parser & Repair Hurok

## Miért értékes ez éles AI rendszerekben?
Az LLM-ek gyakran kevernek prózát vagy Markdown-keretet a JSON válaszok köré, vagy elhagynak egy kötelező mezőt. Ez a modul kinyeri a JSON-t, ellenőrzi a mezők típusát, és hiba esetén pontos hibajelzéssel újrapróbálkozik (repair loop).

## Futtatás
```bash
python3 -m unittest test_app.py -v
```
