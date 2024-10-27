import claudette
from .anthropic import get_anthropic_client

def get_claudette_client(superkey_path:str,vertex_model:str) -> claudette.Client:
    """Create a Claudette client using Vertex AI credentials.

    Parameters
    ----------
    superkey_path : str
        Path to credentials file saved from vertexauth.save_vertex_vals
    vertex_model : str
        Valid Vertex AI model name (e.g., 'claude-3-5-sonnet-v2@20241022')
    """
    vertex_client = get_anthropic_client(superkey_path)
    return claudette.Client(vertex_model, vertex_client)
