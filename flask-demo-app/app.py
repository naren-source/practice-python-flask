from flask import Flask
app = Flask(__name__)


stores = [
    {
        "name": "My Store",
        "items": [
            {
                "name": "Chair",
                "price": 15.00
            }
        ]
    }
]


@app.get("/store")
def get_stores():
    return {"stores": stores}

# http://127.0.0.1:5000/store - accessed this way