# Role Based Access permissions

ROLE_PERMISSIONS = {
    "Admin": ["upload", "view", "delete"],
    "Financial Analyst": ["upload"],
    "Auditor": ["view"],
    "Client": ["view"]
}

def has_permission(role: str, action: str):
    permissions = ROLE_PERMISSIONS.get(role, [])
    return action in permissions