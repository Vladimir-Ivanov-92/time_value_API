import uvicorn
from fastapi import APIRouter, FastAPI, Depends

from auth.base_config import auth_backend, fastapi_users
from auth.models import User
from auth.schemas import UserRead, UserCreate

app = FastAPI(title="service_for_imported_csv_data")

# create the instance for the routes
main_api_router = APIRouter()

# set routers to the app instance
main_api_router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

main_api_router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(main_api_router)

current_user = fastapi_users.current_user()


@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.username}"


@app.get("/unprotected-route")
def protected_route():
    return f"Hello, anonym"


if __name__ == '__main__':
    # run app on the host and port
    uvicorn.run(app, port=8000)
