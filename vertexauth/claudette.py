import claudette
from .anthropic import get_anthropic_client

def get_claudette_client(vertex_model='claude-3-5-sonnet-v2@20241022', **kwargs) -> claudette.Client:
    """
    Creates a claudette.Client configured with VertexAI info.

    Loads info from args, or env var VERTEXAUTH_SUPERKEY, or file at SUPERKEY_DEFAULT_PATH.
    
    vertex_model : str, valid VertexAI model name (e.g., 'claude-3-5-sonnet-v2@20241022')

    superkey: str, superkey value returned by create_superkey_env_value.
    
    superkey_path: path to a superkey file, whose path was returned by create_superkey_file
    
    Returns: a claudette Client object
    """
    vertex_client = get_anthropic_client(**kwargs)
    return claudette.Client(vertex_model, vertex_client)


