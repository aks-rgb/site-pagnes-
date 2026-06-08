# update_local_images.py
import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Supprimer les anciens produits
cursor.execute("DELETE FROM produits")

# Ajouter les produits avec les images locales
produits = [
    ("Wax Prestige", "15000", "/static/images/wax-prestige.jpg", 
     "Pagne Wax haut de gamme - Idéal pour les cérémonies", "premium", 15),
    
    ("Bazin Royal", "20000", "/static/images/bazin-royal.jpg",
     "Bazin Riche - Collection royale pour cérémonies", "premium", 10),
    
    ("Ankara Fashion", "12000", "/static/images/ankara-fashion.jpg",
     "Ankara Fashion - Tendance et coloré", "classique", 20),

     ("Pad Prestige", "25000", "/static/images/jap.png", 
     "Pagne Wax haut de gamme - Idéal pour les cérémonies", "premium", 15),
    
    ("SAR Pestige", "30000", "/static/images/kar.png",
     "Tissue Riche - Collection royale pour cérémonies", "premium", 10),
    
    ("SHEKINA Fashion", "22000", "/static/images/OIP.png",
     "SHEKINA Fashion - Tendance et coloré", "classique", 20),

     ("Kente Royal", "35000", "/static/images/kente-royal.jpg",
     "Kente traditionnel du Ghana - Symbole de royauté", "premium", 5),
    
    ("Mudcloth Authentique", "28000", "/static/images/mudcloth.jpg",
     "Tissu fait main du Mali - Motifs traditionnels uniques", "premium", 8),
    
    ("Faso Dan Fani", "20000", "/static/images/faso-danfani.jpg",
     "Tissu traditionnel burkinabè - Coton tissé main", "premium", 12),
    
    # Classique - Quotidien
    ("Ankara Fashion", "12000", "/static/images/ankara-fashion.jpg",
     "Ankara moderne - Tendance et coloré pour le quotidien", "classique", 20),
    
    ("Kitenge Original", "10000", "/static/images/kitenge.jpg",
     "Kitenge d'Afrique de l'Est - Motifs colorés et variés", "classique", 25),
    
    ("Dutch Wax", "18000", "/static/images/dutch-wax.jpg",
     "Dutch Wax authentique - Résistant et de qualité", "classique", 18),
    
    ("African Print", "11000", "/static/images/african-print.jpg",
     "Imprimé africain polyvalent - Pour toutes les occasions", "classique", 30),
    
    ("Super Wax", "16000", "/static/images/super-wax.jpg",
     "Super Wax haute qualité - Idéal pour les tenues de tous les jours", "classique", 22),
    
    # Cérémonie - Mariages, baptêmes
    ("Lace Cérémonie", "45000", "/static/images/lace-ceremonie.jpg",
     "Dentelle de luxe - Pour mariages et grandes réceptions", "ceremonie", 8),
    
    ("Tissu Royal", "55000", "/static/images/tissu-royal.jpg",
     "Collection prestige - Pour chefs et grandes cérémonies", "ceremonie", 5),
    
    ("Satin Mariage", "30000", "/static/images/satin-mariage.jpg",
     "Satin brillant - Parfait pour les tenues de cérémonie", "ceremonie", 12),
    
    ("Velours Cérémonie", "40000", "/static/images/velours-ceremonie.jpg",
     "Velours de qualité - Élégance et raffinement", "ceremonie", 8),
    
    # Saison - Collections spéciales
    ("Collection Ramadan", "25000", "/static/images/ramadan-collection.jpg",
     "Tissus spéciaux pour le Ramadan - Confort et élégance", "saison", 10),
    
    ("Collection Noël", "20000", "/static/images/noel-collection.jpg",
     "Motifs festifs - Idéal pour les fêtes de fin d'année", "saison", 15),
    
    ("Collection Été", "12000", "/static/images/collection-ete.jpg",
     "Tissu léger pour l'été - Frais et confortable", "saison", 25),
    
    ("Collection Hivernale", "15000", "/static/images/Hiver-colléction.jpg",
     "Tissu épais - Parfait pour la saison fraîche", "saison", 20),

     ("Collection Eté ", "12000", "/static/images/collection-eté.jpg",
     "Tissu léger pour l'été - Frais et confortable", "saison", 25),
    
    ("Collection Hivernale", "15000", "/static/images/hiver-collection.jpg",
     "Tissu épais - Parfait pour la saison fraîche", "saison", 20),
]

for p in produits:
    cursor.execute("""
        INSERT INTO produits (nom, prix, image, description, categorie, stock)
        VALUES (?, ?, ?, ?, ?, ?)
    """, p)
    print(f"✓ {p[0]} ajouté avec image locale")

conn.commit()
conn.close()

print("\n✅ Base de données mise à jour avec images locales !")
print("📁 Dossier: static/images/")