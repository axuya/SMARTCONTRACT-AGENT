from fastapi import FastAPI

from app.api.routes import router as api_router
from app.config import get_settings
from app.logging_config import configure_logging


settings = get_settings()
configure_logging(settings.log_level)

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
)
app.include_router(api_router)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {
        "status": "ok",
        "service": settings.app_name,
        "environment": settings.app_env,
    }
