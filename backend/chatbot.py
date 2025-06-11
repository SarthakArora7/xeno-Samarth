import faiss
import json
import numpy as np
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import Embeddings
from ibm_watsonx_ai.metanames import EmbedTextParamsMetaNames as EmbedParams
from ibm_watsonx_ai.foundation_models.utils.enums import EmbeddingTypes
import os
from dotenv import load_dotenv
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.foundation_models.utils.enums import ModelTypes

def get_chatbot_response(user_message):

    # Load the FAISS index
    index = faiss.read_index("scheme_index.faiss")

    # Load metadata in same order
    with open("scheme_metadata.json", "r", encoding="utf-8") as f:
        metadata_list = json.load(f)

    load_dotenv()

    API_KEY = os.getenv("IBM_API_KEY")
    PROJECT_ID = os.getenv("PROJECT_ID")
    IBM_URL = os.getenv("IBM_URL")

    embed_params = {
        EmbedParams.TRUNCATE_INPUT_TOKENS: 512,
        EmbedParams.RETURN_OPTIONS: {'input_text': True}
    }

    embedding_client = Embeddings(
        model_id=EmbeddingTypes.IBM_SLATE_30M_ENG,
        params=embed_params,
        credentials=Credentials(api_key=API_KEY, url=IBM_URL),
        project_id=PROJECT_ID
    )

    def embed_query(text):
        result = embedding_client.generate([text])
        return np.array(result['results'][0]['embedding']).astype("float32")

    def search_similar_schemes(query_vector, top_k=1):
        D, I = index.search(query_vector.reshape(1, -1), top_k)
        print("schemes: ")
        # print([metadata_list[i] for i in I[0]])
        return [metadata_list[i] for i in I[0]]

    def build_prompt(user_query, retrieved_schemes):
        schemes_context = ""
        for idx, scheme in enumerate(retrieved_schemes):
            schemes_context += (
                f"Title: {scheme['title']}\n"
                f"Description: {scheme['description']}\n"
                f"Eligibility: {scheme['eligibility']}\n"
                f"Apply Link: {scheme.get('apply_link', 'Not available')}\n\n"
            )

        # Strict prompt for structured output
        prompt = (
            f"User Query: {user_query}\n\n"
            f"Relevant Schemes:\n{schemes_context}\n"
            f"Task: Summarize each scheme STRICTLY in this order:\n"
            f"**Title**: [Name of the scheme]\n"
            f"**Description**: [Brief summary]\n"
            f"**Eligibility**: [Criteria]\n"
            f"**Apply Here**: [Link]\n"
        )
        return prompt

    llm = ModelInference(
        model_id="ibm/granite-13b-instruct-v2",
        params={"decoding_method": "greedy", "max_new_tokens": 900},
        credentials=Credentials(api_key=API_KEY, url=IBM_URL),
        project_id=PROJECT_ID
    )

    def generate_response(prompt):
        response = llm.generate(prompt)
        return response['results'][0]['generated_text']

    user_query = user_message
    query_vector = embed_query(user_query)
    similar_schemes = search_similar_schemes(query_vector)
    prompt = build_prompt(user_query, similar_schemes)
    answer = generate_response(prompt)

    return answer
