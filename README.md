# E-commerce application on Fast API

## How to use

### Development (Docker)

1. Make sure Docker and Docker Compose are installed.

2. Build and start the app with PostgreSQL:

```bash
docker compose up --build
```

3. Apply migrations
```bash
docker compose exec web alembic upgrade head
```

4. Open the browser and go to:

```bash
http://127.0.0.1:8000/docs
```

To stop the containers:

```bash
docker compose down
```

### Production (Docker)

Build and start the production stack (Gunicorn + Nginx + PostgreSQL):

```bash
docker compose -f docker-compose.prod.yml up --build
```

Open the browser and go to:

```bash
http://127.0.0.1:8000/docs
```

### Local run without Docker (optional)

1. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Windows (PowerShell):

```bash
python -m venv .venv
. .\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Start the server:

```bash
uvicorn app.main:app --reload
```

4. Open:

```bash
http://127.0.0.1:8000/docs
```
