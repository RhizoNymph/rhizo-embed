from flask import Flask, request, jsonify
from .search import scihub

app = Flask(__name__)

@app.route('/search/authors', methods=['GET'])
def search_authors():
    author_name = request.args.get('author_name', '')
    if author_name:
        try:
            authors = scihub.search_authors(author_name)
            return jsonify(authors), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "Author name is required"}), 400

@app.route('/search/publications', methods=['GET'])
def search_publications():
    pub_title = request.args.get('pub_title', '')
    if pub_title:
        try:
            publications = scihub.search_pubs(pub_title)
            return jsonify(publications), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "Publication title is required"}), 400

if __name__ == '__main__':
    app.run(debug=True)
