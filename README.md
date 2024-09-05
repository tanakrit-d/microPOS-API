<div align="center">
  <img src="assets/images/app-icon-web.png" width="100">
  <p><strong>microPOS:</strong> Middleware API Layer</p>
</div>

----
<div align="center">
<svg fill="none" viewBox="0 0 600 400" width="600" height="400" xmlns="http://www.w3.org/2000/svg">
  <foreignObject width="100%" height="100%">
    <div xmlns="http://www.w3.org/1999/xhtml">
      <style>
        .container {
          width: 600px;
          margin: 20px auto;
        }
        .title {
          font-family: sans-serif;
          font-size: 24px;
          color: #3b4151;
        }
        .api-route {
          display: flex;
          align-items: center;
          margin-bottom: 10px;
          border-radius: 5px;
          border-color: #fff;
          border-style: solid;
          padding: 5px;
        }
        .method {
          width: 80px;
          text-align: center;
          padding: 10px;
          border-radius: 5px;
          color: white;
          font-weight: bold;
        }
        .api-route.get {
          display: flex;
          align-items: center;
          margin-bottom: 10px;
          border-radius: 4px;
          border: 1px;
          border-color: #61affe;
          border-style: solid;
          padding: 5px;
        }
        .method.get {
          background-color: #61affe;
        }
        .api-route.post {
          display: flex;
          align-items: center;
          margin-bottom: 10px;
          border-radius: 4px;
          border: 1px;
          border-color: #49cc90;
          border-style: solid;
          padding: 5px;
        }
        .method.post {
          background-color: #49cc90;
        }
        .api-route.patch {
          display: flex;
          align-items: center;
          margin-bottom: 10px;
          border-radius: 4px;
          border: 1px;
          border-color: #50e3c2;
          border-style: solid;
          padding: 5px;
        }
        .method.patch {
          background-color: #50e3c2;
        }
        .api-route.delete {
          display: flex;
          align-items: center;
          margin-bottom: 10px;
          border-radius: 4px;
          border: 1px;
          border-color: #f93e3e;
          border-style: solid;
          padding: 5px;
        }
        .method.delete {
          background-color: #f93e3e;
        }
        .route {
          flex-grow: 1;
          padding: 10px;
          color: #3b4151;
          background-color: #fff;
          border-radius: 5px;
          margin-left: 10px;
        }
      </style>
      <div class="container">
        <div class="title">Items</div>
        <div class="api-route get">
          <div class="method get">GET</div>
          <div class="route"><b>/item/{item_id}</b> Get Menu Item</div>
        </div>
        <div class="api-route get">
          <div class="method get">GET</div>
          <div class="route"><b>/item/</b> Get All Menu Items</div>
        </div>
        <div class="api-route post">
          <div class="method post">POST</div>
          <div class="route"><b>/item/create</b> Create Menu Item</div>
        </div>
        <div class="api-route patch">
          <div class="method patch">PATCH</div>
          <div class="route"><b>/item/{item_id}</b> Update Menu Item</div>
        </div>
        <div class="api-route delete">
          <div class="method delete">DELETE</div>
          <div class="route"><b>/item/{item_id}</b> Delete Menu Item</div>
        </div>
      </div>
    </div>
  </foreignObject>
</svg>
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