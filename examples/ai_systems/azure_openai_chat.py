"""Optional Azure OpenAI v1 Responses SDK example with Microsoft Entra ID.

python -m pip install openai azure-identity
python -m examples.ai_systems.azure_openai_chat
"""
import os
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from openai import OpenAI


def main():
    with DefaultAzureCredential() as credential:
        token_provider = get_bearer_token_provider(credential, "https://ai.azure.com/.default")
        with OpenAI(base_url=os.environ["AZURE_OPENAI_V1_BASE_URL"], api_key=token_provider,
                    timeout=45.0, max_retries=0) as client:
            result = client.responses.create(
                model=os.environ["AZURE_OPENAI_DEPLOYMENT"],
                input="Explain idempotency in two sentences for a Python learner.",
                store=False,
            )
            print(result.output_text)


if __name__ == "__main__":
    main()
