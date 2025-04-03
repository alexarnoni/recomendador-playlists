
# 🎧 PlayMood – Recomendador Musical Inteligente

**PlayMood** é uma aplicação que entende o que você está sentindo e recomenda playlists do Spotify de forma inteligente. Basta digitar uma frase como “tô triste hoje” ou “acordei animado” que o sistema analisa o sentimento, busca playlists relevantes e te recomenda na hora.

---

## 🚀 Funcionalidades já implementadas

### 🔍 Análise de Sentimentos
- Utiliza o modelo `pysentimiento/robertuito-emotion`, com suporte robusto ao português.
- As frases são pré-processadas para remover ruídos (emojis, gírias, texto confuso).
- Frases curtas ou vazias são rejeitadas com mensagens amigáveis.

### 🎧 Recomendação de Playlists
- As playlists são buscadas diretamente na API do Spotify.
- Quando o sentimento for negativo (tristeza, raiva, medo), são retornadas duas playlists:
  - Uma para aliviar o sentimento.
  - Outra para manter ou explorar o sentimento.
- Quando positivo, retorna apenas uma playlist.

### 🧠 Sistema de Cache
- Evita recomendar a mesma playlist repetidamente para o mesmo sentimento.
- Expiração automática após 10 minutos.

### 📊 Painel Admin (/admin/painel)
- Gráfico em pizza com os sentimentos mais detectados.
- Exibe as últimas frases analisadas e playlists mais recomendadas.
- Botão para limpar o histórico com proteção por senha.

### 🔐 Sistema de Autenticação
- Apenas o primeiro usuário pode se registrar como administrador.
- Login protegido com cookies de sessão.
- Rota de registro bloqueada após primeiro cadastro.
- Logout real com remoção de sessão.

### 📜 Histórico
- Todas as recomendações são salvas em `historico_recomendacoes.json`.
- Entradas duplicadas consecutivas são evitadas automaticamente.
- Todos os campos são validados e salvos corretamente.

### 💡 Mensagens Inteligentes
- Geração de frases de resposta humoradas, como:
  - “Se quiser mudar o clima, algo leve 🎶”
  - “Vai com calma e escuta isso: músicas pra sair da fossa”

### 🧪 Logging
- Logs de ações importantes do sistema salvos em arquivo `.log`.
- Exemplo: histórico salvo, duplicata ignorada, login feito.

### 🌗 Modo Escuro
- Frontend com suporte a tema claro/escuro com toggle persistente.

### 🧼 Limpeza de Entrada
- Emojis, caracteres especiais e ruídos removidos antes da análise.

---

## 📁 Estrutura de Pastas (resumo)
```
backend/
├── main.py
├── api/
│   ├── rotas_publicas.py
│   └── rotas_admin.py
├── services/
│   ├── sentiment_analysis.py
│   ├── spotify_api.py
│   └── historico.py
├── utils/
│   ├── auth.py
│   ├── cache.py
│   ├── limpeza.py
│   ├── logger.py
│   └── hash.py
├── models/
│   └── usuario.py
├── config.py
```

---

## 🔮 Melhorias planejadas
- Aprendizado com uso (associar novas frases a sentimentos detectados).
- Tradução de gírias e expressões populares.
- Busca semântica com FAISS ou Weaviate (versão 2.0).
- Integração com LLM para explicar a recomendação.
- Sistema de logging com rotação e logs por módulo.

---

## 👨‍💻 Desenvolvido por
Alexandre Arnoni Nieri de Freitas  
[GitHub](https://github.com/alexarnoni) • [LinkedIn](https://www.linkedin.com/in/alexandrearnoni)

