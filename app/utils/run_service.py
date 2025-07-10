# from app.services.scraping_service import scrape_top_30_chennai
from app.services.chroma_service import ChromaService
# from app.utils.json_to_txt import convert_json_to_txt

# scrape_top_30_chennai()

chroma = ChromaService()
chroma.build_vector_store()

# convert_json_to_txt()