
import streamlit as st
from openai import OpenAI
from datetime import datetime

# ─────────────────────────────────────────────────────────────
# CONFIGURAÇÃO DA PÁGINA
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Mordomo Victor",
    page_icon="🤵",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────
# ESTILO VISUAL (tema "mordomo" — escuro, elegante, dourado)
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Inter:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

h1 {
    font-family: 'Playfair Display', serif !important;
    color: #D4AF37 !important;
    text-align: center;
    padding-bottom: 0 !important;
}

.subtitle {
    text-align: center;
    color: #9AA0A6;
    font-size: 0.95rem;
    margin-top: -12px;
    margin-bottom: 1.6rem;
}

section[data-testid="stSidebar"] {
    background-color: #14161c;
    border-right: 1px solid #2a2d35;
}

section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] .stMarkdown p strong {
    font-family: 'Playfair Display', serif;
    color: #D4AF37 !important;
}

[data-testid="stChatMessage"] {
    background-color: #1A1D24;
    border-radius: 14px;
    padding: 6px 10px;
    margin-bottom: 8px;
    border: 1px solid #2a2d35;
}

.stButton button, .stDownloadButton button {
    border-radius: 8px !important;
    border: 1px solid #D4AF37 !important;
    color: #D4AF37 !important;
    background-color: transparent !important;
}

.stButton button:hover, .stDownloadButton button:hover {
    background-color: #D4AF37 !important;
    color: #0E1117 !important;
}

.msg-time {
    font-size: 0.7rem;
    color: #6b6f76;
    margin: -8px 0 6px 4px;
}

footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


def saudacao_do_momento() -> str:
    hora = datetime.now().hour
    if hora < 12:
        return "Bom dia"
    if hora < 18:
        return "Boa tarde"
    return "Boa noite"


def agora() -> str:
    return datetime.now().strftime("%H:%M")


# ─────────────────────────────────────────────────────────────
# ACESSO OPCIONAL POR SENHA
# Se você definir APP_PASSWORD nos Secrets do Streamlit, o app passa
# a pedir senha antes de liberar o chat — importante se o link for
# público, para que estranhos não consumam sua cota da API.
# Se o segredo não existir, esta etapa é ignorada normalmente.
# ─────────────────────────────────────────────────────────────
def acesso_liberado() -> bool:
    if "APP_PASSWORD" not in st.secrets:
        return True
    if st.session_state.get("autenticado", False):
        return True

    st.markdown("<h1>🤵 Mordomo Victor</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Acesso restrito — identifique-se, por favor</p>", unsafe_allow_html=True)
    senha = st.text_input("Senha de acesso", type="password", label_visibility="collapsed", placeholder="Senha de acesso")
    if st.button("Entrar", use_container_width=True):
        if senha == st.secrets["APP_PASSWORD"]:
            st.session_state.autenticado = True
            st.rerun()
        else:
            st.error("Senha incorreta, Senhor Victor.")
    return False


if not acesso_liberado():
    st.stop()

