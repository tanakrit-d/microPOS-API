import os

import uvicorn

if __name__ == "__main__":
    environment = os.getenv("ENVIRONMENT", "local")  # Default to 'local' if not set
    uvicorn.run(
        "src.app:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="debug",
    )
