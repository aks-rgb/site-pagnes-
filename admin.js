const form =
document.getElementById("form-produit");

const liste =
document.getElementById("liste-produits");

/* RECUPERATION PRODUITS */

let produits = JSON.parse(
    localStorage.getItem("produits")
) || [];

/* AFFICHAGE PRODUITS */

function afficherProduits(){

    liste.innerHTML = "";

    produits.forEach((produit) => {

        liste.innerHTML += `

        <div class="produit">

            <h3>
                ${produit.nom}
            </h3>

            <p>
                ${produit.prix}
            </p>

            <p>
                ${produit.description}
            </p>

            <img src="${produit.image}">

            <div class="actions">

                <button
                class="supprimer"
                onclick="supprimerProduit(${produit.id})">

                    Supprimer

                </button>

            </div>

        </div>

        `;

    });

}

/* AJOUT PRODUIT */

form.addEventListener("submit", (e) => {

    e.preventDefault();

    const produit = {

        id: Date.now(),

        nom:
        document.getElementById("nom").value,

        prix:
        document.getElementById("prix").value,

        image:
        document.getElementById("image").value,

        description:
        document.getElementById("description").value

    };

    produits.push(produit);

    localStorage.setItem(
        "produits",
        JSON.stringify(produits)
    );

    form.reset();

    afficherProduits();

});

/* SUPPRESSION */

function supprimerProduit(id){

    produits = produits.filter(
        (produit) => produit.id !== id
    );

    localStorage.setItem(
        "produits",
        JSON.stringify(produits)
    );

    afficherProduits();

}

/* CHARGEMENT */

afficherProduits();