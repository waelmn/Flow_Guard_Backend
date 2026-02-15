from fastapi import APIRouter

router = APIRouter()

# TODO: implement reports endpoint
@router.get("/reports")
async def get_reports():
    return {"message": "Reports endpoint — coming soon"}