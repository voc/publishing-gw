from pydantic import BaseModel


class BaseEvent(BaseModel):
    guid: str
    slug: str
    title: str
    date: str


class Video(BaseModel):
    filename: str


class EventSummary(BaseEvent):
    video: Video


class Conference(BaseModel):
    id: str
    title: str
    events: list[EventSummary]

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": "37c3",
                "title": "37C3: Unlocked",
                "events": [
                    {
                        "guid": "8f2618e2-d5d9-521c-96ec-f40e807dd5af",
                        "slug": "37c3-58019-nsu-watch-aufklren-einmischen-der-jahresrckblick-2023",
                        "title": "NSU-Watch: Aufklären & Einmischen. Der Jahresrückblick 2023.",
                        "date": "2023-12-28T19:00:00+01:00",
                        "video": {
                            "filename": "37c3-58019-deu-NSU-Watch_Aufklaeren_Einmischen_Der_Jahresrueckblick_2023_hd.mp4"
                        },
                    },
                    {
                        "guid": "df5ca65a-e3d6-42ae-9805-9bc02821ada4",
                        "slug": "37c3-11784-lass_mal_das_innere_eines_neuronalen_netzes_ansehen",
                        "title": "Lass mal das Innere eines Neuronalen Netzes ansehen!",
                        "date": "2023-12-27T21:10:00+01:00",
                        "video": {
                            "filename": "37c3-11784-deu-Lass_mal_das_Innere_eines_Neuronalen_Netzes_ansehen.mp4"
                        },
                    },
                ],
            }
        }
    }


class Recording(BaseModel):
    size: int
    length: int
    mime_type: str
    language: str
    filename: str
    state: str
    folder: str
    high_quality: bool
    width: int
    height: int
    updated_at: str
    recording_url: str
    url: str


