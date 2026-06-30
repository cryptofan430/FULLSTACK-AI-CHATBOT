import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()


class GPT:
    def __init__(self):
        self.client = InferenceClient(
            api_key=os.getenv("HF_TOKEN")
        )
        self.model = os.getenv("MODEL_ID")

    def query(self, prompt: str):
        try:
            response = self.client.text_generation(
                prompt,
                model=self.model,
                max_new_tokens=100,
            )

            print("RESPONSE:", response)
            return response

        except Exception as e:
            print("ERROR:", repr(e))
            return None


if __name__ == "__main__":
    GPT().query("Explain artificial intelligence in simple terms")