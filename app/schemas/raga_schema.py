from pydantic import BaseModel

class RagaSchema(BaseModel):
    raga_number: int
    raga_name_latin: str
    raga_name_devanagari: str
    classification: str
    swaras_latin: str
    swaras_devanagari: str
    colour_rgb: str

    class Config:
        from_attributes = True