import os
import json
import glob
from google import genai
from google.genai import types

# 1. Gemini Client Kurulumu
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# Klasör Yolları
SPEC_DIR = "specs"
MOCK_DIR = "mock_data"
OUTPUT_SCHEMA_DIR = "output/schemas"
OUTPUT_MAPPING_DIR = "output/mappings"

os.makedirs(OUTPUT_SCHEMA_DIR, exist_ok=True)
os.makedirs(OUTPUT_MAPPING_DIR, exist_ok=True)

# 2. Spec ve Mock Dosyalarını Okuma
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

    # 3. Yöntem 2 Destinasyon Kırılımlı Gemini Prompt'u
    prompt = f"""
    Sen kıdemli bir Analytics ve Schema mimarısın. 
    Aşağıda verilen Markdown spesifikasyonunu ve Örnek Mock JSON verisini analiz et.
    
    --- SPEC DOKÜMANI ---
    {spec_content}
    
    --- MOCK JSON VERİSİ ---
    {mock_content}
    
    Senden 2 adet JSON nesnesi üretmeni istiyorum:
    1. "schema": Standard Draft-07 JSON Schema (Tüm event parametrelerini, tiplerini ve zorunluluk durumlarını içerir).
    2. "mapping": Target/Destination odaklı parametre eşleme JSON'ı. 
       - "destinations" dizisinde hedef provider'lar yer almalıdır (Örn: "FIREBASE", "ADJUST", "SGTM").
       - "destination_payloads" nesnesi altında HER BİR destination için hangi parametrenin hangi hedef key'e eşleneceğini yaz. 
       - İlgili provider'a gönderilmeyen parametreleri o provider'ın payload'ına ekleme.
    
    YAZILACAK ÇIKTI FORMATI:
    Yalnızca geçerli bir JSON objesi döndür. Açıklama metni veya markdown kod blokları (```json) EKLEME. Format tam olarak şu şekilde olmalıdır:
    
    {{
      "schema": {{
        "$schema": "[http://json-schema.org/draft-07/schema#](http://json-schema.org/draft-07/schema#)",
        "title": "AddToCartClicked",
        "type": "object",
        "properties": {{
          "productId": {{ "type": "string" }},
          "price": {{ "type": "number" }},
          "quantity": {{ "type": "integer" }}
        }},
        "required": ["productId", "price", "quantity"]
      }},
      "mapping": {{
        "event_name": "add_to_cart_clicked",
        "destinations": ["FIREBASE", "ADJUST", "SGTM"],
        "destination_payloads": {{
          "FIREBASE": {{
            "item_id": "productId",
            "value": "price",
            "quantity": "quantity"
          }},
          "ADJUST": {{
            "revenue": "price"
          }},
          "SGTM": {{
            "product_id": "productId",
            "price": "price",
            "quantity": "quantity"
          }}
        }}
      }}
    }}
    """

    # 4. Gemini API Çağrısı
    response = client.models.generate_content(
        model='gemini-3.6-flash',
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json"
        )
    )

    # 5. Sonuçları Kaydetme
    result = json.loads(response.text)
    
    with open(os.path.join(OUTPUT_SCHEMA_DIR, f"{filename}.schema.json"), "w", encoding="utf-8") as f:
        json.dump(result["schema"], f, indent=2)

    with open(os.path.join(OUTPUT_MAPPING_DIR, f"{filename}.mapping.json"), "w", encoding="utf-8") as f:
        json.dump(result["mapping"], f, indent=2)

    print(f"Başarıyla üretildi: {filename}")