import streamlit as st
from openai import OpenAI

# Configuração da página
st.set_page_config(page_title="Mordomo Victor", page_icon="🤵", layout="centered")
st.title("🤵 Mordomo Victor")

# Barra lateral com as configurações
with st.sidebar:
    st.header("⚙️ Configurações do Mordomo")
    
    # Prompt do Sistema (já preenchido com a personalidade do Mordomo)
    system_prompt = st.text_area(
        "Prompt de Sistema (Personalidade)",
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
        height=300
    )
    
    temperature = st.slider("Temperatura (Criatividade)", 0.0, 1.0, 0.3, 0.1)
    max_tokens = st.slider("Máximo de Tokens (Tamanho da resposta)", 100, 4096, 1024, 100)

# Inicializa o cliente da OpenRouter
# A chave será lida dos "Secrets" do Streamlit, não do código
if "OPENROUTER_API_KEY" not in st.secrets:
    st.error("Por favor, adicione a chave OPENROUTER_API_KEY nas configurações (Secrets) do Streamlit.")
    st.stop()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=st.secrets["OPENROUTER_API_KEY"],
)

# Inicializa o histórico de mensagens
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibe as mensagens anteriores
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Campo de entrada do usuário
if prompt := st.chat_input("Como posso ajudar, Senhor Victor?"):
    # Adiciona a mensagem do usuário ao histórico
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Prepara as mensagens para a API (incluindo o prompt de sistema)
    api_messages = [{"role": "system", "content": system_prompt}] + st.session_state.messages

    # Gera a resposta
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
           model="openrouter/free",
            messages=api_messages,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=True,
        )
        response = st.write_stream(stream)
    
    # Adiciona a resposta do Mordomo ao histórico
    st.session_state.messages.append({"role": "assistant", "content": response})