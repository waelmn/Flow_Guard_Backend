from fastapi import APIRouter

router = APIRouter()

# TODO: implement inspection endpoint
@router.post("/inspect")
async def inspect():
    return {"message": "Inspection endpoint — coming soon"}