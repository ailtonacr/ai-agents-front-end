import streamlit as st
from typing import Optional
from model.user import User
from infrastructure.logging_config import logger


class UserSessionController:
    def logout_user(self) -> None:
        user = self.get_current_user()
        username = user.name if user else "unknown"
        logger.info(f"User logout: {username}")

        keys_to_clear = [
            "logged_in_user",
            "user_role",
            "current_session_db_id",
            "active_chat_messages",
            "user_id_for_adk",
        ]

        for key in keys_to_clear:
            st.session_state[key] = None

        st.session_state.current_view = "login"

    def navigate_to_admin_panel(self) -> None:
        st.session_state.current_view = "admin_panel"

    def navigate_to_main_app(self) -> None:
        st.session_state.current_view = "app"

    def get_current_user(self) -> Optional[User]:
        return st.session_state.get("logged_in_user")

    def is_admin(self) -> bool:
        user = self.get_current_user()
        is_admin = user and getattr(user, "role", None) == "admin"
        return is_admin
