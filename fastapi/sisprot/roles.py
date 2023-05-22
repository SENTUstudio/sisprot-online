from typing import List
from fastapi import Depends, HTTPException
from sisprot.auth import get_current_user
from sisprot.models import UserAuth


class RoleChecker:
    def __init__(self, allowed_roles: List):
        self.allowed_roles = allowed_roles

    def __call__(self, user: UserAuth = Depends(get_current_user)):
        if user.rol not in self.allowed_roles:
            raise HTTPException(status_code=403, detail="Operation not permitted")


admin_allowed = RoleChecker(['admin'])