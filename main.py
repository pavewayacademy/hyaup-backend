import uvicorn
from config.config import settings

# Start the application server
if __name__ == "__main__":
    uvicorn.run("app:hyaup_app", host="0.0.0.0", port=settings.APP_PORT, reload=True)