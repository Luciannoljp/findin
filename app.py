import os
from flask import Flask, request, jsonify, render_template
from search_engine import run_search
from config import Config

app = Flask(
    __name__,
    static_folder="static",
    static_url_path="/static"
)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/search")
def search():
    query = request.args.get("q", "")
    min_price = request.args.get("min_price", type=float)
    max_price = request.args.get("max_price", type=float)
    store = request.args.get("store")
    category = request.args.get("category")
    page = request.args.get("page", default=1, type=int)

    try:
        data = run_search(
            query=query,
            min_price=min_price,
            max_price=max_price,
            store=store,
            category=category,
            page=page,
            page_size=9
        )
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    # Porta dinâmica para produção (Render)
    port = int(os.environ.get("PORT", 5000))

    # debug=False é obrigatório em produção
    app.run(host="0.0.0.0", port=port, debug=False)