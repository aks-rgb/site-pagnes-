import sqlite3

connexion = sqlite3.connect("database.db")
cursor = connexion.cursor()

# TABLE USERS améliorée
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT DEFAULT 'client',
        telephone TEXT,
        adresse TEXT,
        date_inscription TEXT
    )
""")

# TABLE PRODUITS améliorée
cursor.execute("""
    CREATE TABLE IF NOT EXISTS produits(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL,
        prix TEXT NOT NULL,
        image TEXT NOT NULL,
        description TEXT,
        prix_original TEXT,
        categorie TEXT DEFAULT 'general',
        stock INTEGER DEFAULT 10,
        en_vedette INTEGER DEFAULT 0
    )
""")

# TABLE COMMANDES
cursor.execute("""
    CREATE TABLE IF NOT EXISTS commandes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        date_commande TEXT,
        total TEXT,
        adresse TEXT,
        telephone TEXT,
        statut TEXT DEFAULT 'en_attente',
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
""")

# TABLE COMMANDE_PRODUITS
cursor.execute("""
    CREATE TABLE IF NOT EXISTS commande_produits(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        commande_id INTEGER,
        produit_id INTEGER,
        quantite INTEGER,
        prix TEXT,
        FOREIGN KEY (commande_id) REFERENCES commandes(id)
    )
""")

# Ajout catégorie à produits existants (si besoin)
try:
    cursor.execute("ALTER TABLE produits ADD COLUMN categorie TEXT DEFAULT 'general'")
except:
    pass

try:
    cursor.execute("ALTER TABLE produits ADD COLUMN stock INTEGER DEFAULT 10")
except:
    pass

# Produits par défaut avec catégories
produits_defaut = [
    ("Wax Prestige", "15 000 FCFA", "https://images.unsplash.com/photo-1606761568499-6d2451b23c66?w=300", "Pagne moderne haut de gamme", "premium", 15),
    ("Bazin Royal", "20 000 FCFA", "https://images.unsplash.com/photo-1560343090-f0409e92791a?w=300", "Collection élégante africaine", "premium", 10),
    ("Ankara Fashion", "12 000 FCFA", "https://images.unsplash.com/photo-1524253482453-3fed8d2fe12b?w=300", "Style moderne et tendance", "classique", 20),
    ("Tissu Cérémonie", "25 000 FCFA", "https://images.unsplash.com/photo-1539008835657-9e8e9680c956?w=300", "Idéal pour mariages", "ceremonie", 5),
    ("Pagne Tissé", "18 000 FCFA", "https://images.unsplash.com/photo-1597404294360-feeeda04612e?w=300", "Fait main, qualité supérieure", "premium", 8),
    ("Collection Été", "10 000 FCFA", "https://images.unsplash.com/photo-1618354691373-d851c5c3a990?w=300", "Tissu léger pour été", "saison", 25)
]

for produit in produits_defaut:
    try:
        cursor.execute("""
            INSERT INTO produits (nom, prix, image, description, categorie, stock)
            VALUES (?, ?, ?, ?, ?, ?)
        """, produit)
        print(f"✓ {produit[0]} ajouté")
    except:
        print(f"~ {produit[0]} existe déjà")

# Admin par défaut
try:
    cursor.execute("""
        INSERT INTO users (nom, email, password, role, date_inscription)
        VALUES (?, ?, ?, ?, ?)
    """, ("Admin", "admin@gmail.com", "1234", "admin", "2024-01-01"))
    print("✓ Admin créé (admin@gmail.com / 1234)")
except:
    print("~ Admin existe déjà")

connexion.commit()
connexion.close()

print("\n✅ Base de données améliorée avec succès !")
print("   - Nouveaux produits ajoutés")
print("   - Table commandes créée")
print("   - Catégories ajoutées")