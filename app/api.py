from typing import List

from fastapi import APIRouter, Depends

from app.classify import classify, detect_ars
from app.schemas import *

router = APIRouter()


@router.get("/arcnet/classify_cutout/", tags=['AR Cutout Classification'])
async def classify_cutout(classification_request: ARCutoutClassificationInput = Depends()) -> ARCutoutClassificationResult:
    r"""
    Classify a cutout generated from a magnetogram at the given date and location as URL parameters.
    """
    classification = classify(time=classification_request.time, hgs_latitude=classification_request.hgs_latitude,
                              hgs_longitude=classification_request.hgs_longitude)
    classification_result = ARCutoutClassificationResult.model_validate(classification)
    return classification_result


@router.post("/arcnet/classify_cutout/", tags=['AR Cutout Classification'])
async def classify_cutout(classification_request: ARCutoutClassificationInput) -> ARCutoutClassificationResult:
    r"""
    Classify an AR cutout generated from a magnetogram at the given date and location as json data.
    """
    classification = classify(time=classification_request.time, hgs_latitude=classification_request.hgs_latitude,
                              hgs_longitude=classification_request.hgs_longitude)
    classification_result = ARCutoutClassificationResult.model_validate(classification)
    return classification_result


@router.get("/arcnet/full_disk_detection", tags=['Full disk AR Detection'])
async def full_disk_detection(detection_request: ARDetectionInput = Depends()) -> List[ARDetection]:
    r"""
    Detect and classify all ARs in a magnetogram at the given date as a URL parameter.
    """
    detections = detect_ars(detection_request.time)
    detection_result = [ARDetection.model_validate(d) for d in detections]
    return detection_result


@router.post("/arcnet/full_disk_detection", tags=['Full disk AR Detection'])
async def full_disk_detection(detection_request: ARDetectionInput) -> List[ARDetection]:
    r"""
    Detect and classify all ARs in a magnetogram at the given date as  json data.
    """
    detections = detect_ars(detection_request.time)
    detection_result = [ARDetection.model_validate(d) for d in detections]
    return detection_result