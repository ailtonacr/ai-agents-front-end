import uuid
from controller.chat_controller import ChatController
from infrastructure.user_dao import UserDAO
from infrastructure.session_dao import SessionDAO
from infrastructure.message_dao import MessageDAO
from infrastructure.auth import AuthService
from infrastructure.adk_client import ADKClient
from infrastructure.schema_init import init_db
from infrastructure.logging_config import logger


class AppFactory:
    def __init__(self):
        self._adk_client = None
        self._user_dao = None
        self._session_dao = None
        self._message_dao = None
        self._auth_service = None
        self._chat_controller = None

    def initialize_database(self) -> None:
        logger.info("Initializing database schema")
        init_db()
        logger.info("Database schema initialization completed")

    @property
    def adk_client(self) -> ADKClient:
        if self._adk_client is None:
            self._adk_client = ADKClient()
        return self._adk_client

    @property
    def user_dao(self) -> UserDAO:
        if self._user_dao is None:
            self._user_dao = UserDAO()
        return self._user_dao

    @property
    def session_dao(self) -> SessionDAO:
        if self._session_dao is None:
            self._session_dao = SessionDAO()
        return self._session_dao

    @property
    def message_dao(self) -> MessageDAO:
        if self._message_dao is None:
            self._message_dao = MessageDAO()
        return self._message_dao

    @property
    def auth_service(self) -> AuthService:
        if self._auth_service is None:
            self._auth_service = AuthService(self.user_dao)
        return self._auth_service

    @property
    def chat_controller(self) -> ChatController:
        if self._chat_controller is None:
            self._chat_controller = ChatController(
                self.adk_client, self.session_dao, self.message_dao, self.get_adk_user_id
            )
        return self._chat_controller

    @staticmethod
    def get_adk_user_id(username: str) -> str:
        user_id = f"user-{uuid.uuid5(uuid.NAMESPACE_DNS, username)}"
        return user_id
