import bcrypt
from model.user import User
from model.email import Email
from .logging_config import logger


class AuthService:
    def __init__(self, db):
        self.db = db

    @staticmethod
    def verify_password(plain_password: str, hashed_password_with_salt: bytes) -> bool:
        plain_password_bytes = plain_password.encode("utf-8")
        try:
            result = bcrypt.checkpw(plain_password_bytes, hashed_password_with_salt)
            return result
        except ValueError as e:
            logger.warning(f"Password verification failed with ValueError: {str(e)}")
            return False

    @staticmethod
    def get_password_hash(password: str) -> str:
        password_bytes = password.encode("utf-8")
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password_bytes, salt)
        return hashed_password.decode("utf-8")

    def register_user(self, username: str, password: str, email: Email | None = None) -> tuple[bool, str]:
        logger.info(f"Attempting to register user: {username}")

        if not username or not password:
            logger.warning(f"Registration failed for {username}: missing username or password")
            return False, "Usuário e senha são obrigatórios."
        if len(password) < 6:
            logger.warning(f"Registration failed for {username}: password too short")
            return False, "Senha deve ter pelo menos 6 caracteres."

        hashed_password = self.get_password_hash(password)
        is_first_user = self.db.count_users() == 0
        role = "admin" if is_first_user else "user"

        user = User(username, None, email, role, True, hashed_password)

        if self.db.create_user(user):
            if is_first_user:
                logger.info(f"First admin user created successfully: {username}")
                return True, f'Usuário admin "{username}" registrado com sucesso! Faça o login.'
            return True, f'Usuário "{username}" registrado com sucesso! Faça o login.'
        else:
            logger.error(f"Failed to create user {username}: username or email already exists")
            return False, "Nome de usuário ou email já existe."

    def authenticate_user(self, username: str, password: str) -> User | None:
        logger.info(f"Attempting to authenticate user: {username}")

        user = self.db.get_user_by_username(username)
        if not user:
            logger.warning(f"Authentication failed for {username}: user not found")
            return None
        if not user.is_active:
            logger.warning(f"Authentication failed for {username}: user account is inactive")
            return None
        row = self.db.fetch_one("SELECT hashed_password FROM users WHERE username = %s", (username,))
        if not row:
            logger.warning(f"Authentication failed for {username}: no password hash found")
            return None
        stored_hashed_password_bytes = row["hashed_password"].encode("utf-8")
        if not self.verify_password(password, stored_hashed_password_bytes):
            logger.warning(f"Authentication failed for {username}: invalid password")
            return None

        logger.info(f"User authenticated successfully: {username}")
        return user