# ─────────────────────────────────────────────────────────────
# CABEÇALHO
# ─────────────────────────────────────────────────────────────
st.markdown("<h1>🤵 Mordomo Victor</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Seu assistente pessoal, sempre à disposição</p>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# BARRA LATERAL
# ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Configurações do Mordomo")

    with st.expander("🎭 Personalidade (Prompt de Sistema)", expanded=False):
        system_prompt = st.text_area(
            "Prompt de Sistema",
            value="""[IDENTIDADE E PERSONALIDADE]
Você é um Mordomo Digital. Sua postura é de extrema calma, paciência, responsabilidade e lealdade. Você é prestativo, formal e analítico, mas com uma cordialidade calorosa e encorajadora. Você serve ao seu mestre com dedicação absoluta, agindo como um mentor sábio e um assistente confiável.

[PERFIL DO SEU MESTRE]
Seu mestre se chama Victor. Ele tem 18 anos, está estudando para cursar Psicologia e tem TEA (Transtorno do Espectro Autista). Victor é uma pessoa altamente curiosa e tem grande interesse em projetos de eletrônica. Ele valoriza a lógica, a clareza e a precisão.

[DIRETRIZES DE COMUNICAÇÃO]
1. Trate-o sempre como "Victor" ou "Senhor Victor", mantendo o respeito e a formalidade de um mordomo.
2. Sua linguagem deve ser clara, objetiva e estruturada. Evite ambiguidades, sarcasmo ou ironia.
3. Quando confrontado com uma tarefa complexa, divida-a em passos lógicos e sequenciais.
4. Seja paciente. Se Victor não entender algo, reformule a explicação de uma maneira diferente.
5. Mantenha um tom encorajador. Reconheça o esforço dele e celebre suas conquistas.

[REGRA DE OURO: O USO DE ANALOGIAS]
Para facilitar o entendimento de Victor, você deve SEMPRE usar analogias práticas e visuais com eletrônica e psicologia.""",
            height=280,
            label_visibility="collapsed",
        )

    with st.expander("🧠 Modelo e Parâmetros", expanded=False):
        modelos = {
            "Automático (openrouter/free)": "openrouter/free",
            "DeepSeek R1 (free)": "deepseek/deepseek-r1:free",
            "Llama 3.1 70B (free)": "meta-llama/llama-3.1-70b-instruct:free",
            "Llama 3.1 8B (free)": "meta-llama/llama-3.1-8b-instruct:free",
            "Personalizado…": "custom",
        }
        escolha = st.selectbox("Modelo", list(modelos.keys()))
        if modelos[escolha] == "custom":
            model_id = st.text_input("ID do modelo no OpenRouter", value="openrouter/free")
        else:
            model_id = modelos[escolha]

        temperature = st.slider("Temperatura (Criatividade)", 0.0, 1.0, 0.3, 0.1)
        max_tokens = st.slider("Máximo de Tokens (Tamanho da resposta)", 100, 4096, 1024, 100)

    with st.expander("📎 Contexto adicional (opcional)", expanded=False):
        arquivo = st.file_uploader("Anexar um .txt ou .md para o Mordomo consultar", type=["txt", "md"])
        contexto_extra = arquivo.read().decode("utf-8", errors="ignore") if arquivo else None
        if contexto_extra:
            st.caption(f"✅ {len(contexto_extra)} caracteres carregados de '{arquivo.name}'")

    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        limpar = st.button("🗑️ Limpar", use_container_width=True)
    with col2:
        transcricao = "\n\n".join(
            f"[{m.get('time', '')}] {'Victor' if m['role'] == 'user' else 'Mordomo'}: {m['content']}"
            for m in st.session_state.get("messages", [])
        )
        st.download_button(
            "💾 Exportar",
            data=transcricao if transcricao else "Nenhuma mensagem ainda.",
            file_name=f"conversa_mordomo_victor_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
            use_container_width=True,
        )

    st.caption(f"💬 {len(st.session_state.get('messages', []))} mensagens nesta conversa")

# ─────────────────────────────────────────────────────────────
# CLIENTE OPENROUTER
# ─────────────────────────────────────────────────────────────
if "OPENROUTER_API_KEY" not in st.secrets:
    st.error("Por favor, adicione a chave OPENROUTER_API_KEY nas configurações (Secrets) do Streamlit.")
    st.stop()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=st.secrets["OPENROUTER_API_KEY"],
)

# ─────────────────────────────────────────────────────────────
# HISTÓRICO DE MENSAGENS
# ─────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": f"{saudacao_do_momento()}, Senhor Victor. Em que posso ser útil?",
            "time": agora(),
        }
    ]

if limpar:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": f"{saudacao_do_momento()}, Senhor Victor. Em que posso ser útil?",
            "time": agora(),
        }
    ]
    st.rerun()

# Exibe as mensagens anteriores
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="🤵" if message["role"] == "assistant" else "🧑"):
        st.markdown(message["content"])
        if message.get("time"):
            st.markdown(f"<div class='msg-time'>{message['time']}</div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# ENTRADA DO USUÁRIO
# ─────────────────────────────────────────────────────────────
if prompt := st.chat_input("Como posso ajudar, Senhor Victor?"):
    st.session_state.messages.append({"role": "user", "content": prompt, "time": agora()})
    with st.chat_message("user", avatar="🧑"):
        st.markdown(prompt)
        st.markdown(f"<div class='msg-time'>{agora()}</div>", unsafe_allow_html=True)

    system_final = system_prompt
    if contexto_extra:
        system_final += f"\n\n[CONTEXTO ADICIONAL FORNECIDO POR VICTOR]\n{contexto_extra}"

    api_messages = [{"role": "system", "content": system_final}] + [
        {"role": m["role"], "content": m["content"]} for m in st.session_state.messages
    ]

    with st.chat_message("assistant", avatar="🤵"):
        try:
            stream = client.chat.completions.create(
                model=model_id,
                messages=api_messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=True,
            )
            response = st.write_stream(stream)
            st.markdown(f"<div class='msg-time'>{agora()}</div>", unsafe_allow_html=True)
            st.session_state.messages.append({"role": "assistant", "content": response, "time": agora()})
        except Exception as e:
            st.error(f"⚠️ Peço desculpas, Senhor Victor. Encontrei um imprevisto ao consultar o modelo: {e}")
