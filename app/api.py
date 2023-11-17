from typing import List

from fastapi import APIRouter, Depends

from app.schemas import *

router = APIRouter()


@router.get("/arcnet/classify_cutout/", tags=['AR Cutout Classification'])
async def classify_cutout(classification_request: ARCutoutClassificationInput = Depends()) -> ARCutoutClassificationResult:
    r"""
    Classify a cutout generated from a magnetogram at the given date and location as URL parameters.
    """
    classification_result = ARCutoutClassificationResult(time=classification_request.time,
                                                         hgs_latitude=classification_request.hgs_latitude,
                                                         hgs_longitude=classification_request.hgs_longitude,
                                                         hale_class='alpha',
                                                         mcintosh_class='Fck')
    return classification_result


@router.post("/arcnet/classify_cutout/", tags=['AR Cutout Classification'])
async def classify_cutout(req: ARCutoutClassificationInput) -> ARCutoutClassificationResult:
    r"""
    Classify an AR cutout generated from a magnetogram at the given date and location as json data.
    """
    classification_result = ARCutoutClassificationResult(time=req.time, hgs_latitude=req.hgs_latitude,
                                                          hgs_longitude=req.hgs_longitude, hale_class='alpha',
                                                          mcintosh_class='Fck')
    return classification_result


@router.get("/arcnet/full_disk_detection", tags=['Full disk AR Detection'])
async def full_disk_detection(detection_request: ARDetectionInput = Depends()) -> List[ARDetection]:
    r"""
    Detect and classify all ARs in a magnetogram at the given date as a URL parameter.
    """
    detection_result = ARDetection.parse_obj({"bbox": {"bottom_left": {"latitude": -70, "longitude": 10},
                                             "top_right": {"latitude": -70, "longitude": 10}},
                                    "hale_class": "alpha-beta", "mcintosh_class": "Fck"})
    return [detection_result]


@router.post("/arcnet/full_disk_detection", tags=['Full disk AR Detection'])
async def full_disk_detection(detection_request: ARDetectionInput) -> List[ARDetection]:
    r"""
    Detect and classify all ARs in a magnetogram at the given date as  json data.
    """
    detection_result = ARDetection.parse_obj({"bbox": {"bottom_left": {"latitude": -70, "longitude": 10},
                                             "top_right": {"latitude": -70, "longitude": 10}},
                                    "hale_class": "alpha-beta", "mcintosh_class": "Fck"})
    return [detection_result]