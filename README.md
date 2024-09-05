<div align="center">
  <img src="assets/images/app-icon-web.png" width="100">
  <p><strong>microPOS:</strong> Middleware API Layer</p>
</div>

----
<div style="width: 600px; margin: 20px auto;">
    <div style="font-family: sans-serif; font-size: 24px; color: #3b4151;">Items</div>
    <div style="display: flex; align-items: center; margin-bottom: 10px; border-radius: 4px; border: 1px solid #61affe; padding: 5px;">
        <div style="width: 80px; text-align: center; padding: 10px; border-radius: 5px; color: white; font-weight: bold; background-color: #61affe;">GET</div>
        <div style="flex-grow: 1; padding: 10px; color: #3b4151; background-color: #fff; border-radius: 5px; margin-left: 10px;"><b>/item/{item_id}</b> Get Menu Item</div>
    </div>
    <div style="display: flex; align-items: center; margin-bottom: 10px; border-radius: 4px; border: 1px solid #61affe; padding: 5px;">
        <div style="width: 80px; text-align: center; padding: 10px; border-radius: 5px; color: white; font-weight: bold; background-color: #61affe;">GET</div>
        <div style="flex-grow: 1; padding: 10px; color: #3b4151; background-color: #fff; border-radius: 5px; margin-left: 10px;"><b>/item/</b> Get All Menu Items</div>
    </div>
    <div style="display: flex; align-items: center; margin-bottom: 10px; border-radius: 4px; border: 1px solid #49cc90; padding: 5px;">
        <div style="width: 80px; text-align: center; padding: 10px; border-radius: 5px; color: white; font-weight: bold; background-color: #49cc90;">POST</div>
        <div style="flex-grow: 1; padding: 10px; color: #3b4151; background-color: #fff; border-radius: 5px; margin-left: 10px;"><b>/item/create</b> Create Menu Item</div>
    </div>
    <div style="display: flex; align-items: center; margin-bottom: 10px; border-radius: 4px; border: 1px solid #50e3c2; padding: 5px;">
        <div style="width: 80px; text-align: center; padding: 10px; border-radius: 5px; color: white; font-weight: bold; background-color: #50e3c2;">PATCH</div>
        <div style="flex-grow: 1; padding: 10px; color: #3b4151; background-color: #fff; border-radius: 5px; margin-left: 10px;"><b>/item/{item_id}</b> Update Menu Item</div>
    </div>
    <div style="display: flex; align-items: center; margin-bottom: 10px; border-radius: 4px; border: 1px solid #f93e3e; padding: 5px;">
        <div style="width: 80px; text-align: center; padding: 10px; border-radius: 5px; color: white; font-weight: bold; background-color: #f93e3e;">DELETE</div>
        <div style="flex-grow: 1; padding: 10px; color: #3b4151; background-color: #fff; border-radius: 5px; margin-left: 10px;"><b>/item/{item_id}</b> Delete Menu Item</div>
    </div>
</div>
----
Provides an interface between the microPOS app and supabase.  
Built with FastAPI, pydantic, supabase-py, and uvicorn.  

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
- [ ] authentication
- [ ] ... other things I haven't thought of

## Endpoints (v1)
- [x] Items
    - [x] Get by ID
    - [x] Get All
    - [x] Create
    - [x] Update by ID
    - [x] Delete
- [ ] Categories
    - [ ] Get by ID
    - [ ] Get All
    - [ ] Create
    - [ ] Update by ID
    - [ ] Delete
- [ ] Orders
- [ ] Tables

## Endpoints (v2)
- [ ] Filtering
- [ ] Joins