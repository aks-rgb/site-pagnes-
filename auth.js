// auth.js - Version corrigée
const form = document.getElementById("login-form");

if (form) {
    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        
        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;
        
        // Afficher un message de chargement
        const button = form.querySelector("button");
        const originalText = button.textContent;
        button.textContent = "Connexion en cours...";
        button.disabled = true;
        
        try {
            console.log("Tentative de connexion avec:", email);
            
            const response = await fetch("/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ email, password })
            });
            
            const data = await response.json();
            console.log("Réponse:", data);
            
            if (response.ok) {
                localStorage.setItem("connected", "true");
                localStorage.setItem("user_email", email);
                localStorage.setItem("user_role", data.role);
                localStorage.setItem("user_name", data.nom);
                
                alert("Connexion réussie !");
                window.location.href = "/index";
            } else {
                alert(data.error || "Email ou mot de passe incorrect");
            }
        } catch (error) {
            console.error("Erreur:", error);
            alert("Erreur de connexion au serveur. Vérifiez que Flask est démarré.");
        } finally {
            button.textContent = originalText;
            button.disabled = false;
        }
    });
}

// Vérifier si déjà connecté
if (window.location.pathname === "/login-page" || window.location.pathname === "/login.html") {
    const connecte = localStorage.getItem("connected");
    if (connecte === "true") {
        window.location.href = "/index";
    }
}

// Fonction de déconnexion globale
window.logout = function() {
    fetch("/logout", { method: "POST" }).catch(e => console.log(e));
    localStorage.removeItem("connected");
    localStorage.removeItem("user_email");
    localStorage.removeItem("user_role");
    localStorage.removeItem("user_name");
    window.location.href = "/login-page";
};