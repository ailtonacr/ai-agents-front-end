# AI Agents Frontend

Streamlit web interface for interacting with AI agents. This frontend connects to the ADK backend running on port 8000.

## 🚀 How to Run

### Prerequisites
- Docker and Docker Compose
- ADK backend running on `http://localhost:8000`

### Quick Setup

1. **Configure environment variables:**
   ```bash
   cp .env.example .env
   ```
   
   Edit the `.env` file with your settings:
   - `API_BASE_URL=http://localhost:8000` (ADK backend URL)
   - `GOOGLE_API_KEY=your_google_api_key`

2. **Run with Docker:**
   ```bash
   make docker-run
   ```

3. **Access the application:**
   - Frontend: http://localhost:8501
   - PostgreSQL Database: localhost:5432

### Stop the Application
```bash
make docker-stop
```

## 📋 Features

- **Authentication**: User registration and login
- **Agent Chat**: Interface to chat with different AI agents
- **History**: View previous conversations
- **Admin Panel**: User management (for administrators)

## 🔧 Local Development

If you prefer to run without Docker:

```bash
# Install dependencies
make setup

# Configure environment variables
cp .env.example .env

# Run application
streamlit run src/main.py
```

## 🛠️ Development Commands

- `make help` - Shows all available commands
- `make setup` - Installs project dependencies
- `make lint` - Formats code using Black
- `make test` - Runs unit tests with coverage
- `make docker-run` - Runs with Docker (builds if needed)
- `make docker-stop` - Stops and removes containers

**Important**: Make sure the ADK backend is running on `http://localhost:8000` before starting the frontend.
