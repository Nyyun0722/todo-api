TODO List API

This is a simple containerized REST API for a TODO list service built with Flask, SQLAlchemy, and GitHub OAuth. It allows users to:

- Authenticate with GitHub
- Create, list, update, delete TODO items
- Mark TODO items as completed


Features

- GitHub OAuth login
- RESTful TODO CRUD operations
- Mark TODO as completed
- Token-based auth (Bearer user\_id for simplicity)
- PostgreSQL database
- Docker + Docker Compose
- Unit tests with 'unittest'


Setup & Run

1. Prerequisites

- Docker Desktop
- GitHub OAuth app (for client ID and secret)

2. Clone

git clone https://github.com/YOUR_USERNAME/todo-api.git
cd todo-api


3. Create '.env'

cp .env.example .env

Fill in the actual GitHub credentials.


4. Start Server

docker-compose up --build

Server will be available at 'http://localhost:5000'


5. Login URL

http://localhost:5000/auth/login


6. API Usage (via curl or Postman)

- Use 'Authorization: Bearer <user_id>' in headers

Add TODO

$headers = @{
    "Authorization" = "Bearer 1"
    "Content-Type" = "application/json"
}
$body = @{
    title = "Test from VSCode"
    description = "in PowerShell"
} | ConvertTo-Json
Invoke-WebRequest -Uri "http://localhost:5000/todos" -Method Post -Headers $headers -Body $body


List TODOs

$headers = @{
    "Authorization" = "Bearer 1"
}
Invoke-WebRequest -Uri "http://localhost:5000/todos" -Method Get -Headers $headers | Select-Object -ExpandProperty Content | ConvertFrom-Json


Mark as Completed

$headers = @{
    "Authorization" = "Bearer 1"
    "Content-Type" = "application/json"
}
# First get the current todo item
$todo = Invoke-WebRequest -Uri "http://localhost:5000/todos/1" -Method Get -Headers $headers | 
    Select-Object -ExpandProperty Content | ConvertFrom-Json

# Update the completed status
$todo.completed = $true

# Send the updated todo back
Invoke-WebRequest -Uri "http://localhost:5000/todos/1" -Method Put -Headers $headers -Body ($todo | ConvertTo-Json)


Delete

$headers = @{
    "Authorization" = "Bearer 1"
}
Invoke-WebRequest -Uri "http://localhost:5000/todos/{id}" -Method Delete -Headers $headers


7. Run Tests

docker-compose exec web python -m unittest discover tests


8. Docker Hub

Image pushed to:

docker.io/YOUR_DOCKER_USERNAME/todo-api
