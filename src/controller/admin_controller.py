from typing import List, Optional, Tuple
from infrastructure.user_dao import UserDAO
from infrastructure.logging_config import logger
from model.user import User
from model.email import Email


class AdminController:
    def __init__(self, user_dao: UserDAO):
        self.user_dao = user_dao

    def get_all_users(self) -> List[User]:
        users = self.user_dao.get_all_users()
        return users

    def format_users_for_display(self, users: List[User]) -> List[dict]:
        return [
            {
                "Usuário": user.name,
                "Email": user.email,
                "Role": user.role,
                "Ativo": "Ativo" if user.is_active else "Inativo",
            }
            for user in users
        ]

    def find_user_by_name(self, users: List[User], username: str) -> Optional[User]:
        return next((user for user in users if user.name == username), None)

    def validate_user_update(
        self,
        user: User,
        current_username: str,
        new_password: str,
        confirm_password: str,
        new_role: str,
        new_is_active: bool,
    ) -> Tuple[bool, str]:
        if user.name == current_username and new_role != "admin":
            return False, "Você não pode remover seu próprio status de admin."

        if user.name == current_username and not new_is_active:
            return False, "Você não pode desativar sua própria conta."

        if new_password and new_password != confirm_password:
            return False, "As senhas devem ser iguais, por favor, verifique e tente novamente."

        return True, ""

    def update_user(self, user: User, email_str: str, password: str, role: str, is_active: bool) -> Tuple[bool, str]:
        try:
            user.email = Email(email_str)
            user.role = role
            user.is_active = is_active

            if password:
                logger.info(f"Password change requested for user: {user.name}")
                user.password = password

            self.user_dao.update_user(user)
            return True, f"Usuário {user.name} atualizado com sucesso!"
        except Exception as e:
            logger.error(f"Failed to update user {user.name}: {e}")
            return False, f"Falha ao atualizar o usuário {user.name}: {e}"

    def delete_user(self, username: str, current_username: str) -> Tuple[bool, str]:
        if username == current_username:
            logger.warning(f"Admin {current_username} attempted to delete own account")
            return False, "Você não pode deletar sua própria conta."

        logger.info(f"Admin {current_username} deleting user: {username}")
        try:
            self.user_dao.delete_user(username)
            return True, f"Usuário {username} deletado com sucesso."
        except Exception as e:
            logger.error(f"Failed to delete user {username}: {e}")
            return False, f"Falha ao deletar o usuário: {e}"
