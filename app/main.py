import logging

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.templating import Jinja2Templates
from fluent import handler as fluent_handler
from prometheus_fastapi_instrumentator import Instrumentator

from app.controllers import user_controller
from app.db.database import init_db, init_data

app = FastAPI(title="Financial Exchange API", version="1.0.0", description="API for managing financial transactions")
templates = Jinja2Templates(directory="templates")


# Custom OpenAPI function to add a description, version, etc.
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="API",
        version="1.0.0",
        description="This is a custom OpenAPI schema",
        routes=app.routes
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

Instrumentator().instrument(app).expose(app)

logger = logging.getLogger('fluent.test')
fluent_handler = fluent_handler.FluentHandler('app.follow', host='host.docker.internal', port=24224)
formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
fluent_handler.setFormatter(formatter)
logger.addHandler(fluent_handler)
logger.setLevel(logging.INFO)

# Include the user router
app.include_router(user_controller.router, prefix="/users", tags=["users"])


@app.on_event("startup")
def on_startup():
    init_db()
    # init_data()
