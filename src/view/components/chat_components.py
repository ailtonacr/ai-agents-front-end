import streamlit as st
import html
from typing import List
from infrastructure.session_dao import SessionDAO
from model.user import User
from model.message import Message


class ChatDisplayComponent:
    @staticmethod
    def render_message(role: str, text: str, is_typing_placeholder: bool = False) -> None:
        align_class = "user-message" if role == "user" else "agent-message"
        if is_typing_placeholder:
            align_class = "typing-indicator"

        safe_text = html.escape(text)
        st.markdown(
            f"""<div class="chat-message-container {align_class}">
                <div class="chat-bubble">{safe_text}</div>
            </div>""",
            unsafe_allow_html=True,
        )

    @staticmethod
    def render_messages(messages: List[Message]) -> None:
        if not messages:
            return

        for msg in messages:
            ChatDisplayComponent.render_message(msg.role, msg.text)


class ChatHistoryComponent:
    def __init__(self, session_dao: SessionDAO):
        self.session_dao = session_dao

    def render(self, user: User, current_session_db_id: str = None) -> None:
        st.sidebar.markdown("---")
        st.sidebar.markdown('<h2 class="sidebar-section-header">Histórico de Chats</h2>', unsafe_allow_html=True)

        if not user:
            st.sidebar.warning("Usuário não identificado para carregar histórico.")
            return

        try:
            sessions = self.session_dao.get_sessions_for_user(user)
        except Exception as e:
            st.sidebar.error(f"Erro ao carregar histórico: {e}")
            return

        if not sessions:
            st.sidebar.caption("Nenhum chat encontrado.")
            return

        for session in sessions:
            self._render_session_button(session, current_session_db_id)

    def _render_session_button(self, session, current_session_db_id: str) -> None:
        session_id_db = session.db_id
        summary = session.summary if session.summary else f"Chat com {session.agent_name}"
        summary_display = summary[:30] + "..." if len(summary) > 30 else summary

        button_key = f"session_select_{session_id_db}"
        is_selected = session_id_db == current_session_db_id
        button_label = f"▶  {summary_display}" if is_selected else summary_display

        if st.sidebar.button(
            button_label,
            key=button_key,
            help=f"Agente: {session.agent_name}\nCriado em: {session.created_at}",
            use_container_width=True,
        ):
            self._handle_session_selection(session_id_db)

    def _handle_session_selection(self, session_id_db: str) -> None:
        if st.session_state.current_session_db_id != session_id_db:
            st.session_state.current_session_db_id = session_id_db
            st.session_state.active_chat_messages = []

            try:
                session_details = self.session_dao.get_session_details(session_id_db)
                if session_details:
                    st.session_state.current_adk_session_id = session_details.adk_session_id
                    st.session_state.active_chat_agent_name = session_details.agent_name
                else:
                    st.sidebar.error("Erro ao carregar detalhes da sessão.")
                    return
            except Exception as e:
                st.sidebar.error(f"Erro ao carregar sessão: {e}")
                return

        st.rerun()
