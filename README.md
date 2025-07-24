# Personal Expense Tracker API

A RESTful API built with FastAPI for tracking personal expenses with AI-powered category prediction.

## Features

- 🔐 JWT Authentication
- 💰 Complete expense management (CRUD operations)
- 📊 Daily, weekly, and monthly reports
- 🤖 AI-powered insights and spending analysis using Google Gemini
- 📈 Personalized financial recommendations and trends
- 💡 Spending pattern analysis and forecasting
- 📁 CSV export functionality
- 📚 Auto-generated API documentation

## Tech Stack

- **Framework**: FastAPI
- **Database**: MongoDB Atlas (with PyMongo)
- **Authentication**: JWT (python-jose, passlib)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up MongoDB Atlas:
- Create a free account at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
- Create a new cluster
- Create a database user with read/write permissions
- Get your connection string
- Whitelist your IP address (or use 0.0.0.0/0 for development)

5. Set up environment variables:
Create a `.env` file in the root directory:
```env
MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/expense_tracker?retryWrites=true&w=majority
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

6. Get a Gemini API key:
- Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
- Create a new API key
- Add it to your `.env` file

## Running the Application

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the application is running, you can access:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### Authentication
- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login and get JWT token
- `GET /auth/me` - Get current user info

### Expenses
- `POST /expenses/` - Add a new expense
- `GET /expenses/` - List all expenses (with pagination and filters)
- `GET /expenses/{id}` - Get specific expense
- `PUT /expenses/{id}` - Update an expense
- `DELETE /expenses/{id}` - Delete an expense

### Reports
- `GET /reports/daily` - Get daily expense summary
- `GET /reports/weekly` - Get weekly expense totals
- `GET /reports/monthly` - Get monthly summary
- `GET /reports/export/csv` - Export expenses as CSV

### AI Analytics
- `POST /ai/insights` - Get AI-powered insights for a specific period
- `GET /ai/analysis` - Get comprehensive spending analysis and forecasts

## Expense Categories

- FOOD
- TRANSPORT
- ENTERTAINMENT
- UTILITIES
- HEALTHCARE
- SHOPPING
- OTHER

## Example Usage

### Register a new user:
```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword",
    "full_name": "John Doe"
  }'
```

### Login:
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user@example.com&password=securepassword"
```

### Add an expense:
```bash
curl -X POST "http://localhost:8000/expenses/" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 25.50,
    "category": "FOOD",
    "description": "Lunch at restaurant",
    "date": "2025-07-23T12:30:00"
  }'
```

### Get AI insights:
```bash
curl -X POST "http://localhost:8000/ai/insights" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "period": "month"
  }'
```

### Get spending analysis:
```bash
curl -X GET "http://localhost:8000/ai/analysis" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## Project Structure

```
app/
├── main.py              # Application entry point
├── core/                # Core functionality
│   ├── config.py        # Configuration settings
│   ├── database.py      # Database connection
│   ├── security.py      # Password hashing, JWT
│   └── auth.py          # Authentication logic
├── models/              # MongoDB models
│   ├── user.py          # User model
│   └── expense.py       # Expense model
├── schemas/             # Pydantic schemas
│   ├── user.py          # User schemas
│   └── expense.py       # Expense schemas
├── routes/              # API routes
│   ├── auth.py          # Authentication endpoints
│   ├── expenses.py      # Expense management
│   ├── reports.py       # Reporting endpoints
│   └── ai.py            # AI prediction endpoints
├── services/            # Business logic
│   └── reports.py       # Report generation
├── ml/                  # AI/LLM integration
│   └── gemini_analyzer.py   # Gemini API for insights
└── utils/               # Utilities
    └── exceptions.py    # Exception handlers
```

## Security Considerations

- Always use strong, unique SECRET_KEY in production
- Use HTTPS in production
- Implement rate limiting for API endpoints
- Add request validation and sanitization
- Consider adding refresh tokens for better security

## License

This project is licensed under the MIT License.