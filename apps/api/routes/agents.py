from __future__ import annotations

from fastapi import APIRouter

from core.agents.registry import agent_registry

router = APIRouter(tags=["agents"])


@router.get("/agents")
async def list_agents():
    return {"agents": agent_registry.list_agents()}
