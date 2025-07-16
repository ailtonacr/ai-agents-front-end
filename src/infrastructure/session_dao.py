from .base_dao import BaseDAO
from model.chat_session import ChatSession
from model.user import User
import datetime
from uuid import uuid5, NAMESPACE_DNS
from .logging_config import logger


class SessionDAO(BaseDAO):
    def create_chat_session_from_object(self, chat_session: ChatSession) -> str:
        logger.info(f"Creating chat session for user {chat_session.user_name} with agent {chat_session.agent_name}")
        query = "INSERT INTO sessions (id, username, adk_session_id, agent_name, summary, created_at) VALUES (%s, %s, %s, %s, %s, %s)"
        params = (
            chat_session.db_id,
            chat_session.user_name,
            chat_session.adk_session_id,
            chat_session.agent_name,
            chat_session.summary,
            chat_session.created_at,
        )
        try:
            self.execute(query, params, commit=True)
            logger.info(f"Chat session created successfully with ID: {chat_session.db_id}")
            return chat_session.db_id
        except Exception as e:
            logger.error(f"Failed to create chat session for user {chat_session.user_name}: {str(e)}")
            raise

    def get_sessions_for_user(self, user: User) -> list[ChatSession]:
        logger.debug(f"Fetching sessions for user: {user.name}")
        try:
            rows = self.fetch_all(
                "SELECT id, adk_session_id, agent_name, summary, created_at FROM sessions WHERE username = %s ORDER BY created_at DESC",
                (user.name,),
            )
            sessions = [
                ChatSession(
                    db_id=row["id"],
                    adk_session_id=row["adk_session_id"],
                    user_name=user.name,
                    agent_name=row["agent_name"],
                    created_at=row["created_at"],
                    summary=row["summary"] or f"Chat com {row['agent_name']}",
                )
                for row in rows
            ]
            logger.debug(f"Retrieved {len(sessions)} sessions for user {user.name}")
            return sessions
        except Exception as e:
            logger.error(f"Failed to fetch sessions for user {user.name}: {str(e)}")
            raise

    def get_session_details(self, session_db_id: str) -> ChatSession | None:
        logger.debug(f"Fetching session details for ID: {session_db_id}")
        try:
            row = self.fetch_one(
                "SELECT id, username, adk_session_id, agent_name, summary, created_at FROM sessions WHERE id = %s",
                (session_db_id,),
            )
            if row:
                session = ChatSession(
                    db_id=row["id"],
                    adk_session_id=row["adk_session_id"],
                    user_name=row["username"],
                    agent_name=row["agent_name"],
                    created_at=row["created_at"],
                    summary=row["summary"] or f"Chat com {row['agent_name']}",
                )
                logger.debug(f"Session details found for ID: {session_db_id}")
                return session
            else:
                logger.warning(f"No session details found for ID: {session_db_id}")
                return None
        except Exception as e:
            logger.error(f"Failed to fetch session details for ID {session_db_id}: {str(e)}")
            raise
