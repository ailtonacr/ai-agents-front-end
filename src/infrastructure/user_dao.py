from .base_dao import BaseDAO
from model.user import User
from .auth import AuthService
from .logging_config import logger


class UserDAO(BaseDAO):
    def create_user(self, user: User) -> bool:
        logger.info(f"Creating user: {user.name} with role: {user.role}")
        query = (
            "INSERT INTO users (id, username, hashed_password, email, role) VALUES (%s, %s, %s, %s, %s)"
            if user.email
            else "INSERT INTO users (id, username, hashed_password, role) VALUES (%s, %s, %s, %s)"
        )
        params = (
            (user.id, user.name, user.password, user.email, user.role)
            if user.email
            else (user.id, user.name, user.password, user.role)
        )
        try:
            self.execute(query, params, commit=True)
            return True
        except Exception as e:
            logger.error(f"Failed to create user {user.name}: {str(e)}")
            return False

    def get_user_by_username(self, username: str) -> User | None:
        row = self.fetch_one(
            "SELECT id, username, email, role, is_active FROM users WHERE username = %s", (username,)
        )
        if row:
            return User(
                id=row["id"], name=row["username"], email=row["email"], role=row["role"], is_active=row["is_active"]
            )
        return None

    def count_users(self) -> int:
        row = self.fetch_one("SELECT COUNT(*) as count FROM users")
        count = row["count"] if row else 0
        return count

    def get_all_users(self) -> list[User]:
        rows = self.fetch_all("SELECT id, username, email, role, is_active, created_at FROM users")
        users = [
            User(id=row["id"], name=row["username"], email=row["email"], role=row["role"], is_active=row["is_active"])
            for row in rows
        ]
        return users

    def delete_user(self, username: str) -> bool:
        logger.info(f"Deleting user: {username}")
        try:
            self.execute("DELETE FROM users WHERE username = %s", (username,), commit=True)
            return True
        except Exception as e:
            logger.error(f"Failed to delete user {username}: {str(e)}")
            raise

    def update_user(self, user: User) -> bool:
        try:
            if user.password is not None:
                query = """
                        UPDATE users
                        SET username = %s, email = %s, role = %s, is_active = %s, hashed_password = %s
                        WHERE id = %s
                        """
                params = (
                    user.name,
                    user.email,
                    user.role,
                    user.is_active,
                    AuthService.get_password_hash(user.password),
                    user.id,
                )
            else:
                query = """
                        UPDATE users
                        SET username = %s, email = %s, role = %s, is_active = %s
                        WHERE id = %s
                        """
                params = (user.name, user.email, user.role, user.is_active, user.id)
            self.execute(query, params, commit=True)
            return True
        except Exception as e:
            logger.error(f"Failed to update user {user.name}: {str(e)}")
            raise
