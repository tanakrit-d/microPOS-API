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

Create a `.env` file as follows:

```ini
ENVIRONMENT = ""
```

Then, create any additional environments (such as `.env.local` or `.env.development`) as required:

```ini
API_URL = SUPABASE_URL
API_KEY = API_KEY
VERSION = 0.1.0
ENVIRONMENT = development
DEBUG = true
```

We'll then use `.env` to pass through the environment to `FastAPI` and `Configuration`.  
This is because `uvicorn` spawns a new process, which results in the app being unable to access any `Configuration` object initialised at runtime.  

# Start

```bash
python start_app.py --env development
```

# Docker (Not Ready)

```bash
docker build -t micropos-api
docker run --name micropos-api -d micropos-api
```

# Local Development (Supabase CLI)

If you wish to develop locally, set up [supabase-cli](https://supabase.com/docs/guides/local-development?queryGroups=package-manager&package-manager=pnpm)  
You'll need to ensure you: `login`, `link`, and `migration fetch`.  

# Seeding the Database

Provided your `.env` files are setup, you can seed your database with [start_seed.py](./start_seed.py).

## Example

```log
python start_seed.py --count 3 --env development
2024-11-11 16:57:23 - micropos-api - INFO - Config - Loading from: /Users/cool-guy/Repositories/microPOS-API/.env.development
2024-11-11 16:57:23 - micropos-api - INFO - Config - Successfully loaded environment: development
2024-11-11 16:57:23 - micropos-api - INFO - Seeder - Starting seeding process ...
2024-11-11 16:57:23 - micropos-api - INFO - Seeder - Connecting to supabase instance ...
2024-11-11 16:57:23 - micropos-api - INFO - Seeder - Initializing seeder for environment: development
2024-11-11 16:57:23 - micropos-api - INFO - Seeder - Seeding 3 item(s) ...
2024-11-11 16:57:23 - micropos-api - INFO - Seeder - Created item: title=Spicy Salad; id=ab8ca6bb-3135-4360-8fc4-ab21cc57a727;
2024-11-11 16:57:23 - micropos-api - INFO - Seeder - Created item: title=Homemade Seafood; id=49f2d0fd-c22e-4e03-8627-39c80589a53f;
2024-11-11 16:57:23 - micropos-api - INFO - Seeder - Created item: title=Homemade Rice Bowl; id=30f1ef8c-de62-424b-af5c-ed824fee7d0e;
2024-11-11 16:57:23 - micropos-api - INFO - Seeder - Successfully seeded 3 item(s) in environment: development
```

# Task Implementation Status

## Functionality

- [x] async client
- [x] environment configuration
- [x] database seeding
  - [ ] add other tables
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
