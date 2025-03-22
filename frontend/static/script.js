async function getRecommendation() {
    let frase = document.getElementById("sentimento").value;
    let response = await fetch(`http://127.0.0.1:8000/api/recomendar?frase=${encodeURIComponent(frase)}`);
    let data = await response.json();

    let resultado = document.getElementById("resultado");
    resultado.innerHTML = `<p class="fade-in">${data.mensagem}</p>`;

    if (data.playlist_1) {
        resultado.innerHTML += renderizarPlaylist(data.playlist_1);
    }

    if (data.playlist_2) {
        resultado.innerHTML += renderizarPlaylist(data.playlist_2);
    }

    // Exibe o botão "Nova Recomendação"
    document.getElementById("nova-recomendacao").style.display = "block";
}

function renderizarPlaylist(playlist) {
    return `
    <div class="fade-in" style="margin: 20px;">
        <h3>${playlist.nome}</h3>
        ${playlist.imagem ? `<img src="${playlist.imagem}" alt="Capa da Playlist" style="width: 200px; border-radius: 10px;">` : ""}
        <br>
        <a href="${playlist.url}" target="_blank">
            <button style="margin-top: 10px; padding: 10px;">🎧 Ouvir Playlist</button>
        </a>
    </div>
`;
}

function selecionarSentimento(sentimento) {
    // Preenche o campo de texto com uma frase automática
    const input = document.getElementById("sentimento");
    input.value = `Estou sentindo ${sentimento}`;
    getRecommendation(); // Chama a recomendação direto
}

function alternarModo() {
    const body = document.body;
    const toggle = document.getElementById("modo-toggle");

    body.classList.toggle("dark-mode");
    body.classList.toggle("light-mode");

    const modoAtual = body.classList.contains("dark-mode") ? "dark" : "light";
    toggle.textContent = modoAtual === "dark" ? "☀️" : "🌙";

    // Salva no localStorage
    localStorage.setItem("modo-visual", modoAtual);
}

// Carrega o modo salvo
window.onload = function () {
    const modoSalvo = localStorage.getItem("modo-visual") || "light";
    document.body.classList.add(modoSalvo + "-mode");

    const toggle = document.getElementById("modo-toggle");
    if (toggle) {
        toggle.textContent = modoSalvo === "dark" ? "☀️" : "🌙";
    }
}

function resetarInterface() {
    document.getElementById("sentimento").value = "";
    document.getElementById("resultado").innerHTML = "";
    document.getElementById("nova-recomendacao").style.display = "none";
}

