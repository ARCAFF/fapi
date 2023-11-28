from datetime import datetime

from fastapi import Query
from pydantic import BaseModel, Field


class ARCutoutClassificationInput(BaseModel):
    time: datetime = Field(Query(title='Date time', ge=datetime(2011, 1, 1), le=datetime.now()),
                           example='2022-11-12T13:14:15+00:00')
    hgs_latitude: float = Field(Query(title="Heliographic Latitude", ge=-180, le=180, example=-70))
    hgs_longitude: float = Field(Query(title='Heliographic Latitude', ge=-90, le=90, example=10))


class ARCutoutClassificationResult(BaseModel):
    time: datetime = Field(title='Date time', ge=datetime(2011, 1, 1), le=datetime.now())
    hgs_latitude: float = Field(title="Heliographic Latitude", ge=-180, le=180, example=-70)
    hgs_longitude: float = Field(title='Heliographic Longitude', ge=-90, le=90, example=10)
    hale_class: str = Field(title='Hale Classification', example='alpha-beta')
    mcintosh_class: str = Field(title='McIntosh Classification', example='Fck')


class ARDetectionInput(BaseModel):
    time: datetime = Field(example='2022-11-12T13:14:15+00:00', ge=datetime(2011, 1, 1), le=datetime.now())


class HeliographicStonyhurstCoordinate(BaseModel):
    r"""
    Heliographic Stonyhurst (HGS) Coordinate
    """
    latitude: float = Field(title="Heliographic Latitude", ge=-180, le=180, example=-70)
    longitude: float = Field(title='Heliographic Longitude', ge=-90, le=90, example=10)


class BoundingBox(BaseModel):
    r"""
    Bounding Box
    """
    bottom_left: HeliographicStonyhurstCoordinate
    top_right: HeliographicStonyhurstCoordinate


class ARDetection(BaseModel):
    r"""
    Active Region Detection
    """
    time: datetime = Field(title='Date time', ge=datetime(2011, 1, 1), le=datetime.now())
    bbox: BoundingBox
    hale_class: str = Field(title='Hale Classification', example='alpha-beta')
    mcintosh_class: str = Field(title='McIntosh Classification', example='Fck')