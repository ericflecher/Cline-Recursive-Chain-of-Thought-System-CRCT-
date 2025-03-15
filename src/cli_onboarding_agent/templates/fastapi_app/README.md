# {{project_name}}

{{description}}

## Features

- Modern Python web API with FastAPI
- SQLAlchemy ORM for database interactions
- Pydantic models for data validation
- Dependency injection system
- Automatic API documentation with Swagger UI
- Structured project layout following best practices

## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd {{project_name}}
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

4. Run the application:

```bash
uvicorn app.main:app --reload
```

The API will be available at [http://localhost:8000](http://localhost:8000).

API documentation will be available at:
- Swagger UI: [http://localhost:8000/api/v1/docs](http://localhost:8000/api/v1/docs)
- ReDoc: [http://localhost:8000/api/v1/redoc](http://localhost:8000/api/v1/redoc)

## Project Structure

```
{{project_name}}/
├── app/                    # Application package
│   ├── api/                # API endpoints
│   │   ├── endpoints/      # API endpoint modules
│   │   └── api.py          # API router
│   ├── core/               # Core modules
│   │   ├── config.py       # Configuration settings
│   │   └── exceptions.py   # Custom exceptions
│   ├── db/                 # Database modules
│   │   └── session.py      # Database session
│   ├── models/             # SQLAlchemy models
│   │   ├── user.py         # User model
│   │   └── item.py         # Item model
│   ├── schemas/            # Pydantic schemas
│   │   ├── user.py         # User schemas
│   │   └── item.py         # Item schemas
│   ├── services/           # Business logic
│   │   ├── user_service.py # User service
│   │   └── item_service.py # Item service
│   └── main.py             # Application entry point
├── tests/                  # Test package
│   ├── conftest.py         # Test configuration
│   └── test_*.py           # Test modules
├── .env                    # Environment variables
├── .gitignore              # Git ignore file
├── requirements.txt        # Dependencies
└── README.md               # Project documentation
```

## API Endpoints

### Users

- `GET /api/v1/users/` - Get all users
- `POST /api/v1/users/` - Create a new user
- `GET /api/v1/users/{user_id}` - Get a specific user
- `PUT /api/v1/users/{user_id}` - Update a user
- `DELETE /api/v1/users/{user_id}` - Delete a user

### Items

- `GET /api/v1/items/` - Get all items
- `POST /api/v1/items/` - Create a new item
- `GET /api/v1/items/{item_id}` - Get a specific item
- `PUT /api/v1/items/{item_id}` - Update an item
- `DELETE /api/v1/items/{item_id}` - Delete an item

## Development

### Running Tests

```bash
pytest
```

### Code Formatting

```bash
black app tests
isort app tests
```

## Deployment

### Docker

A Dockerfile is provided to containerize the application:

```bash
docker build -t {{project_name}} .
docker run -p 8000:8000 {{project_name}}
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

{{author}}
