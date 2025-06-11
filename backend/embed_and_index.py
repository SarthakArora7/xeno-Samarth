import json
import os
from dotenv import load_dotenv
import faiss
import numpy as np
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import Embeddings
from ibm_watsonx_ai.metanames import EmbedTextParamsMetaNames as EmbedParams
from ibm_watsonx_ai.foundation_models.utils.enums import EmbeddingTypes

# Load .env variables
load_dotenv()

API_KEY = os.getenv("IBM_API_KEY")
PROJECT_ID = os.getenv("PROJECT_ID")
IBM_URL = os.getenv("IBM_URL")

if not all([API_KEY, PROJECT_ID, IBM_URL]):
    raise Exception("Please set IBM_API_KEY, PROJECT_ID, and IBM_URL in your .env file")

# Setup embed parameters
embed_params = {
    EmbedParams.TRUNCATE_INPUT_TOKENS: 512,
    EmbedParams.RETURN_OPTIONS: {
        'input_text': True
    }
}

# Initialize embedding client
embedding_client = Embeddings(
    model_id=EmbeddingTypes.IBM_SLATE_30M_ENG,
    params=embed_params,
    credentials=Credentials(api_key=API_KEY, url=IBM_URL),
    project_id=PROJECT_ID
)

def embed_scheme_text(text):
    response = embedding_client.generate([text])
    embedding = response['results'][0]['embedding']
    return embedding

def main():
    with open("dataset_schemes.json", "r", encoding="utf-8") as f:
        schemes = json.load(f)

    embeddings = []
    metadata_list = []

    for idx, scheme in enumerate(schemes):
        combined_text = f"{scheme['title']}. {scheme['description']} Eligibility: {scheme['eligibility']}"
        embedding_vector = embed_scheme_text(combined_text)

        embeddings.append(embedding_vector)
        metadata_list.append(scheme)

        print(f"Embedded scheme {idx+1}/{len(schemes)}: {scheme['title']}")

    embeddings_array = np.array(embeddings).astype("float32")

    dimension = embeddings_array.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings_array)

    # Save index
    faiss.write_index(index, "scheme_index.faiss")
    print("FAISS index saved as 'scheme_index.faiss'")

    # Save metadata
    with open("scheme_metadata.json", "w", encoding="utf-8") as f:
        json.dump(metadata_list, f, ensure_ascii=False, indent=2)
    print("Metadata saved as 'scheme_metadata.json'")

    print(f"Total embeddings generated: {len(embeddings)}")
    print("Sample metadata for first scheme:", metadata_list[0])
    print("Sample embedding vector dimension:", len(embeddings[0]))

if __name__ == "__main__":
    main()
