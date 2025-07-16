import streamlit as st
from controller.user_session_controller import UserSessionController
from infrastructure.logging_config import logger


class UserMenuComponent:
    def __init__(self, user_session_controller: UserSessionController):
        self.controller = user_session_controller

    def render(self) -> None:
        _, col_menu = st.columns([10, 0.95])

        with col_menu:
            user = self.controller.get_current_user()
            if not user:
                return

            with st.popover(f"👤 {user.name}", use_container_width=False):
                st.markdown(f'Logado como: **{user.name}** ({getattr(user, "role", None)})')

                if self.controller.is_admin():
                    if st.button("Painel Admin", use_container_width=True, key=f"popover_admin_panel_{user.name}"):
                        self.controller.navigate_to_admin_panel()
                        st.rerun()

                if st.button("Logout", use_container_width=True, key=f"popover_logout_{user.name}"):
                    logger.info(f"User {user.name} logout via menu")
                    self.controller.logout_user()
                    st.success("Logout realizado com sucesso!")
                    st.rerun()
