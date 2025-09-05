from flask import Blueprint, jsonify, request
from services import generate_token
from models import User
from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from services import token_required
import requests


auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({"msg": "Missing required fields"}), 400

    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    new_user = User(username=username, email=email, password=hashed_password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "User registered successfully"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"msg": "Missing required fields"}), 400

    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password, password):
        token = generate_token(identity=user.id)
        return jsonify({"token": token,
                        "user_id": user.id,
                        "username": user.username}), 200

    return jsonify({"msg": "Invalid credentials"}), 401


import requests

@auth_bp.route('/all_users', methods=['GET'])
#@token_required
def get_all_users():
    users = User.query.all()
    user_list = [{"id": user.id, "username": user.username, "email": user.email} for user in users]
    return jsonify(user_list), 200


   
#Търси книги по ключова думи    
@auth_bp.route('/search_books', methods=['GET'])
def search_books():
    query = request.args.get('q')
    if not query:
        return jsonify({"msg": "Missing search query"}), 400

    base_url = "https://openlibrary.org/search.json"
    params = {
        "q": query,
        "fields": "key,title,author_name,first_publish_year,author_key"
    }

    try:
        # Първо търсене на книга/автор
        search_response = requests.get(base_url, params=params)
        search_response.raise_for_status()
        search_data = search_response.json()

        # Ако има поне един резултат, вземаме author_key
        if search_data.get("docs"):
            first_author_key = search_data["docs"][0].get("author_key", [None])[0]
            if first_author_key:
                # Вземаме всички книги на този автор
                author_url = f"https://openlibrary.org/authors/{first_author_key}/works.json"
                author_response = requests.get(author_url)
                author_response.raise_for_status()
                author_data = author_response.json()
                search_data["other_books_by_author"] = author_data.get("entries", [])

        return jsonify(search_data), 200

    except requests.exceptions.RequestException as e:
        return jsonify({"msg": "Error fetching data", "error": str(e)}), 500



#тръсене на книги
@auth_bp.route('/book', methods=['GET'])
def get_single_book():
    title = request.args.get('title')
    if not title:
        return jsonify({"msg": "Missing title query"}), 400

    url = f"https://openlibrary.org/search.json?title={title}&fields=key,title,author_name,first_publish_year,author_key"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if not data["docs"]:
            return jsonify({"msg": "No book found"}), 404

        book = data["docs"][0]
        return jsonify(book), 200

    except requests.exceptions.RequestException as e:
        return jsonify({"msg": "Error fetching data", "error": str(e)}), 500



#тръсене на автор
@auth_bp.route('/author_books/<author_key>', methods=['GET'])
def author_books(author_key):
    url = f"https://openlibrary.org/authors/{author_key}/works.json"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # Вземаме само основна информация от entries
        clean_entries = []
        for entry in data.get("entries", []):
            clean_entries.append({
                "title": entry.get("title"),
                "key": entry.get("key"),
                "description": entry.get("description", {}).get("value") if isinstance(entry.get("description"), dict) else entry.get("description"),
            })

        return jsonify({"books": clean_entries}), 200

    except requests.exceptions.RequestException as e:
        return jsonify({"msg": "Error fetching data", "error": str(e)}), 500



#информация за Автора 
@auth_bp.route('/author/<author_key>', methods=['GET'])
def author_details(author_key):
    try:
        # 1. Основни данни от author.json
        url = f"https://openlibrary.org/authors/{author_key}.json"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        author_name = data.get("name")

        # 2. Търсene na резюме по име 
        search_url = "https://openlibrary.org/search/authors.json"
        search_response = requests.get(search_url, params={"q": author_name})
        search_response.raise_for_status()
        search_data = search_response.json()

        author_summary = {}
        for doc in search_data.get("docs", []):
            if doc.get("key") == author_key:
                author_summary = doc
                break

        clean_data = {
            "key": data.get("key", "").replace("/authors/", ""),
            "name": author_name,
            "alternate_names": data.get("alternate_names", [])[:5],
            "birth_date": data.get("birth_date"),
            "bio": data.get("bio", {}).get("value") if isinstance(data.get("bio"), dict) else data.get("bio"),
            "top_work": author_summary.get("top_work"),
            "work_count": author_summary.get("work_count"),
            "top_subjects": author_summary.get("top_subjects", [])[:5],
            "ratings_average": author_summary.get("ratings_average"),
            "ratings_count": author_summary.get("ratings_count"),
        }

        return jsonify(clean_data), 200

    except requests.exceptions.RequestException as e:
        return jsonify({"msg": "Error fetching author data", "error": str(e)}), 500



#корици на книги 
from flask import redirect, request

@auth_bp.route('/cover/<int:cover_id>', methods=['GET'])
def get_cover(cover_id):
    size = request.args.get('size', 'L').upper()  # L, M или S
    if size not in ['L', 'M', 'S']:
        size = 'L'
    cover_url = f"https://covers.openlibrary.org/b/id/{cover_id}-{size}.jpg"
    return redirect(cover_url)





