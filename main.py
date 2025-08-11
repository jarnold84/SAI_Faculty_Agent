
from fastapi import FastAPI
from api import register_routes
import uvicorn

app = FastAPI(
    title="Scraping Agent #1", 
    version="0.1.0",
    description="University Music Faculty Directory Scraper"
)

# Register API routes
register_routes(app)

@app.get("/")
def home():
    return {"message": "Scraping Agent #1 - Ready for university faculty directory extraction"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "version": "0.1.0"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
