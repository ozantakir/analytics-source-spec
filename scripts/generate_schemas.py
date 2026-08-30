import os
import json
import glob
from google import genai
from google.genai import types

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

SPEC_DIR = "specs"
MOCK_DIR = "mock_data"
OUTPUT_SCHEMA_DIR = "output/schemas"
OUTPUT_MAPPING_DIR = "output/mappings"

os.makedirs(OUTPUT_SCHEMA_DIR, exist_ok=True)
os.makedirs(OUTPUT_MAPPING_DIR, exist_ok=True)

spec_files = glob.glob(f"{SPEC_DIR}/*.md")

for spec_path in spec_files:
    filename = os.path.basename(spec_path).replace(".md", "")
    mock_path = os.path.join(MOCK_DIR, f"{filename}.json")
    
    with open(spec_path, "r", encoding="utf-8") as f:
        spec_content = f.read()
        
    mock_content = "{}"
    if os.path.exists(mock_path):
        with open(mock_path, "r", encoding="utf-8") as f:
            mock_content = f.read()

    prompt = f"""
    Sen kıdemli bir Analytics ve Schema mimarısın. 
    Aşağıdaki Markdown spesifikasyonunu ve Örnek Mock JSON verisini analiz et.
    
    --- SPEC DOKÜMANI ---
    {spec_content}
    
    --- MOCK JSON VERİSİ ---
    {mock_content}
    
    Senden 2 adet JSON nesnesi üretmeni istiyorum:
    1. "schema": Standard Draft-07 JSON Schema.
    2. "mapping": Target/Destination odaklı parametre eşleme JSON'ı. 
       - "destinations" dizisinde hedef provider'lar BÜYÜK HARFLERLE yer almalıdır (Örn: ["FIREBASE", "ADJUST", "SGTM"]).
       - "destination_payloads" nesnesi altında HER BİR destination için nesne açılmalı ve parametrelerin hedef key karşılıkları yazılmalıdır.
       - İlgili provider'a gönderilmeyen parametreler o provider'ın payload nesnesine EKLENMEMELİDİR.
    """

    # Kesin format zorlaması için Structured Output Schema
    json_response_schema = {
        "type": "OBJECT",
        "properties": {
            "schema": {
                "type": "OBJECT",
                "description": "Draft-07 JSON Schema definition"
            },
            "mapping": {
                "type": "OBJECT",
                "properties": {
                    "event_name": {"type": "STRING"},
                    "destinations": {
                        "type": "ARRAY",
                        "items": {"type": "STRING"}
                    },
                    "destination_payloads": {
                        "type": "OBJECT",
                        "description": "Target bazlı key-value mapping. Örn: {'FIREBASE': {'item_id': 'productId'}, 'ADJUST': {'revenue': 'price'}}"
                    }
                },
                "required": ["event_name", "destinations", "destination_payloads"]
            }
        },
        "required": ["schema", "mapping"]
    }

    response = client.models.generate_content(
        model='gemini-3.6-flash',
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=json_response_schema
        )
    )

    result = json.loads(response.text)
    
    with open(os.path.join(OUTPUT_SCHEMA_DIR, f"{filename}.schema.json"), "w", encoding="utf-8") as f:
        json.dump(result["schema"], f, indent=2)

    with open(os.path.join(OUTPUT_MAPPING_DIR, f"{filename}.mapping.json"), "w", encoding="utf-8") as f:
        json.dump(result["mapping"], f, indent=2)

    print(f"Başarıyla üretildi: {filename}")