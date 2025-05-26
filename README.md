# 📦 XML Parser API

Este projeto é uma API desenvolvida em Python com Flask para fazer upload de arquivos XML e retornar seus dados estruturados em formato JSON. Ele é especialmente útil para processar documentos como **Notas Fiscais Eletrônicas (NF-e)** e integrá-los com sistemas como o de **cadastro de compras**.

## 🚀 Funcionalidades

- Upload de arquivos XML via `POST`
- Remoção automática de namespaces XML
- Conversão completa de XML para JSON com atributos e hierarquia preservados
- Suporte a CORS (para integração com frontends como React)

## 🔧 Tecnologias Utilizadas

- [Python 3.x](https://www.python.org/)
- [Flask](https://flask.palletsprojects.com/)
- [Flask-CORS](https://flask-cors.readthedocs.io/)

## 📁 Estrutura

```bash
.
├── app.py         # Código principal da API
└── README.md      # Documentação do projeto
```

## 🧪 Como usar

### 1. Clone o repositório

```bash
git clone [https://github.com/seu-usuario/nome-do-repositorio.git](https://github.com/eskivx/OCR-Invoice.git)

```

### 2. Crie um ambiente virtual (opcional, mas recomendado)

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt


```

### 4. Execute a aplicação

```bash
python app.py
```

A aplicação estará disponível em `http://localhost:5000`.

## 🧾 Endpoint

### `POST /upload`

Faz o upload de um arquivo XML e retorna seu conteúdo como JSON.

#### Exemplo com `curl`

```bash
curl -X POST -F "file=@caminho/para/arquivo.xml" http://localhost:5000/upload
```

#### Resposta esperada:

```json
{
  "nfeProc": {
    "NFe": {
      "infNFe": {
        "ide": {
          "cUF": "42",
          "natOp": "VENDA"
        }
      }
    }
  }
}
```

## 🌐 CORS

O CORS está habilitado para o frontend local rodando em:

```
http://localhost:5173
```

Caso queira alterar a origem permitida, modifique esta linha no `app.py`:

```python
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})
```

## 📌 Possíveis melhorias

- Extração automática de campos específicos da NF-e (ex: CNPJ, data, valor total, etc.)
- Armazenamento dos dados extraídos em banco de dados
- Interface gráfica para upload via navegador

## 🛡️ Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

