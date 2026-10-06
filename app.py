import streamlit as st
from ollama import chat


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AI Project Mentor",
    page_icon="🤖",
    layout="wide"
)


# =========================================================
# SESSION STATE
# =========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "history" not in st.session_state:
    st.session_state.history = []

if "current_title" not in st.session_state:
    st.session_state.current_title = None


# =========================================================
# SAVE CURRENT CHAT TO HISTORY
# =========================================================

def save_current_chat():

    if not st.session_state.messages:
        return

    # Get only user messages
    user_messages = [
        msg["content"]
        for msg in st.session_state.messages
        if msg["role"] == "user"
    ]

    if not user_messages:
        return

    # First user message = chat title
    title = user_messages[0].strip()

    # Short title
    if len(title) > 35:
        title = title[:35] + "..."

    # Check duplicate title
    existing_titles = [
        item["title"]
        for item in st.session_state.history
    ]

    if title not in existing_titles:

        st.session_state.history.append({
            "title": title,
            "messages": st.session_state.messages.copy()
        })


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.title("🤖 AI Project Mentor")

    st.divider()


    # =====================================================
    # NEW CHAT
    # =====================================================

    if st.button(
        "➕ New Chat",
        use_container_width=True
    ):

        # Save current chat before starting new chat
        save_current_chat()

        # Clear current messages
        st.session_state.messages = []

        st.session_state.current_title = None

        st.rerun()


    # =====================================================
    # CLEAR CURRENT CHAT
    # =====================================================

    if st.button(
        "🗑️ Clear Chat",
        use_container_width=True
    ):

        # Only current chat will be deleted
        st.session_state.messages = []

        st.session_state.current_title = None

        st.rerun()


    # =====================================================
    # CLEAR ALL HISTORY
    # =====================================================

    if st.button(
        "🧹 Clear History",
        use_container_width=True
    ):

        # Delete all saved history
        st.session_state.history = []

        # Also clear current chat
        st.session_state.messages = []

        st.session_state.current_title = None

        st.rerun()


    st.divider()


    # =====================================================
    # HISTORY
    # =====================================================

    st.subheader("📜 History")


    if st.session_state.history:

        # Show latest chat first
        for i, item in enumerate(
            reversed(st.session_state.history)
        ):

            if st.button(
                f"💬 {item['title']}",
                key=f"history_{i}",
                use_container_width=True
            ):

                # Open selected old chat
                st.session_state.messages = (
                    item["messages"].copy()
                )

                st.session_state.current_title = (
                    item["title"]
                )

                st.rerun()

    else:

        st.info("No chat history yet.")


# =========================================================
# MAIN PAGE
# =========================================================

st.title("🤖 AI-Powered Mini Project Mentor")

st.caption(
    "From idea to implementation — "
    "your AI-powered project mentor. 🚀"
)

st.divider()


# =========================================================
# WELCOME MESSAGE
# =========================================================

if not st.session_state.messages:

    st.markdown("""
    ### 👋 Hello!

    I'm your **AI Project Mentor**.

    I can help you with:

    - 💡 Project ideas
    - 🛠️ Technologies
    - 🧩 Project modules
    - 🗄️ Database design
    - 📋 Development steps
    - 🤖 AI integration
    - 🎯 Project improvements
    - ❓ Viva questions

    **Tell me about your project to get started!**
    """)


# =========================================================
# DISPLAY PREVIOUS MESSAGES
# =========================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# =========================================================
# CHAT INPUT
# =========================================================

user_input = st.chat_input(
    "💬 Ask your project mentor..."
)


# =========================================================
# PROCESS USER MESSAGE
# =========================================================

if user_input:

    # -----------------------------------------------------
    # ADD USER MESSAGE
    # -----------------------------------------------------

    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })


    # -----------------------------------------------------
    # DISPLAY USER MESSAGE
    # -----------------------------------------------------

    with st.chat_message("user"):

        st.markdown(user_input)


    # -----------------------------------------------------
    # AI RESPONSE
    # -----------------------------------------------------

    with st.chat_message("assistant"):

        with st.spinner(
            "🧠 AI Mentor is thinking..."
        ):

            try:

                # System prompt
                system_message = {
                    "role": "system",
                    "content": """
You are an AI Project Mentor for B.Tech CSE students.

Help students develop their projects step-by-step.

Give simple and beginner-friendly explanations.

Help with:

- Project ideas
- Project titles
- Technologies
- Architecture
- Modules
- Database design
- Development steps
- AI integration
- Testing
- Deployment
- Future enhancements
- Viva questions

Remember the previous conversation and
continue the discussion naturally.

Do not repeat the complete previous answer
unless the student asks for it.
"""
                }


                # -------------------------------------------------
                # SEND CONVERSATION TO OLLAMA
                # -------------------------------------------------

                response = chat(

                    model="llama3.2",

                    messages=[
                        system_message,
                        *st.session_state.messages
                    ]
                )


                # -------------------------------------------------
                # GET AI ANSWER
                # -------------------------------------------------

                answer = response.message.content


                # -------------------------------------------------
                # DISPLAY AI ANSWER
                # -------------------------------------------------

                st.markdown(answer)


                # -------------------------------------------------
                # SAVE AI ANSWER IN CURRENT CHAT
                # -------------------------------------------------

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })


            except Exception as e:

                st.error(
                    f"❌ Ollama Error: {e}"
                )