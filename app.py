from flask import Flask, request, jsonify, render_template, session
from flask_cors import CORS
import sqlite3
from functools import wraps
from datetime import datetime

app = Flask(__name__)
app.secret_key = "antou_guiny_2026_secret_key"
CORS(app)

# ====================================
# DECORATEURS
# ====================================

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user_id'):
            return jsonify({"error": "Non autorisé"}), 401
        return f(*args, **kwargs)
    return decorated_function

def role_required(allowed_roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not session.get('user_id'):
                return jsonify({"error": "Non autorisé"}), 401
            if session.get('user_role') not in allowed_roles:
                return jsonify({"error": "Permission refusée"}), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# ====================================
# ROUTES PAGES
# ====================================

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login-page")
def login_page():
    return render_template("login.html")

@app.route("/register-page")
def register_page():
    return render_template("register.html")

@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/admin-dashboard")
@role_required(['admin'])
def admin_dashboard():
    return render_template("admin_dashboard.html")

@app.route("/mes-commandes")
@login_required
def mes_commandes():
    return render_template("commandes.html")

@app.route("/profil")
@login_required
def profil():
    return render_template("profil.html")

@app.route("/panier")
def panier():
    return render_template("panier.html")

# ====================================
# API AUTHENTIFICATION
# ====================================

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    nom = data.get("nom")
    email = data.get("email")
    password = data.get("password")
    
    if not all([nom, email, password]):
        return jsonify({"error": "Tous les champs sont requis"}), 400
    
    connexion = sqlite3.connect("database.db")
    cursor = connexion.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO users (nom, email, password, role, date_inscription)
            VALUES(?, ?, ?, 'client', ?)
        """, (nom, email, password, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        
        connexion.commit()
        return jsonify({"message": "Compte créé avec succès"})
    
    except sqlite3.IntegrityError:
        return jsonify({"error": "Email déjà utilisé"}), 400
    
    finally:
        connexion.close()

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")
    
    connexion = sqlite3.connect("database.db")
    cursor = connexion.cursor()
    
    cursor.execute("""
        SELECT id, nom, email, password, role FROM users
        WHERE email = ? AND password = ?
    """, (email, password))
    
    user = cursor.fetchone()
    connexion.close()
    
    if user:
        session['user_id'] = user[0]
        session['user_email'] = user[2]
        session['user_role'] = user[4]
        session['user_nom'] = user[1]
        
        return jsonify({
            "message": "Connexion réussie",
            "role": user[4],
            "user_id": user[0],
            "nom": user[1]
        })
    else:
        return jsonify({"error": "Email ou mot de passe incorrect"}), 401

@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"message": "Déconnecté"})

@app.route("/tous-les-produits")
def tous_les_produits():
    return render_template("tous-les-produits.html")


# Ajoute cette route dans app.py (après /logout)

@app.route("/check-session", methods=["GET"])
def check_session():
    """Vérifie si l'utilisateur est connecté"""
    if session.get('user_id'):
        return jsonify({
            "connected": True,
            "role": session.get('user_role'),
            "nom": session.get('user_nom'),
            "email": session.get('user_email')
        })
    return jsonify({"connected": False})

@app.route("/user/profile", methods=["GET"])
@login_required
def user_profile():
    connexion = sqlite3.connect("database.db")
    cursor = connexion.cursor()
    
    cursor.execute("SELECT nom, email, date_inscription FROM users WHERE id = ?", (session['user_id'],))
    user = cursor.fetchone()
    connexion.close()
    
    if user:
        return jsonify({
            "nom": user[0],
            "email": user[1],
            "date_inscription": user[2]
        })
    return jsonify({"error": "Utilisateur non trouvé"}), 404
# ====================================
# API PRODUITS
# ====================================

@app.route("/products", methods=["GET"])
def products():
    categorie = request.args.get('categorie')
    limite = request.args.get('limite')
    
    connexion = sqlite3.connect("database.db")
    cursor = connexion.cursor()
    
    query = "SELECT * FROM produits"
    params = []
    
    if categorie:
        query += " WHERE categorie = ?"
        params.append(categorie)
    
    query += " ORDER BY id DESC"
    
    if limite:
        query += " LIMIT ?"
        params.append(int(limite))
    
    cursor.execute(query, params)
    produits = cursor.fetchall()
    connexion.close()
    
    liste = []
    for produit in produits:
        liste.append({
            "id": produit[0],
            "nom": produit[1],
            "prix": produit[2],
            "prix_original": produit[5] if len(produit) > 5 else None,
            "image": produit[3],
            "description": produit[4] if produit[4] else "",
            "categorie": produit[6] if len(produit) > 6 else "general",
            "stock": produit[7] if len(produit) > 7 else 10
        })
    
    return jsonify(liste)

@app.route("/product/<int:product_id>", methods=["GET"])
def product_detail(product_id):
    connexion = sqlite3.connect("database.db")
    cursor = connexion.cursor()
    
    cursor.execute("SELECT * FROM produits WHERE id = ?", (product_id,))
    produit = cursor.fetchone()
    connexion.close()
    
    if produit:
        return jsonify({
            "id": produit[0],
            "nom": produit[1],
            "prix": produit[2],
            "image": produit[3],
            "description": produit[4]
        })
    return jsonify({"error": "Produit non trouvé"}), 404

@app.route("/add-product", methods=["POST"])
@role_required(['admin'])
def add_product():
    data = request.json
    
    nom = data.get("nom")
    prix = data.get("prix")
    image = data.get("image")
    description = data.get("description")
    categorie = data.get("categorie", "general")
    stock = data.get("stock", 10)
    
    connexion = sqlite3.connect("database.db")
    cursor = connexion.cursor()
    
    cursor.execute("""
        INSERT INTO produits (nom, prix, image, description, categorie, stock)
        VALUES(?, ?, ?, ?, ?, ?)
    """, (nom, prix, image, description, categorie, stock))
    
    connexion.commit()
    connexion.close()
    
    return jsonify({"message": "Produit ajouté"})

@app.route("/update-product/<int:product_id>", methods=["PUT"])
@role_required(['admin'])
def update_product(product_id):
    data = request.json
    
    connexion = sqlite3.connect("database.db")
    cursor = connexion.cursor()
    
    cursor.execute("""
        UPDATE produits 
        SET nom=?, prix=?, image=?, description=?, categorie=?, stock=?
        WHERE id=?
    """, (data.get("nom"), data.get("prix"), data.get("image"), 
          data.get("description"), data.get("categorie"), data.get("stock"), product_id))
    
    connexion.commit()
    connexion.close()
    
    return jsonify({"message": "Produit modifié"})

@app.route("/delete-product/<int:product_id>", methods=["DELETE"])
@role_required(['admin'])
def delete_product(product_id):
    connexion = sqlite3.connect("database.db")
    cursor = connexion.cursor()
    
    cursor.execute("DELETE FROM produits WHERE id = ?", (product_id,))
    connexion.commit()
    connexion.close()
    
    return jsonify({"message": "Produit supprimé"})

# ====================================
# API PANIER & COMMANDES
# ====================================

@app.route("/commande", methods=["POST"])
@login_required
def creer_commande():
    data = request.json
    panier = data.get("panier")
    total = data.get("total")
    adresse = data.get("adresse")
    telephone = data.get("telephone")
    
    connexion = sqlite3.connect("database.db")
    cursor = connexion.cursor()
    
    cursor.execute("""
        INSERT INTO commandes (user_id, date_commande, total, adresse, telephone, statut)
        VALUES(?, ?, ?, ?, ?, 'en_attente')
    """, (session['user_id'], datetime.now().strftime("%Y-%m-%d %H:%M:%S"), total, adresse, telephone))
    
    commande_id = cursor.lastrowid
    
    for item in panier:
        cursor.execute("""
            INSERT INTO commande_produits (commande_id, produit_id, quantite, prix)
            VALUES(?, ?, ?, ?)
        """, (commande_id, item['id'], item['quantite'], item['prix']))
    
    connexion.commit()
    connexion.close()
    
    return jsonify({"message": "Commande créée", "commande_id": commande_id})

@app.route("/mes-commandes-api", methods=["GET"])
@login_required
def get_mes_commandes():
    connexion = sqlite3.connect("database.db")
    cursor = connexion.cursor()
    
    cursor.execute("""
        SELECT id, date_commande, total, statut 
        FROM commandes 
        WHERE user_id = ? 
        ORDER BY id DESC
    """, (session['user_id'],))
    
    commandes = cursor.fetchall()
    connexion.close()
    
    liste = []
    for cmd in commandes:
        liste.append({
            "id": cmd[0],
            "date": cmd[1],
            "total": cmd[2],
            "statut": cmd[3]
        })
    
    return jsonify(liste)

# ====================================
# API STATISTIQUES (ADMIN)
# ====================================

@app.route("/admin/stats", methods=["GET"])
@role_required(['admin'])
def admin_stats():
    connexion = sqlite3.connect("database.db")
    cursor = connexion.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM users")
    total_clients = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM produits")
    total_produits = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM commandes")
    total_commandes = cursor.fetchone()[0]
    
    cursor.execute("SELECT SUM(total) FROM commandes WHERE statut = 'livree'")
    total_ventes = cursor.fetchone()[0] or 0
    
    connexion.close()
    
    return jsonify({
        "total_clients": total_clients,
        "total_produits": total_produits,
        "total_commandes": total_commandes,
        "total_ventes": total_ventes
    })

if __name__ == "__main__":
    app.run(debug=True)