# TaskMaster Pro - Advanced Todo Application

A modern, full-featured todo application featuring JWT authentication, priority-based task management, and a stunning neon glow UI with glassmorphism effects.

## Features

### Phase 1: Basic Todo App
- **Backend**: FastAPI-powered RESTful API
- **Frontend**: Next.js-based responsive interface
- **Core Functionality**: Create, read, update, and delete tasks
- **Database Integration**: PostgreSQL/SQLite backend

### Phase 2: Enhanced Features
- **JWT Authentication System**: Secure sign up and login functionality
- **Neon Glow UI**: Modern aesthetic with glassmorphism design elements
- **Task Priority Levels**: High, Medium, and Low priority classifications
- **Enhanced Security**: Token-based authentication and authorization

### Phase 3: Agentic Todo Chatbot
- **AI-Powered Assistant**: Natural language interaction with your todo list
- **Backend Framework**: FastAPI with advanced routing and async capabilities
- **Database**: SQLModel for elegant ORM operations
- **AI Integration**: Llama-3 powered agent for intelligent task management
- **Frontend Interface**: Streamlit-based chat interface for seamless interaction

## Tech Stack

- **Backend**: [FastAPI](https://fastapi.tiangolo.com/) - Modern, fast (high-performance) web framework for building APIs with Python 3.7+
- **Frontend**: [Next.js](https://nextjs.org/) - React-based framework for production-ready applications
- **Database**: PostgreSQL/SQLite - Reliable and scalable database solutions
- **Styling**: [Tailwind CSS](https://tailwindcss.com/) - Utility-first CSS framework for rapid UI development
- **Authentication**: JWT (JSON Web Tokens) - Secure token-based authentication system

## Installation

### Prerequisites
- Node.js (v14 or later)
- Python (v3.7 or later)
- PostgreSQL or SQLite

### Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Set up environment variables:
   ```bash
   # Create a .env file with the following variables:
   DATABASE_URL="sqlite:///./todo.db"  # Or your PostgreSQL connection string
   SECRET_KEY="your-secret-key-here"
   ALGORITHM="HS256"
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

6. Initialize the database:
   ```bash
   python init_db.py
   ```

7. Start the backend server:
   ```bash
   uvicorn main:app --reload
   ```

### Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Set up environment variables:
   ```bash
   # Create a .env.local file with the following variables:
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

4. Start the development server:
   ```bash
   npm run dev
   ```

## Usage

1. Visit `http://localhost:3000` in your browser
2. Sign up for a new account or log in if you already have one
3. Start managing your tasks with priority levels:
   - High: Urgent tasks requiring immediate attention
   - Medium: Important tasks to complete soon
   - Low: Less urgent tasks for later

## Project Structure

```
Hackathon-2-Q4/
├── backend/
│   ├── main.py          # FastAPI application entry point
│   ├── auth.py          # Authentication logic
│   ├── models.py        # Database models
│   ├── init_db.py       # Database initialization script
│   └── requirements.txt # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── pages/       # Next.js pages
│   │   ├── components/  # Reusable UI components
│   │   └── utils/       # Utility functions
│   ├── package.json     # Node.js dependencies
│   └── tailwind.config.js # Tailwind CSS configuration
├── README.md
└── requirements.txt
```

## API Endpoints

### Authentication
- `POST /auth/signup` - Create a new user account
- `POST /auth/login` - Authenticate user and return JWT token

### Tasks
- `GET /tasks` - Retrieve all tasks for authenticated user
- `POST /tasks` - Create a new task
- `PUT /tasks/{id}` - Update an existing task
- `DELETE /tasks/{id}` - Delete a task

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with FastAPI for high-performance API development
- Designed with Next.js for optimal user experience
- Styled with Tailwind CSS for beautiful, responsive UI
- Secured with JWT authentication for reliable user management