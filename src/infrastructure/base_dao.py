import os
import psycopg2
import psycopg2.extras
from typing import Any
from .logging_config import logger


class BaseDAO:
    def __init__(self):
        self.host = os.getenv("POSTGRES_HOST", "localhost")
        self.port = os.getenv("POSTGRES_PORT", "5432")
        self.user = os.getenv("POSTGRES_USER")
        self.password = os.getenv("POSTGRES_PASSWORD")
        self.database = os.getenv("POSTGRES_DATABASE")

    def get_db_connection(self):
        try:
            conn = psycopg2.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database
            )
            return conn
        except Exception as e:
            logger.error(f"Failed to establish database connection: {str(e)}")
            raise

    def execute(self, query: str, params: tuple = (), commit: bool = False) -> None:
        conn = self.get_db_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        try:
            cursor.execute(query, params)
            if commit:
                conn.commit()
        except Exception as e:
            logger.error(f"Query execution failed: {str(e)}")
            conn.rollback()
            raise
        finally:
            cursor.close()
            conn.close()

    def fetch_one(self, query: str, params: tuple = ()) -> dict[str, Any] | None:
        conn = self.get_db_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        try:
            cursor.execute(query, params)
            row = cursor.fetchone()
            return dict(row) if row else None
        except Exception as e:
            logger.error(f"Fetch one failed: {str(e)}")
            raise
        finally:
            cursor.close()
            conn.close()

    def fetch_all(self, query: str, params: tuple = ()) -> list[dict[str, Any]]:
        conn = self.get_db_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        try:
            cursor.execute(query, params)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Fetch all failed: {str(e)}")
            raise
        finally:
            cursor.close()
            conn.close()
