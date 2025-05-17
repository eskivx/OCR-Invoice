from flask import Flask, request, jsonify
from flask_cors import CORS
import fitz
import re

app = Flask(__name__)

CORS(app, origins=["http://localhost:5173"])

@app.route('/parse-pdf', methods=['POST'])
def parse_pdf():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    doc = fitz.open(stream=file.read(), filetype="pdf")
    
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()

    fornecedor = re.search(r"FORNECEDOR:\s*(.+)", text)
    itens = re.search(r"ITENS:\s*(.+)", text)
    preco = re.search(r"PREÇO TOTAL DA COMPRA:\s*([\d,.]+)\s*R\$", text)
    data = re.search(r"DATA DA COMPRA:\s*(\d{2}/\d{2}/\d{4})", text)

    result = {
        "fornecedor": fornecedor.group(1) if fornecedor else "",
        "itens": [item.strip() for item in itens.group(1).split(",")] if itens else [],
        "preco_total": preco.group(1).replace(",", ".") if preco else "",
        "data_compra": data.group(1) if data else ""
    }
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
