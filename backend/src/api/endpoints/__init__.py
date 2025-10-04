from .users import router as users_router
from .groups import router as groups_router
from .sports import router as sports_router
from .teams import router as teams_router

__all__ = ["users_router", "groups_router", "sports_router", "teams_router"]