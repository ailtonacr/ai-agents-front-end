import streamlit as st
from controller.admin_controller import AdminController
from controller.user_session_controller import UserSessionController
from infrastructure.user_dao import UserDAO
from infrastructure.logging_config import logger


def admin_panel_view(user_dao: UserDAO) -> None:
    current_user = st.session_state.get("logged_in_user")
    admin_name = current_user.name if current_user else "unknown"
    logger.info(f"Admin panel accessed by user: {admin_name}")

    admin_controller = AdminController(user_dao)
    user_session_controller = UserSessionController()

    st.title("👑 Painel de Administração")
    if st.button("← Voltar para o Chat"):
        user_session_controller.navigate_to_main_app()
        st.rerun()

    st.subheader("Gerenciar Usuários")
    try:
        users = admin_controller.get_all_users()
    except Exception as e:
        logger.error(f"Failed to fetch users for admin {admin_name}: {str(e)}")
        st.error("Erro ao carregar lista de usuários")
        return

    if not users:
        st.info("Nenhum usuário encontrado (além de você, se for o único).")
        return

    user_data_for_editor = admin_controller.format_users_for_display(users)
    st.data_editor(
        user_data_for_editor,
        disabled=["Usuário", "Email", "Role", "Ativo"],
        num_rows="dynamic",
        key="admin_user_editor",
    )

    st.caption(
        "Para alterar Role ou status Ativo, modifique na tabela e use os botões abaixo para confirmar ações mais complexas."
    )

    _render_user_actions_section(admin_controller, users, user_session_controller)


def _render_user_actions_section(
    admin_controller: AdminController, users, user_session_controller: UserSessionController
) -> None:
    st.subheader("Ações nos Usuários")
    selected_username = st.selectbox("Selecione o usuário para Ações:", options=[u.name for u in users])

    if not selected_username:
        return

    selected_user = admin_controller.find_user_by_name(users, selected_username)
    if not selected_user:
        st.error("Usuário selecionado não encontrado.")
        return

    st.subheader(f"Editando: {selected_user.name}")

    user_form_data = _render_user_edit_form(selected_user)

    _render_action_buttons(admin_controller, selected_user, user_form_data, user_session_controller)


def _render_user_edit_form(selected_user) -> dict:
    col1, col2 = st.columns(2)

    with col1:
        username = st.text_input("Nome de Usuário", value=selected_user.name, key="username_input")
        email_input = st.text_input("Email", value=selected_user.email, key="email_input")
        new_password = st.text_input("Nova Senha", key="new_password", type="password")

    with col2:
        role = st.selectbox(
            "Role",
            ["user", "admin"],
            index=["user", "admin"].index(selected_user.role),
            key="role_select",
        )
        is_active_str = st.selectbox(
            "Usuário Ativo",
            options=["Ativo", "Inativo"],
            index=0 if selected_user.is_active else 1,
            key="active_toggle",
        )
        is_active = is_active_str == "Ativo"
        confirm_password = st.text_input("Confirme sua nova Senha", key="confirm_new_password", type="password")

    st.divider()

    return {
        "username": username,
        "email": email_input,
        "password": new_password,
        "confirm_password": confirm_password,
        "role": role,
        "is_active": is_active,
    }


def _render_action_buttons(
    admin_controller: AdminController, selected_user, form_data: dict, user_session_controller: UserSessionController
) -> None:
    action_col1, action_col2, _ = st.columns([1, 1, 2])

    if action_col1.button("✓ Salvar Alterações", type="primary", use_container_width=True):
        st.session_state.confirm_action = "update"

    if action_col2.button("🗑️ Deletar Usuário", type="secondary", use_container_width=True):
        st.session_state.confirm_action = "delete"

    if st.session_state.get("confirm_action") == "update":
        _handle_update_confirmation(admin_controller, selected_user, form_data, user_session_controller)

    if st.session_state.get("confirm_action") == "delete":
        _handle_delete_confirmation(admin_controller, selected_user, user_session_controller)


def _handle_update_confirmation(
    admin_controller: AdminController, selected_user, form_data: dict, user_session_controller: UserSessionController
) -> None:
    st.warning(f"**Tem certeza que deseja SALVAR as alterações para o usuário {selected_user.name}?**")

    confirm_col1, confirm_col2, _ = st.columns([1, 1, 2])

    if confirm_col1.button("Sim, salvar", key="confirm_update_yes"):
        current_user = user_session_controller.get_current_user()
        current_username = current_user.name if current_user else None

        is_valid, error_msg = admin_controller.validate_user_update(
            selected_user,
            current_username,
            form_data["password"],
            form_data["confirm_password"],
            form_data["role"],
            form_data["is_active"],
        )

        if not is_valid:
            st.error(error_msg)
        else:
            success, message = admin_controller.update_user(
                selected_user, form_data["email"], form_data["password"], form_data["role"], form_data["is_active"]
            )

            if success:
                st.success(message)
                del st.session_state.confirm_action
                st.rerun()
            else:
                st.error(message)

    if confirm_col2.button("Não, cancelar", key="confirm_update_no"):
        del st.session_state.confirm_action
        st.rerun()


def _handle_delete_confirmation(
    admin_controller: AdminController, selected_user, user_session_controller: UserSessionController
) -> None:
    st.warning(f"**Tem certeza que deseja DELETAR o usuário {selected_user.name}? Esta ação é irreversível.**")

    confirm_col1, confirm_col2, _ = st.columns([1, 1, 2])

    if confirm_col1.button("Sim, deletar", key="confirm_delete_yes", type="primary"):
        current_user = user_session_controller.get_current_user()
        current_username = current_user.name if current_user else None

        success, message = admin_controller.delete_user(selected_user.name, current_username)

        if success:
            st.success(message)
            del st.session_state.confirm_action
            st.rerun()
        else:
            st.error(message)

    if confirm_col2.button("Não, cancelar", key="confirm_delete_no"):
        del st.session_state.confirm_action
        st.rerun()
