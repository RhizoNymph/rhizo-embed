from flask import Flask, request, jsonify
from .search.scholar import search_authors, search_pubs
from .search.arxiv import general_search

app = Flask(__name__)

@app.route('/scholar/authors', methods=['GET'])
def search_authors():
    author_name = request.args.get('name', '')
    if author_name:
        try:
            authors = search_authors(author_name)
            return jsonify(authors), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "Author name is required"}), 400

@app.route('/scholar/publications', methods=['GET'])
def search_publications():
    pub_title = request.args.get('title', '')
    if pub_title:
        try:
            publications = search_pubs(pub_title)
            return jsonify(publications), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "Publication title is required"}), 400

@app.route('/arxiv', methods=['GET'])
def search_arxiv():
    query = request.args.get('query', '')
    if query:
        try:
            results = general_search(query)
            return jsonify(results), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "Query is required"}), 400

if __name__ == '__main__':
    app.run(debug=True)
