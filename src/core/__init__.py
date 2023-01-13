from typing import Callable, Any


def Depends(dependency: Callable[..., Any] | None) -> Any:
    return next(dependency())
