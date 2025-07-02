from contextlib import asynccontextmanager

from fastapi import FastAPI
from rich import panel, print
from scalar_fastapi import get_scalar_api_reference

from app.database.session import create_db_tables


from app.api.router import router

@asynccontextmanager
async def lifespan_handler(app: FastAPI):
    print(panel.Panel("Server started...", border_style="green"))
    await create_db_tables()
    yield
    print(panel.Panel("...stopped!", border_style="red"))


app = FastAPI(lifespan=lifespan_handler)

app.include_router(router)

# Scalar API Documentation
@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API",
    )
