import streamlit as st
from infrastructure.app_factory import AppFactory
from view.admin_views import admin_panel_view
from view.auth_views import login_view, registration_view
from view.main_app_view import main_app_view
from infrastructure.logging_config import logger


class AppRouter:
    def __init__(self, app_factory: AppFactory):
        self.app_factory = app_factory

    def route(self) -> None:
        current_view = st.session_state.current_view

        if current_view == "initial_setup":
            self._show_initial_setup()
        elif current_view == "login":
            self._show_login()
        elif current_view == "register":
            self._show_register()
        elif current_view == "app" and st.session_state.logged_in_user:
            self._show_main_app()
        elif current_view == "admin_panel" and st.session_state.user_role == "admin":
            self._show_admin_panel()
        else:
            logger.warning(f"Invalid view state: {current_view}, redirecting to login")
            self._redirect_to_login()

    def _show_initial_setup(self) -> None:
        registration_view(self.app_factory.auth_service, is_initial_setup=True)

    def _show_login(self) -> None:
        login_view(self.app_factory.auth_service, self.app_factory.get_adk_user_id)

    def _show_register(self) -> None:
        registration_view(self.app_factory.auth_service)

    def _show_main_app(self) -> None:
        main_app_view(self.app_factory.chat_controller, self.app_factory.session_dao)

    def _show_admin_panel(self) -> None:
        admin_panel_view(self.app_factory.user_dao)

    def _redirect_to_login(self) -> None:
        st.session_state.current_view = "login"
        st.rerun()
