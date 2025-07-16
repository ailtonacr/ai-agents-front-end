from .base_dao import BaseDAO
from model.message import Message
from .logging_config import logger


class MessageDAO(BaseDAO):
    def add_message(self, session_db_id: str, message: Message):
        logger.debug(f"Adding message to session {session_db_id}: role={message.role}")
        query = "INSERT INTO messages (session_db_id, role, text, timestamp) VALUES (%s, %s, %s, %s)"
        params = (session_db_id, message.role, message.text, message.timestamp)
        try:
            self.execute(query, params, commit=True)
            logger.debug(f"Message added successfully to session {session_db_id}")
        except Exception as e:
            logger.error(f"Failed to add message to session {session_db_id}: {str(e)}")
            raise

    def get_messages_for_session(self, session_db_id: str) -> list[Message]:
        logger.debug(f"Fetching messages for session: {session_db_id}")
        try:
            rows = self.fetch_all(
                "SELECT role, text, timestamp FROM messages WHERE session_db_id = %s ORDER BY timestamp ASC",
                (session_db_id,),
            )
            messages = []
            for row in rows:
                message = Message(role=row["role"], text=row["text"], timestamp=row["timestamp"])
                messages.append(message)
            logger.debug(f"Retrieved {len(messages)} messages for session {session_db_id}")
            return messages
        except Exception as e:
            logger.error(f"Failed to fetch messages for session {session_db_id}: {str(e)}")
            raise
