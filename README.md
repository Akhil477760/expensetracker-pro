# ExpenseTracker Pro 💰

An AI-powered personal finance management REST API built with Django REST Framework. Users can track income/expenses, categorize spending, set monthly budgets, view financial reports, and get AI-generated savings tips powered by Google's Gemini API.

## 🚀 Features

- **JWT Authentication** — secure register/login system
- **Category Management** — custom income/expense categories per user
- **Transaction Tracking** — full CRUD with filtering (by type, category, date, month)
- **Smart Budgeting** — set monthly budget limits per category with real-time spend percentage calculation
- **Financial Reports** — monthly summary (income/expense/savings) and category-wise breakdown
- **AI-Powered Insights** — Google Gemini API analyzes spending patterns and generates personalized savings tips
- **Secure & Isolated** — every user's data is completely isolated (no cross-user data leaks)

## 🛠️ Tech Stack

- **Backend**: Python, Django, Django REST Framework
- **Database**: SQLite (dev) / PostgreSQL (production-ready)
- **Authentication**: JWT (djangorestframework-simplejwt)
- **AI Integration**: Google Gemini API
- **Filtering**: django-filter

## 📋 API Endpoints

### Auth
| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/auth/register/` | Register + get JWT tokens |
| POST | `/api/auth/login/` | Login, get JWT tokens |
| POST | `/api/auth/refresh/` | Refresh access token |
| GET | `/api/auth/me/` | Get current user profile |

### Categories & Transactions
| Method | Endpoint | Description |
|---|---|---|
| GET/POST | `/api/categories/` | List / create categories |
| GET/POST | `/api/transactions/` | List / create transactions (supports filters) |
| PATCH/DELETE | `/api/transactions/<id>/` | Update / delete a transaction |

### Budgets
| Method | Endpoint | Description |
|---|---|---|
| GET/POST | `/api/budgets/` | List / create budgets — auto-includes spent amount & % used |

### Reports
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/reports/monthly-summary/` | Total income, expense, net savings |
| GET | `/api/reports/category-breakdown/` | Category-wise spend totals (for charts) |
| GET | `/api/reports/ai-insight/` | AI-generated savings tip based on spending |

## ⚙️ Setup & Installation

```bash
# Clone the repo
git clone https://github.com/Akhil477760/expensetracker-pro.git
cd expensetracker-pro

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
# Create a .env file with:
# SECRET_KEY=your-secret-key
# DEBUG=True
# GEMINI_API_KEY=your-gemini-api-key   (get free at https://aistudio.google.com)

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Start the server
python manage.py runserver
```

API runs at `http://127.0.0.1:8000/`

## 🔒 Security Notes

- All endpoints (except register/login) require JWT authentication
- Each user can only access their own data (enforced at the queryset level)
- Sensitive credentials are stored in `.env` (excluded from version control)

## 📈 Roadmap

- [ ] Docker containerization + cloud deployment
- [ ] Automated tests (pytest)
- [ ] Recurring transactions with Celery
- [ ] CSV/PDF export for transaction history
- [ ] Frontend dashboard with charts

## 👤 Author

**Akhil** — Built as part of a transition into a Software Engineer role, focused on demonstrating REST API design, authentication, and AI integration skills.