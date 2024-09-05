<div align="center">
  <img src="assets/images/app-icon-web.png" width="100">
  <p><strong>microPOS:</strong> Middleware API Layer</p>
</div>

----
<div align="center">
    <img src="./assets/images/open_api.png">
</div>

----
Provides an interface between the microPOS app and supabase.  

# Setup
Clone the repo and `cd` to the directory  
Install the dependencies and enable the `.venv` with [rye](https://rye.astral.sh/guide/installation/)  
```bash
rye sync
```

# Configuration
Create a `.env` file and specify the following:
```ini
API_URL = SUPABASE_URL
KEY = API_KEY
VERSION = 0.1.0
```

# Start
```bash
python run.py
```

# Task Implementation Status
## Functionality
- [x] async client
- [ ] ... other things I haven't thought of

## Endpoints
- [ ] Menu Items
    - [x] Get by ID
    - [x] Get All
    - [x] Create
    - [x] Update by ID
    - [ ] Delete
- [ ] Categories
- [ ] Orders
- [ ] Tables