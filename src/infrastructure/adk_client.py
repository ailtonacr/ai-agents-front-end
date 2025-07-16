from .logging_config import logger
import os
import uuid
import requests
import json
import time


class ADKClient:
    def __init__(self):
        self.API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

    def get_available_agents(self) -> list[str]:
        try:
            response = requests.get(f"{self.API_BASE_URL}/list-apps?relative_path=./")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error fetching agents: {e}")
            return []

    def create_adk_session(self, agent_name: str, user_id_for_adk: str) -> str | None:
        adk_session_id = f"session-{int(time.time())}-{uuid.uuid4()}"
        try:
            response = requests.post(
                f"{self.API_BASE_URL}/apps/{agent_name}/users/{user_id_for_adk}/sessions/{adk_session_id}",
                headers={"Content-Type": "application/json"},
                data=json.dumps({}),
            )
            response.raise_for_status()
            return adk_session_id
        except requests.RequestException as e:
            logger.error(f"Error creating ADK session: {e}")
            return None

    def send_message_to_adk(
        self, agent_name: str, user_id_for_adk: str, adk_session_id: str, message_text: str
    ) -> list[dict]:
        payload = {
            "app_name": agent_name,
            "user_id": user_id_for_adk,
            "session_id": adk_session_id,
            "new_message": {"role": "user", "parts": [{"text": message_text}]},
        }
        try:
            response = requests.post(
                f"{self.API_BASE_URL}/run", headers={"Content-Type": "application/json"}, data=json.dumps(payload)
            )
            response.raise_for_status()
            events = response.json()
            messages = []
            for event in events:
                content = event.get("content", {})
                role = content.get("role")
                parts = content.get("parts", [])
                for part in parts:
                    text = part.get("text")
                    if text:
                        messages.append({"role": role, "text": text})
            return messages
        except requests.RequestException as e:
            logger.error(f"Error sending message to ADK: {e}")
            return [{"role": "agent", "text": f"Error: Could not connect to ADK. ({e})"}]
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding ADK response: {e}")
            return [{"role": "agent", "text": "Error: Invalid response from ADK."}]
