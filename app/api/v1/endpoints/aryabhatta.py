from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.dependencies.database import get_db
from ..services.mapping_service import MappingService
from app.schemas.ab_schema import ProcessWordRequest, CalculateRequest, AddMappingRequest
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

# -----------------------------
# Singleton instance (loads once)
# -----------------------------
_mapping_service_instance = None

def get_mapping_service():
    """
    Returns a cached MappingService instance (Singleton pattern).
    Loads all mappings and colors from DB only on first call.
    """
    global _mapping_service_instance
    if _mapping_service_instance is None:
        _mapping_service_instance = MappingService()
        _mapping_service_instance.load_initial_values_from_db()
        _mapping_service_instance.load_character_colors_from_db()
        logger.info("✅ MappingService initialized and cached!")
    return _mapping_service_instance

# -----------------------------
# Base endpoint
# -----------------------------
@router.get("/")
async def home():
    return {"message": "Varnamala Tokenizer backend is running (Aryabhatta Numeration)."}

# -----------------------------
# Word processing
# -----------------------------
@router.post("/process_sentence")
async def process_word_api(
    request: ProcessWordRequest,
    mapping_service: MappingService = Depends(get_mapping_service)
):
    word_input = request.word
    input_script = request.inputScript

    if not word_input:
        raise HTTPException(status_code=400, detail="No word provided.")
    if " " in word_input:
        raise HTTPException(status_code=400, detail="Input must be a single word. Spaces are not allowed.")
    if len(word_input) > 100:
        raise HTTPException(status_code=400, detail="Input word exceeds 100 character limit.")
    if input_script not in ["latin", "devanagari", "kannada", "telugu", "malayalam"]:
        raise HTTPException(status_code=400, detail="Invalid input script specified.")

    tokens, all_numbers = mapping_service.tokenize_sentence(word_input, input_script)
    return {"tokens": tokens, "all_numbers": all_numbers}

# -----------------------------
# Calculation
# -----------------------------
@router.post("/calculate")
async def calculate_api(
    request: CalculateRequest,
    mapping_service: MappingService = Depends(get_mapping_service)
):
    tokens_data = request.tokens
    operation = request.operation

    if not isinstance(tokens_data, list):
        raise HTTPException(status_code=400, detail="Invalid tokens format. Expected a list.")
    if not operation:
        raise HTTPException(status_code=400, detail="No operation specified.")

    results = mapping_service.calculate_logic(tokens_data, operation)
    return {"operation": operation, "result": results}

# -----------------------------
# Mappings endpoints
# -----------------------------
@router.get("/get_mappings")
async def get_mappings_api(mapping_service: MappingService = Depends(get_mapping_service)):
    try:
        mappings = mapping_service.get_mappings()  # no DB argument needed
        return mappings
    except Exception as e:
        logger.error("Error fetching mappings", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/add_mapping")
async def add_mapping_api(
    request: AddMappingRequest,
    mapping_service: MappingService = Depends(get_mapping_service)
):
    new_latin_char = request.latinChar
    insert_at = request.number
    mapping_type = (request.type or "").strip().lower()
    new_devanagari_char = request.devanagariChar or ""
    new_kannada_char = request.kannadaChar or ""
    new_color_hex = getattr(request, "colorHex", None)

    if mapping_type not in ["consonant", "vowel"]:
        raise HTTPException(status_code=400, detail="Invalid mapping type")

    mapping_service.add_mapping(
        None,  # DB session not needed if service handles DB internally
        new_latin_char,
        insert_at,
        mapping_type,
        new_devanagari_char,
        new_kannada_char,
        new_color_hex
    )

    return {"success": True, "message": "Mapping added successfully."}

# -----------------------------
# Color-related endpoints
# -----------------------------
@router.get("/color_mappings")
async def get_color_mappings_api(mapping_service: MappingService = Depends(get_mapping_service)):
    try:
        rows = mapping_service.get_color_mappings()
        return {"success": True, "data": rows}
    except Exception as e:
        logger.error("Error fetching color mappings", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))



@router.post("/closest_character")
async def closest_character_post(
    payload: dict,
    mapping_service: MappingService = Depends(get_mapping_service)
):
    try:
        r = int(payload.get("r"))
        g = int(payload.get("g"))
        b = int(payload.get("b"))
        # Use the correct method name here:
        closest = mapping_service.closest_character(r, g, b)
        return closest
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))




@router.get("/colors")
async def get_colors_api(mapping_service: MappingService = Depends(get_mapping_service)):
    """
    Fetch all characters and their assigned colors.
    """
    try:
        colors = mapping_service.get_colors()
        return colors
    except Exception as e:
        logger.error("Error fetching colors", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")