class DetailedEvent(BaseEvent):
    subtitle: str | None
    link: str
    description: str
    original_language: str
    persons: list[str]
    tags: list[str]
    view_count: int
    promoted: bool
    release_date: str
    updated_at: str
    length: int
    duration: int
    thumb_url: str
    poster_url: str
    timeline_url: str
    thumbnails_url: str
    frontend_link: str
    url: str
    related: list[str]
    recordings: list[Recording]

    model_config = {
        "json_schema_extra": {
            "example": {
                "guid": "8f2618e2-d5d9-521c-96ec-f40e807dd5af",
                "title": "NSU-Watch: Aufklären & Einmischen. Der Jahresrückblick 2023.",
                "subtitle": None,
                "slug": "37c3-58019-nsu-watch-aufklren-einmischen-der-jahresrckblick-2023",
                "link": "https://events.ccc.de/congress/2023/hub/event/nsu-watch-aufklren-einmischen-der-jahresrckblick-2023/",
                "description": "Wir blicken auf ein Jahr voller rechter, rassistischer und antisemitischer Kampagnen zurück. Der Diskurs um Migration und Flucht wird mit zunehmender Selbstverständlichkeit als ein Diskurs der Abwehr und des Ausschlusses der „Anderen“ geführt. Dies drückt sich in immer neuen Gesetzesverschärfungen bis hin zur Forderung nach einer vollständigen Abschaffung des Grundrechtes auf Asyl aus. Und auch in anderen Bereichen der Politik wird der Ruf nach autoritären „Lösungen“ für tatsächliche oder vermeintliche Probleme lauter. Nur vor diesem gesellschaftlichen Hintergrund sind die Wahlerfolge der AfD in Hessen und Bayern zu verstehen.\n\nFür uns ist klar: Unter solchen gesellschaftlichen Bedingungen wächst die Gefahr rechten Terrors. Die Zahl der antisemitischen, rassistischen und rechten Angriffe steigt weiterhin, denn Rechte Täter*innen können sich als diejenigen verstehen, die einen vermeintlichen „Volkswillen“ in die Tat umsetzen. Sie finden vermehrt die Ermöglichungsstrukturen, die sie für ihre Taten benötigen – in rechten Organisationen ebenso wie im Netz oder im direkten sozialen Umfeld.\n\nWir wollen im Podcast auf das Jahr 2023 zurückschauen und ausloten, wo wir im Kampf gegen rechten Terror stehen. Was sind unsere Möglichkeiten, zu informieren und zu intervenieren? Wir müssen von Staat und Gesellschaft Aufklärung und Konsequenzen einfordern, die Arbeit von Polizei, Justiz und Parlamenten kritisch beobachten, Verharmlosung und Entpolitisierung entgegentreten, solidarisch sein und Betroffenen in ihren Kämpfen um Anerkennung und Gerechtigkeit beiseite stehen. Dafür scheinen die Räume enger und weniger zu werden. Was können wir 2024 gemeinsam erreichen?",
                "original_language": "deu",
                "persons": ["Caro Keller (NSU-Watch)"],
                "tags": ["37c3", "58019", "2023", ""],
                "view_count": 158,
                "promoted": False,
                "date": "2023-12-28T19:00:00.000+01:00",
                "release_date": "2024-03-22T00:00:00.000+01:00",
                "updated_at": "2024-11-09T16:15:01.826+01:00",
                "length": 2577,
                "duration": 2577,
                "thumb_url": "https://static.media.ccc.de/media/congress/2023/58019-8f2618e2-d5d9-521c-96ec-f40e807dd5af.jpg",
                "poster_url": "https://static.media.ccc.de/media/congress/2023/58019-8f2618e2-d5d9-521c-96ec-f40e807dd5af_preview.jpg",
                "timeline_url": "https://static.media.ccc.de/media/congress/2023/58019-8f2618e2-d5d9-521c-96ec-f40e807dd5af.timeline.jpg",
                "thumbnails_url": "https://static.media.ccc.de/media/congress/2023/58019-8f2618e2-d5d9-521c-96ec-f40e807dd5af.thumbnails.vtt",
                "frontend_link": "https://media.ccc.de/v/37c3-58019-nsu-watch-aufklren-einmischen-der-jahresrckblick-2023",
                "url": "https://media.ccc.de/public/events/8f2618e2-d5d9-521c-96ec-f40e807dd5af",
                "related": [],
                "recordings": [
                    {
                        "size": 366,
                        "length": 2577,
                        "mime_type": "video/webm",
                        "language": "deu",
                        "filename": "37c3-58019-deu-NSU-Watch_Aufklaeren_Einmischen_Der_Jahresrueckblick_2023_webm-hd.webm",
                        "state": "new",
                        "folder": "webm-hd",
                        "high_quality": True,
                        "width": 1920,
                        "height": 1080,
                        "updated_at": "2024-03-22T20:23:06.323+01:00",
                        "recording_url": "https://cdn.media.ccc.de/congress/2023/webm-hd/37c3-58019-deu-NSU-Watch_Aufklaeren_Einmischen_Der_Jahresrueckblick_2023_webm-hd.webm",
                        "url": "https://media.ccc.de/public/recordings/76552",
                    },
                    {
                        "size": 117,
                        "length": 2577,
                        "mime_type": "video/webm",
                        "language": "deu",
                        "filename": "37c3-58019-deu-NSU-Watch_Aufklaeren_Einmischen_Der_Jahresrueckblick_2023_webm-sd.webm",
                        "state": "new",
                        "folder": "webm-sd",
                        "high_quality": False,
                        "width": 720,
                        "height": 576,
                        "updated_at": "2024-03-22T17:44:20.892+01:00",
                        "recording_url": "https://cdn.media.ccc.de/congress/2023/webm-sd/37c3-58019-deu-NSU-Watch_Aufklaeren_Einmischen_Der_Jahresrueckblick_2023_webm-sd.webm",
                        "url": "https://media.ccc.de/public/recordings/76522",
                    },
                    {
                        "size": 137,
                        "length": 2577,
                        "mime_type": "video/mp4",
                        "language": "deu",
                        "filename": "37c3-58019-deu-NSU-Watch_Aufklaeren_Einmischen_Der_Jahresrueckblick_2023_sd.mp4",
                        "state": "new",
                        "folder": "h264-sd",
                        "high_quality": False,
                        "width": 720,
                        "height": 576,
                        "updated_at": "2024-03-22T16:43:56.214+01:00",
                        "recording_url": "https://cdn.media.ccc.de/congress/2023/h264-sd/37c3-58019-deu-NSU-Watch_Aufklaeren_Einmischen_Der_Jahresrueckblick_2023_sd.mp4",
                        "url": "https://media.ccc.de/public/recordings/76505",
                    },
                    {
                        "size": 39,
                        "length": 2577,
                        "mime_type": "audio/mpeg",
                        "language": "deu",
                        "filename": "37c3-58019-deu-NSU-Watch_Aufklaeren_Einmischen_Der_Jahresrueckblick_2023_mp3.mp3",
                        "state": "new",
                        "folder": "mp3",
                        "high_quality": False,
                        "width": 0,
                        "height": 0,
                        "updated_at": "2024-03-22T16:41:43.216+01:00",
                        "recording_url": "https://cdn.media.ccc.de/congress/2023/mp3/37c3-58019-deu-NSU-Watch_Aufklaeren_Einmischen_Der_Jahresrueckblick_2023_mp3.mp3",
                        "url": "https://media.ccc.de/public/recordings/76504",
                    },
                    {
                        "size": 28,
                        "length": 2577,
                        "mime_type": "audio/opus",
                        "language": "deu",
                        "filename": "37c3-58019-deu-NSU-Watch_Aufklaeren_Einmischen_Der_Jahresrueckblick_2023_opus.opus",
                        "state": "new",
                        "folder": "opus",
                        "high_quality": False,
                        "width": 0,
                        "height": 0,
                        "updated_at": "2024-03-22T16:41:35.315+01:00",
                        "recording_url": "https://cdn.media.ccc.de/congress/2023/opus/37c3-58019-deu-NSU-Watch_Aufklaeren_Einmischen_Der_Jahresrueckblick_2023_opus.opus",
                        "url": "https://media.ccc.de/public/recordings/76503",
                    },
                    {
                        "size": 536,
                        "length": 2577,
                        "mime_type": "video/mp4",
                        "language": "deu",
                        "filename": "37c3-58019-deu-NSU-Watch_Aufklaeren_Einmischen_Der_Jahresrueckblick_2023_hd.mp4",
                        "state": "new",
                        "folder": "h264-hd",
                        "high_quality": True,
                        "width": 1920,
                        "height": 1080,
                        "updated_at": "2024-03-22T16:40:05.437+01:00",
                        "recording_url": "https://cdn.media.ccc.de/congress/2023/h264-hd/37c3-58019-deu-NSU-Watch_Aufklaeren_Einmischen_Der_Jahresrueckblick_2023_hd.mp4",
                        "url": "https://media.ccc.de/public/recordings/76502",
                    },
                ],
            }
        }
    }
