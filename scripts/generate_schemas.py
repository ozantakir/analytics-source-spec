import glob
import json
import os
from google import genai

# Gemini Client Başlatma
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

os.makedirs("output/schemas", exist_ok=True)
os.makedirs("output/mappings", exist_ok=True)

spec_files = glob.glob("specs/*.md")

for spec_path in spec_files:
    filename = os.path.basename(spec_path).replace(".md", "")
    mock_path = f"mock_data/{filename}.json"

    with open(spec_path, "r", encoding="utf-8") as f:
        spec_content = f.read()

    mock_content = ""
    if os.path.exists(mock_path):
        with open(mock_path, "r", encoding="utf-8") as f:
            mock_content = f.read()

    prompt = f"""
    Sen bir Analytics Schema Architect'sin.
    Aşağıdaki Spec Markdown ve Mock Response JSON verilerini incele:

    SPEC DOKÜMANI:
    {spec_content}

    MOCK DATA:
    {mock_content}

    Lütfen iki adet GEÇERLİ JSON nesnesi üret. Yanıtını tam olarak şu JSON formatında ver:
    {{
      "schema": {{ ...draft-07 json schema... }},
      "mapping": {{ ...parameter mappings and destinations... }}
    }}
    Sadece geçerli JSON çıktısı ver, markdown kod bloğu dışında metin ekleme.
    """

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
    )

    clean_text = (
        response.text.strip().removeprefix("```json").removesuffix("```").strip()
    )
    result = json.loads(clean_text)

    # Event adını dosyaya isim olarak ver
    schema_filename = (
        filename.replace("_analytics", "").replace("_spec", "") + ".schema.json"
    )
    mapping_filename = (
        filename.replace("_analytics", "").replace("_spec", "") + ".mapping.json"
    )

    with open(
        f"output/schemas/{schema_filename}", "w", encoding="utf-8"
    ) as f:
        json.dump(result["schema"], f, indent=2)

    with open(
        f"output/mappings/{mapping_filename}", "w", encoding="utf-8"
    ) as f:
        json.dump(result["mapping"], f, indent=2)

print("Tüm şemalar Gemini ile otomatik olarak üretildi!")