from fastapi import FastAPI

from app.api import router

description = """
# ARCAFF API
Active Region Classification and Flare Forecasting (ARCAFF) API

### ARCNET

Active Region Classification Network (ARCNET) provides an API to AR classifications.
#### AR Cutout Classification

Given a AR magnetogram cutout return the classifications Hale (magnetic) and McInstosh (modified Zurich) classifications.

#### AR Detection

Given a full disk magnetogram return the bounding boxes and classification for each detected AR.

"""

tags_metadata = [
    {
        "name": "AR Cutout Classification",
        "description": "Classify cutouts generated from a magnetogram at the given date and location.",
    },
    {
        "name": "Full disk AR Detection",
        "description": "Detect and classify all AR from a magnetogram for the given date.",
    },
]


app = FastAPI(
    title="ARCNET",
    description=description,
    summary="Active Region Classification and Flare Forecasting (ARCAFF) API",
    version="0.0.1",
    contact={
        "name": "ARCAFF",
        "url": "http://www.arcaff.eu",
    },
    openapi_tags=tags_metadata
)
app.include_router(router, prefix='')
