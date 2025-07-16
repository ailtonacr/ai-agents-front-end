import streamlit as st
from infrastructure.user_dao import UserDAO
from infrastructure.logging_config import logger


class SessionManager:
    def __init__(self, user_dao: UserDAO):
        self.user_dao = user_dao

    def init_session_state(self) -> None:
        defaults = {
            "logged_in_user": None,
            "user_role": None,
            "current_view": "login",
            "available_agents": [],
            "selected_agent_for_new_chat": None,
            "current_session_db_id": None,
            "current_adk_session_id": None,
            "active_chat_agent_name": "Agente",
            "active_chat_messages": [],
            "chat_input_key_counter": 0,
            "show_agent_selector": False,
            "user_id_for_adk": None,
        }

        for key, value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = value

        user_count = self.user_dao.count_users()
        if user_count == 0 and st.session_state.current_view not in ["initial_setup", "register"]:
            logger.info("No users found in database, redirecting to initial setup")
            st.session_state.current_view = "initial_setup"
