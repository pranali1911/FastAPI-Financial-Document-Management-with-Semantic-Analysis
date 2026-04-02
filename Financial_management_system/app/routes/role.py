# store user roles and permissions (for simplicity, we will use in-memory storage here)
from fastapi import APIRouter
from utils.rbac import ROLE_PERMISSIONS


router = APIRouter()

# temporary storage (later DB)
user_roles = {}

# assign role api

@router.post("/users/assign-role")
def assign_role(user_id: int, role: str):
    user_roles[user_id] = role
    return {"message": f"Role {role} assigned to user {user_id}"}

# get user role api
@router.get("/users/{user_id}/roles")
def get_role(user_id: int):
    return {"role": user_roles.get(user_id, "No role")}

@router.post("/roles/create")
def create_role(role: str):
    return {"message": f"Role {role} created"}


@router.get("/users/{user_id}/permissions")
def get_permissions(user_id: int):
    role = user_roles.get(user_id)
    permissions = ROLE_PERMISSIONS.get(role, [])

    return {
        "role": role,
        "permissions": permissions
    }