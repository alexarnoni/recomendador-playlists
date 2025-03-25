async function getRecommendation() {
    let frase = document.getElementById("sentimento")?.value;
    let resultado = document.getElementById("resultado");

    if (!frase || !resultado) return;

    try {
        let response = await fetch(`http://127.0.0.1:8000/api/recomendar?frase=${encodeURIComponent(frase)}`);

        if (!response.ok) {
            let erro = await response.json();
            resultado.innerHTML = `<p class="erro fade-in">${erro.erro}</p>`;
            document.getElementById("nova-recomendacao").style.display = "none";
            return;
        }

        let data = await response.json();

        resultado.innerHTML = `<p class="fade-in">${data.mensagem}</p>`;

        if (data.playlist_1) {
            resultado.innerHTML += renderizarPlaylist(data.playlist_1);
        }

        if (data.playlist_2) {
            resultado.innerHTML += renderizarPlaylist(data.playlist_2);
        }

        document.getElementById("nova-recomendacao").style.display = "block";

    } catch (err) {
        resultado.innerHTML = `<p class="erro fade-in">Erro ao conectar com a API.</p>`;
        console.error(err);
    }
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
    const input = document.getElementById("sentimento");
    if (!input) return;

    input.value = `Estou sentindo ${sentimento}`;
    getRecommendation();
}

function alternarModo() {
    const body = document.body;
    const toggle = document.getElementById("modo-toggle");

    body.classList.toggle("dark-mode");
    body.classList.toggle("light-mode");

    const modoAtual = body.classList.contains("dark-mode") ? "dark" : "light";
    if (toggle) {
        toggle.textContent = modoAtual === "dark" ? "☀️" : "🌙";
    }

    localStorage.setItem("modo-visual", modoAtual);
}

window.onload = function () {
    const modoSalvo = localStorage.getItem("modo-visual") || "light";
    document.body.classList.add(`${modoSalvo}-mode`);

    const toggle = document.getElementById("modo-toggle");
    if (toggle) {
        toggle.textContent = modoSalvo === "dark" ? "☀️" : "🌙";
    }
}

function resetarInterface() {
    const input = document.getElementById("sentimento");
    const resultado = document.getElementById("resultado");
    const novaRecomendacao = document.getElementById("nova-recomendacao");

    if (input) input.value = "";
    if (resultado) resultado.innerHTML = "";
    if (novaRecomendacao) novaRecomendacao.style.display = "none";
}