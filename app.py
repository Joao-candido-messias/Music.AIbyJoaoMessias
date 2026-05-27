import streamlit as st
import google.generativeai as genai

# =========================================
# CONFIGURAÇÃO DA PÁGINA
# =========================================
st.set_page_config(
    page_title="MusicIA",
    page_icon="🎵",
    layout="centered"
)

st.markdown(
    """
    <style>

    /* Fundo geral */
    .stApp {
        background-color: #EEEEEE;
        color: #1F6F5F;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #6FCF97;
        color: #1F6F5F;
    }

    /* Títulos */
    h1, h2, h3, h4, h5, h6 {
        color: #1F6F5F !important;
    }

    /* Texto geral */
    p, span, label, div {
        color: #1F6F5F !important;
    }

    /* Inputs */
    textarea, input {
        background-color: #EEEEEE !important;
        color: #1F6F5F !important;
        border: 1px solid #2FA084 !important;
    }

    /* Placeholder */
    textarea::placeholder,
    input::placeholder {
        color: #4a8f80 !important;
        opacity: 1;
    }

    /* Botão principal */
    div.stButton > button {
        background-color: #2FA084;
        color: white;
        border-radius: 10px;
        border: none;
        padding: 0.6rem 1rem;
    }

    div.stButton > button:hover {
        background-color: #1F6F5F;
        color: white;
    }

    /* Componentes Streamlit */
    .stMarkdown, .stText, .stSelectbox, .stMultiSelect {
        color: #1F6F5F !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)
# =========================================
# CONFIGURAÇÃO DA API
# =========================================

genai.configure(api_key=st.secrets["general"]["api_key"])


# =========================================
# MODELO GEMINI
# =========================================
model = genai.GenerativeModel(
    "gemini-2.5-flash"
)

# =========================================
# INTERFACE PRINCIPAL
# =========================================
st.title("🎵 MusicIA: Sua Próxima Música")

st.markdown(
    """
    Descubra músicas baseadas no seu humor,
    estilo favorito e clima atual.
    """
)

# =========================================
# SIDEBAR
# =========================================
with st.sidebar:

    st.header("⚙️ Preferências")

    genero = st.multiselect(
        "🎼 Gêneros favoritos:",
        [
            "Jazz",
            "Pop",
            "Rock",
            "Funk",
            "MPB",
            "Rap",
            "Lo-fi",
            "Eletrônica",
            "Sertanejo",
            "Pagode"
        ]
    )

    tempo = st.slider(
        "⏱️ Duração máxima (minutos):",
        min_value=2,
        max_value=15,
        value=5
    )

    mood = st.text_area(
        "🧠 Como você está se sentindo?",
        placeholder=(
            "Ex: Quero uma música quente e marcante "
            "com harmonia rica e letra emocionante."
        )
    )

    botao_recomendar = st.button(
        "🎧 Buscar Recomendações"
    )

# =========================================
# LÓGICA PRINCIPAL
# =========================================
if botao_recomendar:

    if not mood:

        st.warning(
            "⚠️ Por favor, descreva o que deseja ouvir."
        )

    else:

        with st.spinner(
            "🎶 Procurando as melhores músicas..."
        ):

            # Caso usuário não escolha gênero
            generos_str = (
                ", ".join(genero)
                if genero
                else "qualquer gênero"
            )

            # Prompt enviado para IA
            prompt = f"""
            Você é um especialista em música.

            Recomende 5 músicas para alguém com as
            seguintes preferências:

            - Gêneros favoritos: {generos_str}
            - Duração máxima: {tempo} minutos
            - Clima desejado: {mood}

            Para cada música forneça:

            🎵 Nome da música
            🎤 Artista
            📅 Ano
            ⭐ Motivo da recomendação

            Seja criativo, organizado e objetivo.
            """

            try:

                # Resposta da IA
                response = model.generate_content(prompt)

                st.success(
                    "✅ Aqui estão suas recomendações musicais!"
                )

                st.markdown("---")

                # Exibe resposta formatada
                st.markdown(response.text)

            except Exception as e:

                st.error(
                    f"❌ Erro ao conectar com a IA:\n\n{e}"
                )


col1, col2 = st.columns(2)

with col1:
    if st.button("👍 Gostei"):
        with open("feedback.csv", "a", encoding="utf-8") as f:
            f.write(f"{mood},{genero},{tempo},Gostei\n")

        st.success("Obrigado pelo seu feedback positivo!")

with col2:
    if st.button("👎 Não gostei"):
        with open("feedback.csv", "a", encoding="utf-8") as f:
            f.write(f"{mood},{genero},{tempo},Não gostei\n")

        st.info("Feedback registrado. Vamos melhorar!")
# =========================================
# RODAPÉ
# =========================================
st.markdown("---")

st.caption(
    "Desenvolvido na disciplina Desenvolvimento "
    "Full Stack - Sistemas de Informação - UFN"
)