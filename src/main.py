from infrastructure.config import configure_streamlit
from infrastructure.app_factory import AppFactory
from infrastructure.session_manager import SessionManager
from controller.router import AppRouter
from infrastructure.logging_config import logger


def main() -> None:
    logger.info("Starting application")
    configure_streamlit()

    app_factory = AppFactory()
    app_factory.initialize_database()

    session_manager = SessionManager(app_factory.user_dao)
    session_manager.init_session_state()

    router = AppRouter(app_factory)
    router.route()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"Application crashed with error: {str(e)}", exc_info=True)
        raise
