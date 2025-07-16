CHAT_STYLES = """
    <style>
        /* Overall page adjustments */
        .stApp {
            background-color: #0E1117; /* Dark background for the whole app */
        }
        /* Main chat container styling */
        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 1rem;
            padding-left: 1rem;
            padding-right: 1rem;
        }

        /* Sidebar styling */
        .st-emotion-cache-16txtl3 { /* Main sidebar container */
            background-color: #1F232A; /* Slightly lighter dark for sidebar */
        }
        div[data-testid="stSidebarUserContent"] {
             padding: 1rem;
        }

        .sidebar-user-name-display {
            display: flex;
            align-items: center;
            padding: 80px 0px;
            margin-bottom: 1rem;
            border-bottom: 1px solid #333;
        }
        .sidebar-user-name-display span {
            margin-left: 10px;
            font-weight: bold;
            color: #FFFFFF;
        }
        .sidebar-button {
            display: block;
            width: 100%;
            border: 1px solid #4A4A4A !important;
            background-color: #2A2D35 !important;
            color: #FFFFFF !important;
            text-align: left;
            padding: 10px 15px !important;
            border-radius: 8px !important;
            margin-bottom: 8px !important;
            transition: background-color 0.2s ease;
        }
        .sidebar-button:hover {
            background-color: #3A3D45 !important;
        }
        .sidebar-button.selected-chat {
            background-color: #0078D4 !important; /* Highlight selected chat */
            border: 1px solid #0078D4 !important;
        }
        .sidebar-section-header {
            font-size: 0.9rem;
            color: #A0A0A0;
            margin-top: 1.5rem;
            margin-bottom: 0.5rem;
            text-transform: uppercase;
        }

        /* Chat messages styling */
        .chat-message-container {
            display: flex;
            flex-direction: column;
            margin-bottom: 12px;
        }
        .chat-bubble {
            padding: 10px 15px;
            border-radius: 18px;
            max-width: 75%;
            word-wrap: break-word;
            color: white; /* Default text color for bubbles */
        }
        .user-message .chat-bubble {
            background-color: #005C9D; /* User message bubble color (e.g. blue) */
            align-self: flex-end;
            border-bottom-right-radius: 5px;
        }
        .agent-message .chat-bubble {
            background-color: #2B3139; /* Agent message bubble color (e.g. dark grey) */
            align-self: flex-start;
            border-bottom-left-radius: 5px;
        }
        .message-role {
            font-size: 0.8em;
            color: #888;
            margin-bottom: 3px;
        }
        .user-message .message-role {
            text-align: right;
            margin-right: 5px;
        }
        .agent-message .message-role {
            text-align: left;
            margin-left: 5px;
        }

        /* Typing indicator placeholder style */
        .typing-indicator .chat-bubble {
            background-color: #2B3139;
            align-self: flex-start;
            border-bottom-left-radius: 5px;
            color: #AAAAAA;
            font-style: italic;
        }

        /* Input area */
        div[data-testid="stChatInput"] {
             background-color: #1F232A; /* Match sidebar or a distinct input area color */
        }
         div[data-testid="stChatInput"] textarea {
            background-color: #2B3139;
            color: white;
            border-radius: 8px;
        }

        /* Agent selection in main area if needed */
        .stSelectbox div[data-baseweb="select"] > div {
            background-color: #2B3139;
            border: 1px solid #4A4A4A;
            color: white;
        }
        .stSelectbox div[data-baseweb="select"] > div:hover {
             border-color: #0078D4;
        }
         .stSelectbox li {
            background-color: #2B3139;
            color: white;
        }
        .stSelectbox li:hover {
            background-color: #3A3D45;
        }
    </style>
"""
