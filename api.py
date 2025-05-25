from flask import Flask, request, jsonify
from flask_cors import CORS
import xml.etree.ElementTree as ET

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

def remove_namespace(doc):
    for elem in doc.iter():
        if '}' in elem.tag:
            elem.tag = elem.tag.split('}', 1)[1]
    return doc

def xml_to_dict(elem):
    d = {}
    if elem.attrib:
        d['@attributes'] = elem.attrib

    text = elem.text.strip() if elem.text else ''
    if text:
        d['#text'] = text

    children = list(elem)
    if children:
        child_dict = {}
        for child in children:
            child_res = xml_to_dict(child)
            tag = child.tag
            if tag not in child_dict:
                child_dict[tag] = []
            child_dict[tag].append(child_res)

        for tag, items in child_dict.items():
            if len(items) == 1:
                child_dict[tag] = items[0]

        d.update(child_dict)

    return d

@app.route('/upload', methods=['POST'])
def parse_xml_full():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    xml_content = file.read()

    try:
        root = ET.fromstring(xml_content)
    except ET.ParseError:
        return jsonify({"error": "Invalid XML file"}), 400

    root = remove_namespace(root)
    data_dict = {root.tag: xml_to_dict(root)}

    return jsonify(data_dict)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
