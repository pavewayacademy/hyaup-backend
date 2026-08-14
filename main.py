import uvicorn
from config.config import settings

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=settings.APP_PORT, reload=True)