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

    def search_similar_schemes(query_vector, top_k=3):
        D, I = index.search(query_vector.reshape(1, -1), top_k)
        return [metadata_list[i] for i in I[0]]

    def build_prompt(user_query, retrieved_schemes):
        schemes_context = []
        for idx, scheme in enumerate(retrieved_schemes, start=1):
            schemes_context.append((
                f"Scheme {idx}:\n"
                f"Title: {scheme['title']}\n"
                f"Description: {scheme['description']}\n"
                f"Eligibility: {scheme['eligibility']}\n"
                f"Apply Link: {scheme.get('apply_link', 'Not available')}\n\n"
            ))

        prompt = (
        f"User Query: {user_query}\n\n"
        f"The following are relevant government schemes. ONLY USE THESE SCHEMES to answer:\n\n"
        f"{''.join(schemes_context)}"
        f"Task: DO NOT use any external knowledge. DO NOT generate your own examples.\n"
        f"ONLY summarize the schemes above. There are {len(retrieved_schemes)} schemes.\n"
        f"For EACH scheme, use the following format:\n\n"
        f"Title: [Name of the scheme]\n"
        f"Description: [Brief summary of the description above. Do not invent anything.]\n"
        f"Eligibility: [Criteria from above. Do not guess.]\n"
        f"Apply Here: [Link]\n\n"
        f"List all {len(retrieved_schemes)} schemes."
        )

        return prompt

    llm = ModelInference(
        model_id="ibm/granite-13b-instruct-v2",
        params={"decoding_method": "sample", "max_new_tokens": 900, "temperature": 0.3},
        credentials=Credentials(api_key=API_KEY, url=IBM_URL),
        project_id=PROJECT_ID
    )

    def clean_llm_output(text):
        # Remove lines that include task instructions
        keywords = [
            "Your task", 
            "DO NOT use", 
            "ONLY summarize", 
            "Provide summaries", 
            "List all", 
            "Instructions"
        ]
        lines = text.splitlines()
        cleaned = "\n\n".join(line for line in lines if all(k not in line for k in keywords))
        return cleaned.strip()


    def generate_response(prompt):
        response = llm.generate(prompt)
        return response['results'][0]['generated_text']

    user_query = user_message
    query_vector = embed_query(user_query)
    similar_schemes = search_similar_schemes(query_vector)
    prompt = build_prompt(user_query, similar_schemes)
    answer = generate_response(prompt)
    cleaned_answer = clean_llm_output(answer)

    return cleaned_answer
