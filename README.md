<div align="center">
    <img src="assets/images/app-icon-web.png" alt="MicroPOS Logo" width="100">
    <p><strong>microPOS:</strong> Middleware API Layer</p>
</div>

----
<div align="center">
    <img src="assets/images/item_api_routes.svg" alt="Item API Routes" width="600">
</div>

----
Provides an interface between the microPOS app and supabase.  
Built with FastAPI, pydantic, supabase-py, and uvicorn.  

# Setup

Clone the repo and `cd` to the directory  
Install the dependencies and enable the `.venv` with [uv](https://docs.astral.sh/uv/getting-started/installation/)  

```bash
uv sync
```

# Configuration

Create a `.env` file and specify the following:

```ini
API_URL = SUPABASE_URL
KEY = API_KEY
VERSION = 0.1.0
DEBUG = true
```

# Start

```bash
. .venv/bin/activate
python start_app.py
```

# Docker Approach

```bash
docker build -t micropos-api
docker run --name micropos-api -d micropos-api
```

# Task Implementation Status

## Functionality

- [x] async client
- [x] database seeding
- [ ] authentication
- [ ] ... other things I haven't thought of

## Endpoints (v1)

- [x] Items
  - [x] Get by ID
  - [x] Get All
  - [x] Create
  - [x] Update by ID
  - [x] Delete
- [x] Categories
  - [x] Get by ID
  - [x] Get All
  - [x] Create
  - [x] Update by ID
  - [x] Delete
- [ ] Storage
- [ ] Orders
- [ ] Tables

## Endpoints (v2)

- [ ] Accounts (New/Sign-in/Reset/Delete)
- [ ] Filtering
- [ ] Joins
