#!/usr/bin/env python3
# parse_fields_exact.py
# Extrai: No. Processo, Data (Data de Disponibilização), Comarca, Vara, Juiz, Réu
# Saídas: docs.json e docs_mapping.csv
# Uso: rode na pasta com os .txt (ou ajuste SRC_DIR)

import os
import re
import json
import csv
from datetime import datetime

SRC_DIR = "./decisoesTJSP"               # pasta com os arquivos (ex: "./downloads")
OUT_JSON = "docs.json"
OUT_CSV  = "docs_mapping.csv"
SNIPPET_CHARS = 400

# padrões (listas para tentar variantes)
PATTERNS = {
    "processo": [
        r"([0-9]{7}\-[0-9]{2}\.[0-9]{4}\.[0-9]\.[0-9]{4}\.[0-9]{4})",             # CNJ clássico
        r"Processo(?:\s+Digital)?\s*(?:n[ºo]\s*|nº\s*|n\.)?\s*[:º\.\s-]*\s*([0-9\-\./]{10,})",
        r"Processo\s*[:\-]\s*([0-9\-\./]{10,})"
    ],
    "data": [
        r"Data de Disponibiliza(?:ç|c)ão\s*:\s*([0-9]{2}\/[0-9]{2}\/[0-9]{4})",
        r"Data\s*[:\-]\s*([0-9]{2}\/[0-9]{2}\/[0-9]{4})",
        r"Disponibiliza(?:ç|c)ão\s*[:\-]\s*([0-9]{2}\/[0-9]{2}\/[0-9]{4})"
    ],
    "comarca": [
        r"Comarca\s*[:\-]\s*(.+)",
        r"COMARCA\s+de\s+(.+)",
        r"COMARCA\s*[:\-]?\s*(.+)"
    ],
    "vara": [
        r"Vara\s*[:\-]\s*(.+)",
        r"Vara\s+Única",
        r"Vara\s+[:\-]?\s*(.+)"
    ],
    "juiz": [
        r"Juiz de Direito\s*:\s*(.+)",
        r"Juiz(?:a)?\s*[:\-]\s*(.+)",
        r"Juiz(?:a)?(?:\s+de\s+Direito)?\s*[:\-]\s*(.+)"
    ],
    "reu": [
        r"R[eé]u\s*:\s*(.+)",
        r"R[eé]us?\s*:\s*(.+)",
        r"R[eé]u\(s\)\s*:\s*(.+)",
        r"R[eé]u(?:s)?\s*[:\-]\s*(.+)"
    ]
}

def clean(s):
    if s is None:
        return None
    s = s.strip()
    # remove múltiplos espaços e quebras de linha
    s = re.sub(r"\s+", " ", s)
    # remove traços finais estranhos
    return s

def find_first(patterns, text, max_chars=300):
    for pat in patterns:
        m = re.search(pat, text, flags=re.I | re.M)
        if m:
            # prefer group 1 if existir
            if m.groups():
                val = m.group(1)
            else:
                val = m.group(0)
            # limitar comprimento razoável
            return clean(val[:max_chars])
    return None

def parse_date_iso(s):
    if not s: return None
    s = s.strip()
    try:
        return datetime.strptime(s, "%d/%m/%Y").date().isoformat()
    except Exception:
        return s  # retorna original se falhar

def process_txt(path, files_set):
    with open(path, encoding='utf-8', errors='ignore') as fh:
        raw = fh.read()

    # normalizar espaços para facilitar regex multiline
    raw_norm = re.sub(r"\r\n?", "\n", raw)

    data = {}
    data['processo'] = find_first(PATTERNS['processo'], raw_norm, max_chars=80)
    data['data'] = parse_date_iso(find_first(PATTERNS['data'], raw_norm, max_chars=20))
    data['comarca'] = find_first(PATTERNS['comarca'], raw_norm, max_chars=120)
    data['vara'] = find_first(PATTERNS['vara'], raw_norm, max_chars=120)
    data['juiz'] = find_first(PATTERNS['juiz'], raw_norm, max_chars=120)
    data['reu'] = find_first(PATTERNS['reu'], raw_norm, max_chars=200)

    base = os.path.splitext(os.path.basename(path))[0]
    # acha pdf com mesmo base (se existir)
    pdf = None
    for cand in (base + ".pdf", base + ".PDF"):
        if cand in files_set:
            pdf = cand
            break

    snippet = re.sub(r"\s+", " ", raw_norm)[:SNIPPET_CHARS]

    return {
        "id": data['processo'] or base,
        "No. Processo": data['processo'] or "",
        "Data": data['data'] or "",
        "Comarca": data['comarca'] or "",
        "Vara": data['vara'] or "",
        "Juiz": data['juiz'] or "",
        "Réu": data['reu'] or "",
        "pdf": pdf,
        "txt": os.path.basename(path),
        "snippet": snippet
    }

def main():
    files = [f for f in os.listdir(SRC_DIR) if os.path.isfile(os.path.join(SRC_DIR, f))]
    files_set = set(files)
    txts = sorted([os.path.join(SRC_DIR, f) for f in files if f.lower().endswith('.txt')])

    entries = []
    incomplete = []

    for txt in txts:
        try:
            e = process_txt(txt, files_set)
            entries.append(e)
            # marca se algum campo essencial estiver vazio (para revisão)
            if not e["No. Processo"] or not e["Data"] or not e["Réu"]:
                incomplete.append(e["txt"])
        except Exception as ex:
            print("Erro processando", txt, ":", ex)

    # grava JSON
    with open(OUT_JSON, 'w', encoding='utf-8') as fh:
        json.dump(entries, fh, ensure_ascii=False, indent=2)

    # grava CSV com colunas na ordem solicitada
    headers = ["No. Processo","Data","Comarca","Vara","Juiz","Réu","pdf","txt"]
    with open(OUT_CSV, 'w', encoding='utf-8', newline='') as csvf:
        writer = csv.DictWriter(csvf, fieldnames=headers)
        writer.writeheader()
        for e in entries:
            writer.writerow({h: e.get(h, "") for h in headers})

    print(f"Wrote {len(entries)} entries to {OUT_JSON} and {OUT_CSV}")
    if incomplete:
        print("Arquivos com campos essenciais possivelmente faltando (revisar):")
        for x in incomplete:
            print(" -", x)

if __name__ == "__main__":
    main()

