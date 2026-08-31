import uvicorn

# Start the application server
if __name__ == "__main__":
    uvicorn.run("app:hyaup_app", reload=True)