import streamlit as st
from infrastructure.auth import AuthService
from model.email import Email
from infrastructure.logging_config import logger


def login_view(auth: AuthService, get_adk_user_id: callable) -> None:
    st.subheader("Login existentes")
    with st.form("login_form"):
        username = st.text_input("Usuário").lower()
        password = st.text_input("Senha", type="password")
        submitted = st.form_submit_button("Login")

        if submitted:
            logger.info(f"Login attempt for user: {username}")
            user = auth.authenticate_user(username, password)
            if user:
                logger.info(f"Login successful for user: {username}, role: {user.role}")
                st.session_state.logged_in_user = user
                st.session_state.user_role = getattr(user, "role", None)
                st.session_state.user_id_for_adk = get_adk_user_id(user.name)
                st.session_state.current_view = "app"
                st.session_state.current_session_db_id = None
                st.session_state.active_chat_messages = []
                st.rerun()
            else:
                logger.warning(f"Login failed for user: {username}")
                st.error("Usuário ou senha inválidos, ou usuário inativo.")

    if st.button("Não tem uma conta? Cadastre-se"):
        st.session_state.current_view = "register"
        st.rerun()


def registration_view(auth: AuthService, is_initial_setup: bool = False) -> None:
    st.subheader("Cadastro de Novo Usuário" if not is_initial_setup else "Cadastro do Primeiro Usuário (Admin)")
    with st.form("registration_form"):
        username = st.text_input("Usuário (letras minúsculas, sem espaços)").lower()
        email_input = st.text_input("Email (opcional)")
        password = st.text_input("Senha (mínimo 6 caracteres)", type="password")
        confirm_password = st.text_input("Confirme a Senha", type="password")
        submitted = st.form_submit_button("Cadastrar")

        if submitted:
            logger.info(f"Registration attempt for user: {username}")
            if password != confirm_password:
                logger.warning(f"Registration failed for {username}: password mismatch")
                st.error("As senhas não coincidem.")
            else:
                try:
                    email = Email(email_input)
                    success, message = auth.register_user(username, password, email)
                    if success:
                        logger.info(f"Registration successful for user: {username}")
                        st.success(message)
                        st.session_state.current_view = "login"
                        st.rerun()
                    else:
                        logger.warning(f"Registration failed for {username}: {message}")
                        st.error(message)
                except Exception as e:
                    logger.error(f"Registration error for {username}: {str(e)}")
                    st.error(str(e))

    if not is_initial_setup:
        if st.button("Já tem uma conta? Faça Login"):
            st.session_state.current_view = "login"
            st.rerun()
