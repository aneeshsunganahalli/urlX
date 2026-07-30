from fastapi import APIRouter

router = APIRouter(tags=["Redirects"])

@router.get("/{short_url}")
async def redirect(short_url: str):
  pass
