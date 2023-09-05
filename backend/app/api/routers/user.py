from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from app.api.schemas.user import UserRequestSchema, UserResponseSchema
from app.repository import UserRepository


user_router = APIRouter(prefix="/users", tags=["Users"])


@user_router.get("/", response_model=list[UserResponseSchema])
async def get_users(User: UserRepository):
    return await User.get_all_users()


@user_router.post("/", response_model=UserResponseSchema)
async def create_user(data: UserRequestSchema, User: UserRepository):
    return await User.create_one(data)


@user_router.delete(
    "/{user_id}",
    summary="Delete user by ID",
)
async def delete_user_cv(data: UserRequestSchema, User: UserRepository):
    deleted_cv = await User.delete_user(data)

    if deleted_cv:
        return JSONResponse(
            content={"message": "User deleted successfully"},
            status_code=status.HTTP_200_OK,
        )

    return JSONResponse(
        content={"message": "There is no user with such email"},
        status_code=status.HTTP_404_NOT_FOUND,
    )
