import os
from docling.document_converter import DocumentConverter

# Forçar uso de CPU
os.environ["DOCLING_DEVICE"] = "cpu"

# Caminho para o PDF
pdf_path = "ESCEFATELBT01_0001742576_0000001077A.pdf"

# Inicializar e converter
converter = DocumentConverter()
result = converter.convert(pdf_path)

# Exportar Markdown
with open("saida.md", "w", encoding="utf-8") as f:
    f.write(result.document.export_to_markdown())

# Exportar JSON
with open("saida.json", "w", encoding="utf-8") as f:
    f.write(result.document.export_to_json())

print("Arquivos gerados: saida.md e saida.json")