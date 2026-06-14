import os

try:
    from dotenv import load_dotenv
except ImportError:
    def load_dotenv():
        return False

try:
    from azure.identity import DefaultAzureCredential
    from azure.ai.projects import AIProjectClient
except ImportError:
    DefaultAzureCredential = None
    AIProjectClient = None


load_dotenv()

ENDPOINT = os.getenv(
    "AZURE_AI_PROJECT_ENDPOINT",
    "https://ai-interview-coach-resource.services.ai.azure.com/api/projects/ai-interview-coach"
)

DEPLOYMENT = os.getenv(
    "AZURE_OPENAI_DEPLOYMENT",
    "gpt-5-mini"
)


class LazyAzureOpenAIClient:
    def __init__(self):
        self._client = None

    def _get_client(self):
        if DefaultAzureCredential is None or AIProjectClient is None:
            raise RuntimeError(
                "Azure SDK packages are not installed. "
                "Install requirements.txt or use Demo Mode fallbacks."
            )

        if self._client is None:
            project = AIProjectClient(
                endpoint=ENDPOINT,
                credential=DefaultAzureCredential()
            )
            self._client = project.get_openai_client()

        return self._client

    @property
    def responses(self):
        return self._get_client().responses


client = LazyAzureOpenAIClient()
