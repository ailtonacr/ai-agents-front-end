import streamlit as st
from view.components.chat_components import ChatDisplayComponent, ChatHistoryComponent
from view.components.user_menu_component import UserMenuComponent
from controller.user_session_controller import UserSessionController
from infrastructure.session_dao import SessionDAO
from controller.chat_controller import ChatController
from model.message import Message
from infrastructure.logging_config import logger


def main_app_view(chat_controller: ChatController, session_dao: SessionDAO) -> None:
    user = st.session_state.get("logged_in_user")

    user_session_controller = UserSessionController()
    user_menu = UserMenuComponent(user_session_controller)
    user_menu.render()

    _render_sidebar(chat_controller, session_dao)

    _render_chat_area(chat_controller)


def _render_sidebar(chat_controller: ChatController, session_dao: SessionDAO) -> None:
    with st.sidebar:
        st.markdown(f"## 🧠 ADK Chat UI")
        st.markdown("---")

        if st.button("💬 Novo Chat", use_container_width=True, type="primary"):
            st.session_state.show_agent_selector = not st.session_state.show_agent_selector
            if not st.session_state.available_agents:
                st.session_state.available_agents = chat_controller.adk_client.get_available_agents()

        _render_agent_selector(chat_controller)

        chat_history = ChatHistoryComponent(session_dao)
        chat_history.render(st.session_state.logged_in_user, st.session_state.current_session_db_id)


def _render_agent_selector(chat_controller: ChatController) -> None:
    if not st.session_state.show_agent_selector:
        return

    if not st.session_state.available_agents:
        st.caption("Buscando agentes...")
        try:
            st.session_state.available_agents = chat_controller.adk_client.get_available_agents()
        except Exception as e:
            logger.error(f"Failed to fetch available agents: {str(e)}")
            st.error(f"Erro ao buscar agentes: {e}")
            return

    if st.session_state.available_agents:
        selected_agent = st.selectbox(
            "🤖 Escolha o Agente para o Novo Chat:",
            options=[""] + st.session_state.available_agents,
            index=0,
            key="new_chat_agent_selector_main_app",
        )
        if selected_agent:
            try:
                chat_controller.start_new_chat_session(selected_agent)
            except Exception as e:
                logger.error(f"Failed to start new chat with agent {selected_agent}: {str(e)}")
                st.error(f"Erro ao iniciar chat: {e}")
    else:
        st.warning("Nenhum agente disponível.")


def _render_chat_area(chat_controller: ChatController) -> None:
    if not st.session_state.current_session_db_id:
        st.info('👈 Selecione um chat existente ou clique em "💬 Novo Chat" na barra lateral para começar.')
        return

    if not st.session_state.active_chat_messages and st.session_state.current_session_db_id:
        try:
            chat_controller.load_chat_messages_from_db(st.session_state.current_session_db_id)
        except Exception as e:
            logger.error(f"Failed to load chat messages: {str(e)}")
            st.error(f"Erro ao carregar mensagens: {e}")
            return

    st.subheader(f"Chat com: {st.session_state.active_chat_agent_name}")
    st.markdown("---")

    chat_container = st.container()
    with chat_container:
        ChatDisplayComponent.render_messages(st.session_state.active_chat_messages)

    _handle_user_input(chat_controller, chat_container)


def _handle_user_input(chat_controller: ChatController, chat_container) -> None:
    user_input = st.chat_input("Digite sua mensagem...", key=f"chat_input_{st.session_state.chat_input_key_counter}")

    if not user_input:
        return

    user = st.session_state.get("logged_in_user")
    username = user.name if user else "unknown"
    agent_name = st.session_state.active_chat_agent_name

    logger.info(f"User {username} sending message to agent {agent_name}")

    try:
        new_msg = Message(role="user", text=user_input)
        st.session_state.active_chat_messages.append(new_msg)
        chat_controller.message_dao.add_message(st.session_state.current_session_db_id, new_msg)

        with chat_container:
            ChatDisplayComponent.render_message("user", user_input)

        with st.spinner(f"{st.session_state.active_chat_agent_name} está digitando..."):
            agent_responses = chat_controller.adk_client.send_message_to_adk(
                st.session_state.active_chat_agent_name,
                st.session_state.user_id_for_adk,
                st.session_state.current_adk_session_id,
                user_input,
            )

        for resp in agent_responses:
            agent_msg = Message(role=resp["role"], text=resp["text"])
            st.session_state.active_chat_messages.append(agent_msg)
            chat_controller.message_dao.add_message(st.session_state.current_session_db_id, agent_msg)

        st.rerun()

    except Exception as e:
        logger.error(f"Error handling user input for user {username}: {str(e)}")
        st.error(f"Erro ao enviar mensagem: {e}")
        if st.session_state.active_chat_messages and st.session_state.active_chat_messages[-1].role == "user":
            st.session_state.active_chat_messages.pop()
