# datosarray.py
#
# Los datos ya no viven hardcodeados aquí: se leen desde datosarray.json
# (requisito de la evaluación: la información debe almacenarse en archivo(s) JSON).
# Se conservan los nombres `periodo` y `personas` para no tener que tocar
# ninguna otra parte del proyecto que ya los importa.

import json
from pathlib import Path

_DATA_PATH = Path(__file__).resolve().parent / "datosarray.json"

with open(_DATA_PATH, encoding="utf-8") as _archivo:
    _datos = json.load(_archivo)

periodo = _datos["periodo"]
personas = _datos["personas"]
