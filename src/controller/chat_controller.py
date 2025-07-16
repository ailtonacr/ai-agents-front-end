import datetime
import streamlit as st
from model.message import Message
from model.chat_session import ChatSession
from infrastructure.adk_client import ADKClient
from infrastructure.session_dao import SessionDAO
from infrastructure.message_dao import MessageDAO
from infrastructure.logging_config import logger


class ChatController:
    def __init__(
        self, adk_client: ADKClient, session_dao: SessionDAO, message_dao: MessageDAO, get_adk_user_id: callable
    ):
        self.adk_client = adk_client
        self.session_dao = session_dao
        self.message_dao = message_dao
        self.get_adk_user_id = get_adk_user_id

    def start_new_chat_session(self, agent_name: str):
        logger.info(f"Starting new chat session with agent: {agent_name}")

        if not st.session_state.logged_in_user:
            logger.warning("Attempt to start chat session without logged in user")
            st.error("Usuário não logado.")
            return
        if not agent_name:
            logger.warning("Attempt to start chat session without selecting an agent")
            st.error("Selecione um agente.")
            return

        user = st.session_state.logged_in_user

        adk_session_id = self.adk_client.create_adk_session(agent_name, st.session_state.user_id_for_adk)
        if adk_session_id:
            chat_session = ChatSession(
                db_id=None,
                adk_session_id=adk_session_id,
                user_name=user.name,
                agent_name=agent_name,
                created_at=datetime.datetime.now(),
                summary=f"{agent_name} Chat com {user.name}",
            )
            session_db_id = self.session_dao.create_chat_session_from_object(chat_session)

            st.session_state.current_session_db_id = session_db_id
            st.session_state.current_adk_session_id = adk_session_id
            st.session_state.active_chat_agent_name = agent_name
            st.session_state.active_chat_messages = []
            st.session_state.chat_input_key_counter += 1
            st.session_state.show_agent_selector = False

            logger.info(f"Chat session started successfully for user {user.name} with agent {agent_name}")
            st.success(f"Nova sessão com {agent_name} iniciada!")
            st.rerun()
        else:
            logger.error(f"Failed to create ADK session for agent: {agent_name}")
            st.error("Falha ao criar sessão com o ADK.")

    def load_chat_messages_from_db(self, session_db_id: str):
        messages_db = self.message_dao.get_messages_for_session(session_db_id)

        st.session_state.active_chat_messages = messages_db
        session_details = self.session_dao.get_session_details(session_db_id)
        if session_details:
            st.session_state.current_session_db_id = session_db_id
            st.session_state.current_adk_session_id = session_details.adk_session_id
            st.session_state.active_chat_agent_name = session_details.agent_name
            st.session_state.user_id_for_adk = self.get_adk_user_id(session_details.user_name)
        else:
            logger.warning(f"No session details found for session: {session_db_id}")
