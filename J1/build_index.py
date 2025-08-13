#!/usr/bin/env python3
# build_index_with_fields.py
# Varre ./decisoesTJSP, extrai campos dos .txt e gera docs.json completo para o site.

import os, re, json, csv
from datetime import datetime

SRC_DIR = "./decisoesTJSP"
OUT_JSON = "docs.json"
OUT_CSV = "docs_mapping.csv"
RECURSIVE = True
SNIPPET_CHARS = 400

# Padrões para captura de campos
PATTERNS = {
    "data": [
        r"Data de Disponibiliza(?:ç|c)ão\s*:\s*([0-9]{2}/[0-9]{2}/[0-9]{4})",
    ],
    "comarca": [
        r"Comarca\s*:\s*(.+)",
        r"COMARCA\s+de\s+(.+)"
    ],
    "vara": [
        r"Vara\s*:\s*(.+)",
        r"Vara\s+Única"
    ],
    "juiz": [
        r"Juiz(?:a)? de Direito\s*:\s*(.+)",
        r"Juiz(?:a)?\s*:\s*(.+)"
    ],
    "reu": [
        r"R[eé]u\s*:\s*(.+)",
        r"R[eé]us\s*:\s*(.+)"
    ],
    "assunto": [
        r"Assunto\s*:\s*(.+)"
    ]
}

def clean(s):
    if not s:
        return None
    s = s.strip()
    s = re.sub(r"\s+", " ", s)
    return s

def find_first(patterns, text, max_chars=300):
    for pat in patterns:
        m = re.search(pat, text, flags=re.I | re.M)
        if m:
            val = m.group(1) if m.groups() else m.group(0)
            return clean(val[:max_chars])
    return None

def parse_date_iso(s):
    if not s:
        return None
    try:
        return datetime.strptime(s.strip(), "%d/%m/%Y").date().isoformat()
    except Exception:
        return s.strip()

def filename_id(path):
    base = os.path.splitext(os.path.basename(path))[0]
    # tenta CNJ
    m = re.search(r"\d{7}-\d{2}\.\d{4}\.\d\.\d{4}\.\d{4}", base)
    return m.group(0) if m else base

def process_txt(path, files_set):
    base_id = filename_id(path)
    with open(path, encoding='utf-8', errors='ignore') as fh:
        raw = fh.read()
    raw_norm = re.sub(r"\r\n?", "\n", raw)

    data = {
        "No. Processo": base_id,
        "Data": parse_date_iso(find_first(PATTERNS['data'], raw_norm)),
        "Comarca": find_first(PATTERNS['comarca'], raw_norm),
        "Vara": find_first(PATTERNS['vara'], raw_norm),
        "Juiz": find_first(PATTERNS['juiz'], raw_norm),
        "Réu": find_first(PATTERNS['reu'], raw_norm),
        "Assunto": find_first(PATTERNS['assunto'], raw_norm)
    }

    # PDF com mesmo ID ou mesmo nome do arquivo
    pdf = None
    for cand in (base_id + ".pdf", base_id + ".PDF",
                 os.path.splitext(os.path.basename(path))[0] + ".pdf",
                 os.path.splitext(os.path.basename(path))[0] + ".PDF"):
        if cand in files_set:
            pdf = cand
            break

    snippet = re.sub(r"\s+", " ", raw_norm)[:SNIPPET_CHARS]

    return {
        "id": base_id,
        **data,
        "pdf": pdf,
        "txt": os.path.basename(path),
        "snippet": snippet
    }

def main():
    files = []
    if RECURSIVE:
        for root, _, fns in os.walk(SRC_DIR):
            for f in fns:
                if f.lower().endswith(('.pdf', '.txt')):
                    files.append(os.path.join(root, f))
    else:
        for f in os.listdir(SRC_DIR):
            if f.lower().endswith(('.pdf', '.txt')):
                files.append(os.path.join(SRC_DIR, f))

    files_set = {os.path.basename(f) for f in files}
    txt_files = sorted([f for f in files if f.lower().endswith('.txt')])

    entries = []
    for txt in txt_files:
        entries.append(process_txt(txt, files_set))

    # Salva JSON
    with open(OUT_JSON, 'w', encoding='utf-8') as fh:
        json.dump(entries, fh, ensure_ascii=False, indent=2)

    # Salva CSV
    headers = ["No. Processo","Data","Comarca","Vara","Juiz","Réu","Assunto","pdf","txt"]
    with open(OUT_CSV, 'w', encoding='utf-8', newline='') as csvf:
        writer = csv.DictWriter(csvf, fieldnames=headers)
        writer.writeheader()
        for e in entries:
            writer.writerow({h: e.get(h, "") for h in headers})

    print(f"Wrote {len(entries)} entries to {OUT_JSON} and {OUT_CSV}")

if __name__ == "__main__":
    main()