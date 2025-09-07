# Financial AI Agents

A comprehensive financial assistant application built with FastAPI, LangGraph, and Streamlit that provides AI-powered financial advice, planning tools, and report generation.

## Features

- **Multi-Agent Financial Assistant**: AI agent with 9 specialized financial tools
- **User Authentication**: Secure registration and login with JWT tokens
- **Persistent Chat History**: Conversations saved to database with memory across sessions
- **Financial Calculations**: Tools for savings, investments, loans, budgets, taxes, and more
- **PDF Report Generation**: Downloadable financial analysis reports
- **Real-time Conversations**: Agent remembers context within chat sessions

## Technology Stack

### Backend
- **FastAPI**: Async web framework
- **MySQL**: Primary database with async SQLAlchemy
- **Redis**: Caching and session management
- **Alembic**: Database migrations
- **LangGraph**: AI agent orchestration
- **OpenAI GPT**: Large language model
- **Pydantic**: Data validation and settings
- **JWT**: Authentication tokens
- **ReportLab**: PDF generation

### Frontend
- **Streamlit**: Web interface
- **HTTPX**: HTTP client for API calls

### Infrastructure
- **Docker**: Containerization
- **Docker Compose**: Multi-service orchestration
- **Uvicorn**: ASGI server

## Setup Instructions

### Prerequisites
- Docker and Docker Compose
- Python 3.11+ (for local development)
- OpenAI API key

### Environment Setup

1. **Clone the repository**
   cpgit clone https://github.com/HassanAbdelshafy21/financial-ai-agents.git cd financial-ai-agents

2. Create environment file
   cp .env.example .env
3.Configure environment variables
Edit .env file with your settings:
  APP_ENV=dev
  SECRET_KEY=your_secret_key_here
  JWT_EXPIRES_MIN=60
  DB_URI=mysql+aiomysql://root:pickles@mysql:3306/finai
  REDIS_URL=redis://redis:6379/0
  OPENAI_API_KEY=your_openai_api_key_here
  SMTP_HOST=
  SMTP_PORT=
  SMTP_USER=
  SMTP_PASS=
  FROM_EMAIL=

###Running the application
1.Start services with Docker
 docker-compose up --build -d
2.Run database migrations
 docker-compose exec api alembic upgrade head
3.Install Streamlit dependencies (if running locally)
 pip install streamlit httpx
4.Start Streamlit frontend
 streamlit run streamlit_app/main.py
5.Access the application
 Frontend: http://localhost:8501
 API: http://localhost:8000
 API Documentation: http://localhost:8000/docs
 API Redoc: http://localhost:8000/redoc

Usage
1.Registration: Create a new account with email and password
2.Login: Access your account to start using the financial assistant
3.Chat: Interact with the AI agent for financial advice and calculations
4.Tools: Use specialized financial calculators and analyzers
5.Reports: Generate and download PDF reports of your financial analysis
6.History: View and continue previous conversations


API Endpoints
Authentication

POST /api/v1/auth/register - User registration
POST /api/v1/auth/login - User login
GET /api/v1/auth/me - Get current user information

Chat Management

GET /api/v1/chats/ - List user's chat sessions
POST /api/v1/chats/ - Create new chat session
DELETE /api/v1/chats/{chat_id} - Delete specific chat
GET /api/v1/chats/{chat_id}/messages - Get messages from chat
POST /api/v1/chats/{chat_id}/messages - Save message to chat

Agent Interaction
POST /api/v1/query - Send query to AI agent with conversation memory

Reports
POST /api/v1/reports/generate - Generate and download PDF financial report

Health Check
GET /api/v1/health/ - Application health status

Architecture
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Streamlit     │    │    FastAPI      │    │     MySQL       │
│   Frontend      │◄──►│    Backend      │◄──►│   Database      │
│   (Port 8501)   │    │   (Port 8000)   │    │   (Port 3307)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │     Redis       │
                       │   Cache/State   │
                       │   (Port 6379)   │
                       └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │   LangGraph     │
                       │   AI Agents     │
                       │   + OpenAI      │
                       └─────────────────┘
Financial Tools Available

1.Savings Calculator - Calculate total savings over time periods
2.Compound Interest Calculator - Investment growth with monthly contributions
3.Loan Payment Calculator - Monthly payment calculations with amortization
4.Portfolio Analyzer - Investment allocation and risk analysis
5.Budget Planner - Income and expense analysis with recommendations
6.Retirement Calculator - Retirement savings projections and planning
7.Debt Payoff Calculator - Compare different debt payoff strategies
8.Emergency Fund Calculator - Emergency fund planning and targets
9.Tax Calculator - Federal income tax estimation (US)

Key Features Explained
Conversation Memory
The system uses LangGraph with MemorySaver to maintain context within chat sessions. Each conversation has a unique thread_id that preserves the conversation history, allowing the AI to reference previous messages and maintain coherent, contextual responses.

Database Persistence
All user conversations are saved to MySQL database with the following structure:

-Users table for authentication
-Chats table for conversation sessions
-Messages table for individual chat messages

PDF Report Generation
Uses ReportLab to generate comprehensive financial reports including:

-User information and date
-Financial summary data
-Conversation summaries
-Personalized recommendations
