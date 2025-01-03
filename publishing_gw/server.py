import os
from fastapi.encoders import jsonable_encoder
import jwt
import pydantic
import uvicorn
import pathlib

from fastapi import (
    Body,
    Depends,
    FastAPI,
    HTTPException,
    Path,
    UploadFile,
    File,
    Form,
    Header,
)
from fastapi.responses import JSONResponse, RedirectResponse
from typing import Optional
from pydantic import BaseModel, TypeAdapter

from publishing_gw import cdn, voctoweb

from publishing_gw.config import config
from publishing_gw.model import Conference, DetailedEvent

app = FastAPI(
    title="c3voc Publishing Gateway",
    description="simplify publishing of auxiliary content like slides, subtitles, and other addional metadata to the c3voc infrastructure",
    version="0.2.0",
)


def Error(message=None, status_code=400, detail=None):
    return JSONResponse(
        status_code=status_code,
        content={"errors": [{"message": message or detail or "unknown error"}]},
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
) -> Conference:
    result = voctoweb.graphql(
        """query Conference($slug: ID!){
    	 conference(id: $slug) {
    		id
    		title
    		events:lectures{nodes{guid,slug,title,date,video:videoPreferred{filename}}}
    	}
    }""",
        slug=conference,
    )["conference"]

    if result is None:
        raise HTTPException(status_code=404, detail="Conference not found")

    result["events"] = result.get("events", {}).get("nodes", [])
    result["events"] = [event for event in result["events"] if event is not None] # api returns null in some cases at the moment

    return Conference.model_validate(result)


@app.get(
    "/api/{conference}/events/{guid}",
    summary="Get event/lecture/item metadata needed for publishing from voctoweb/schedule etc.",
)
async def get_event(
    conference: str = Path(example="37c3"),
    guid: str = Path(example="b64fa58b-6f1c-45ef-8dd1-c09947f8a455"),
) -> DetailedEvent:
    res = voctoweb.get(f"/public/events/{guid}")
    return TypeAdapter(DetailedEvent).validate_python(res)


@app.post(
    "/api/{conference}/events/{guid}",
    summary="Create or update event metadata, compatible with existing voctoweb private API",
)
async def upsert_event(
    conference: str, guid: str, token: str = Depends(token_required)
):

    # ... (Adapt the request logic for FastAPI)

    return Error(status_code=501, detail="Not implemented yet")


@app.patch(
    "/api/{conference}/events/{guid}",
    summary="Update event metadata, compatible with existing voctoweb private API",
)
async def patch_event(conference: str, guid: str, token: str = Depends(token_required)):
    #
    # ... (Adapt the request logic for FastAPI)
    return Error(status_code=501, detail="Not implemented yet")


@app.post(
    "/api/recordings",
    summary="Create or update recording metadata, compatible with existing voctoweb private API",
    tags=["legacy"],
)
async def recordings(payload: dict = Form(...), token: str = Depends(token_required)):
    # ... (Adapt the rest of the recordings function for FastAPI)
    return Error(status_code=501, detail="Not implemented yet")


class FileMeta(BaseModel):
    language: str
    mime_type: str


class FileUpsertBody(BaseModel):
    recording: FileMeta
    # other: any

    class Config:
        arbitrary_types_allowed = True


@app.put(
    "/api/{conference}/events/{guid}/file",
    summary="Add (or update) a file to an event e.g. lecture slides, subtitles etc.",
)
async def create_or_update_file(
    conference: str = Path(examples=["37c3"]),
    guid: str = Path(examples=["b64fa58b-6f1c-45ef-8dd1-c09947f8a455"]),
    file: UploadFile = File(),  # example="b64fa58b-6f1c-45ef-8dd1-c09947f8a455.deu.vtt"),
    meta: str = Body(..., media_type="application/json"),
    token: str = Depends(token_required),
):
    if not file.filename.endswith(".vtt"):
        raise HTTPException(
            status_code=400, detail="At the moment, only VTT files are supported"
        )

    try:
        model = FileUpsertBody.model_validate_json(json_data=meta)
    except pydantic.ValidationError as e:
        raise HTTPException(detail=jsonable_encoder(e.errors()), status_code=422) from e

    # get legacy_id from voctoweb
    event = voctoweb.get(f"/public/events/{guid}")

    # we need to get the confernce_path and the legacy_id from the event
    # "thumbnails_url": "https://static.media.ccc.de/media/congress/2024/66-59022846-b130-581e-a89f-ecf6e7e43940.thumbnails.vtt",
    path_base = pathlib.Path(
        event.get("thumbnails_url")
        .replace("https://static.media.ccc.de/media/", "")
        .replace(".thumbnails.vtt", "")
    )
    filename = f"{path_base.name}-{model.recording.language}.vtt"
    # filename = f"{legacy_id}-{guid}-{model.recording.language}.vtt"

    conference_path = path_base.parent

    # upload file to cdn.media.ccc.de
    cdn.upload_file(
        file,
        f"/static.media.ccc.de/{conference_path}/{filename}",
    )

    # add (or update) file to voctoweb
    r = voctoweb.upsert_recording(
        guid,
        {
            "folder": "",
            **model.recording.model_dump(),
            "filename": filename,
            "mime_type": "text/vtt",
            "language": model.recording.language,
            "state": "auto",
        },
    )

    return {"message": "File and data processed"}


def dev():
    run(reload=True, log_level="debug")


def run(reload=False, log_level="info"):
    port = int(os.environ.get("PORT", 5005))
    config = uvicorn.Config(
        app,
        host="::1",
        port=port,
        log_level=log_level,
        reload=reload,
    )
    server = uvicorn.Server(config)
    # TODO
    # setup_logging()
    server.run()


if __name__ == "__main__":
    run()
