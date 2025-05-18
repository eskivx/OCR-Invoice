from flask import Flask, request, jsonify
from flask_cors import CORS
import fitz
import re
from datetime import datetime

app = Flask(__name__)
CORS(app, origins=["http://localhost:5173"])

@app.route('/parse-pdf', methods=['POST'])
def parse_pdf():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    file_stream = file.read()
    doc = fitz.open(stream=file_stream, filetype="pdf")
    text = "".join([page.get_text() for page in doc])

    metadata = doc.metadata
    data_pdf = metadata.get("modDate") or metadata.get("creationDate")

    # Formatar data do PDF
    data_pdf_formatada = ""
    if data_pdf and data_pdf.startswith("D:"):
        try:
            data_pdf_formatada = datetime.strptime(data_pdf[2:16], "%Y%m%d%H%M%S").strftime("%d/%m/%Y")
        except:
            data_pdf_formatada = ""

    doc.close()

    # Captura itens com fornecedor incluso
    item_regex = r"(\d+)\s+unidade\(s\) de:\s*(.*?)\s+Vendido por:\s*(.*?)\s+Condição:.*?R\$ ([\d.,]+)"
    matches = re.findall(item_regex, text, re.DOTALL)

    itens = []
    for match in matches:
        quantidade, nome, fornecedor, valor = match
        itens.append({
            "nome_produto": nome.strip(),
            "quantidade": int(quantidade),
            "fornecedorNome": fornecedor.strip(),
            "valor_unitario": valor.replace(".", "").replace(",", ".")
        })

    data_pedido = re.search(r"Pedido feito:\s*([\d]{1,2} de \w+ de \d{4})", text)
    total_geral = re.search(r"Total geral:\s*R\$ ([\d.,]+)", text)

    result = {
        "itemNomes": itens,
        "preco": total_geral.group(1).replace(".", "").replace(",", ".") if total_geral else "",
        "dataCompra": data_pedido.group(1) if data_pedido else "",
        "dataInvoice": data_pdf_formatada
    }

    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

