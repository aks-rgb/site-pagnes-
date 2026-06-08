const galerie = document.querySelector(".galerie");

let produits = JSON.parse(
    localStorage.getItem("produits")
) || [];

/* PRODUITS PAR DEFAUT */

if(produits.length === 0){

    produits = [

        {
            id: 1,

            nom: "Wax Prestige",

            prix: "15 000 FCFA",

            image: "images/pagne1.jpg",

            description:
            "Pagne moderne haut de gamme"
        },

        {
            id: 2,

            nom: "Bazin Royal",

            prix: "20 000 FCFA",

            image: "images/pagne2.jpg",

            description:
            "Collection élégante africaine"
        },

        {
            id: 3,

            nom: "Ankara Fashion",

            prix: "18 000 FCFA",

            image: "images/pagne3.jpg",

            description:
            "Style moderne et tendance"
        }

    ];

    localStorage.setItem(
        "produits",
        JSON.stringify(produits)
    );
}

/* AFFICHAGE PRODUITS */

function afficherProduits(listeProduits){

    galerie.innerHTML = "";

    listeProduits.forEach((produit) => {

        galerie.innerHTML += `

        <div class="carte">

            <img src="${produit.image}">

            <div class="carte-content">

                <h3>
                    ${produit.nom}
                </h3>

                <p>
                    ${produit.prix}
                </p>

                <p>
                    ${produit.description}
                </p>

                <button
                class="commander-btn"
                onclick="commanderProduit('${produit.nom}')">

                    Commander

                </button>

            </div>

        </div>

        `;

    });

}

/* WHATSAPP */

function commanderProduit(nomProduit){

    const numero = "22892984983";

    const message =
`Bonjour, je suis intéressé par le produit : ${nomProduit}`;

    const url =
`https://wa.me/${numero}?text=${encodeURIComponent(message)}`;

    window.open(url, "_blank");
}

/* RECHERCHE */

const recherche =
document.getElementById("recherche");

recherche.addEventListener("keyup", () => {

    const valeur =
    recherche.value.toLowerCase();

    const filtres = produits.filter(
        (produit) =>

        produit.nom
        .toLowerCase()
        .includes(valeur)
    );

    afficherProduits(filtres);

});

/* CHARGEMENT */

afficherProduits(produits);