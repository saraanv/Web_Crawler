import os

from dotenv import load_dotenv
from huggingface_hub import InferenceClient


load_dotenv()


client = InferenceClient(
    token=os.getenv("HF_TOKEN")
)


response = client.text_generation(
    "آدرس بیمارستان میلاد کجاست؟",
    model="mistralai/Mistral-7B-Instruct-v0.3",
    max_new_tokens=100
)


print(response)