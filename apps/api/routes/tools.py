from __future__ import annotations

from fastapi import APIRouter

from core.tools.registry import tool_registry

router = APIRouter(tags=["tools"])


@router.get("/tools")
async def list_tools():
    return {"tools": tool_registry.list_tools()}
