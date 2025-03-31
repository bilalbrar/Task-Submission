from fastapi import APIRouter, Request, Body
from app.core.logging import logger
from app.services.model_service import get_model_service
from app.api.schemas import PredictionResponse

router = APIRouter()

@router.post("/predict", tags=["predictions"], response_model=PredictionResponse)
async def predict_endpoint(
    request: Request,
    body: dict = Body({
        "sentences": [
            "This product is good.",
            "The story was terrible",
            "The toy car was okay"
        ]
    })
):
    """
    Predict sentiment for a list of sentences.
    """
    import time
    sentences = body.get("sentences", [])
    # If there are no sentences, return response without processing time
    if not sentences:
        logger.info(f"Received empty input")
        return {"predictions": []}
    
    start_time = time.time()
    logger.info(f"Received API call with sentences: {sentences}")
    model_service = get_model_service(request)
    logger.info(f"Using model service instance: {id(model_service)}")
    try:
        predictions = model_service.predict(sentences)
    except Exception as e:
        logger.error(f"Prediction failed: {str(e)}")
        raise RuntimeError(f"Prediction failed: {str(e)}")
    
    processing_time_ms = (time.time() - start_time) * 1000
    logger.info(f"Predictions: {predictions}, Processing time: {processing_time_ms:.2f}ms")
    
    return PredictionResponse(
        predictions=predictions,
        processing_time_ms=processing_time_ms
    )