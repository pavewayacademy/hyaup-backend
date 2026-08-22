import uvicorn
from config.config import settings
from app import app


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=settings.APP_PORT, reload=True)


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
