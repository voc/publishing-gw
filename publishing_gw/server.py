import os
import json
import jwt

from fastapi import (
    Depends,
    FastAPI,
    HTTPException,
    Path,
    UploadFile,
    File,
    Form,
    Header,
)
from typing import Optional
from fastapi.responses import RedirectResponse

from publishing_gw import voctoweb

# import config

app = FastAPI(
    title="c3voc Publishing Gateway",
    description="simplify publishing of ancillary content like slides, subtitles, and other addional metadata to the c3voc infrastructure",
)


async def token_required(authorization: Optional[str] = Header(None)):
    api_key = None

    if authorization and authorization.startswith("Bearer "):
        # TODO add support for Bearer token via sso.c3voc.de
        token = jwt.decode(authorization.split(" ")[1], verify=True)
        return token


    if authorization and authorization.startswith("Token "):
        api_key = authorization.split(" ")[1]
    if authorization and authorization.startswith("token="):
        api_key = authorization.split("=")[1]

    if not api_key:
        raise HTTPException(status_code=400, detail="Please provide an API key")
    if api_key not in config.allowed_keys:
        raise HTTPException(status_code=403, detail="The provided API key is not valid")
    return api_key


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse("/docs", status_code=302)


@app.get(
    "/api/{conference}",
    summary="Get conference/series/project metadata needed for publishing from voctoweb/c3tracker etc.",
)
async def get_conference(
    conference: str = Path(example="37c3"),
):  # Header(default="37c3")):
    return voctoweb.graphql(
        """query Conference($slug: ID!){
    	 conference(id: $slug) {
    		id
    		title
    	}
    }""",
        slug=conference,
    )["conference"]


@app.get(
    "/api/{conference}/events/{guid}",
    summary="Get event/lecture/item metadata needed for publishing from voctoweb/schedule etc.",
)
async def get_event(conference: str, guid: str, token: str = Depends(token_required)):
    return voctoweb.get(f"/public/events/{guid}")


@app.post(
    "/api/{conference}/events/{guid}",
    summary="Create or update event metadata, compatible with existing voctoweb private API",
)
async def upsert_event(
    conference: str, guid: str, token: str = Depends(token_required)
):

    # ... (Adapt the request logic for FastAPI)
    pass


@app.patch(
    "/api/{conference}/events/{guid}",
    summary="Update event metadata, compatible with existing voctoweb private API",
)
async def patch_event(conference: str, guid: str, token: str = Depends(token_required)):

    # ... (Adapt the request logic for FastAPI)
    pass


@app.post(
    "/api/recordings",
    summary="Create or update recording metadata, compatible with existing voctoweb private API",
    tags=["legacy"],
)
async def recordings(payload: dict = Form(...), token: str = Depends(token_required)):
    # ... (Adapt the rest of the recordings function for FastAPI)
    pass


@app.put(
    "/api/{conference}/events/{guid}/file",
    summary="Add or update a file to an event e.g. lecture slides, subtitles etc.",
)
async def create_or_update_file(
    conference: str = Path(example="37c3"),
    guid: str = Path(example="b64fa58b-6f1c-45ef-8dd1-c09947f8a455"),
    file: UploadFile = File(...),
    json_data: str = Form(...),
    token: str = Depends(token_required),
):
    try:
        data = json.loads(json_data)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON data")

    # File handling
    # ... (Adapt file handling logic for FastAPI)

    return {"message": "File and data processed"}


async def dev():
    import uvicorn

    config = uvicorn.Config(
        "publishing_gw.server:run",
        port=int(os.environ.get("PORT", 5005)),
        reload=True,
        log_level="info",
    )
    server = uvicorn.Server(config)
    await server.run()


async def run():
    import uvicorn

    config = uvicorn.Config(
        app,
        port=int(os.environ.get("PORT", 5005)),
        log_level="info",
    )
    server = uvicorn.Server(config)
    await server.run()


if __name__ == "__main__":
    run()
