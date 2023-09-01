import uvicorn
from fastapi import APIRouter, FastAPI

from auth.router import auth_router
from value.router import value_router

app = FastAPI(title="service_for_imported_csv_data")

# create the instance for the routes
main_api_router = APIRouter()

# set routers to the app instance
main_api_router.include_router(auth_router)
main_api_router.include_router(value_router)

app.include_router(main_api_router)

if __name__ == '__main__':
    # run app on the host and port
    uvicorn.run(app, port=8000)
