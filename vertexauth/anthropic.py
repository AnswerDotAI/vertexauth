import os
from operator import itemgetter
from anthropic import AnthropicVertex
from .core import load_vertex_vals as _lvv

def get_anthropic_client(**kwargs) -> AnthropicVertex:
    """
    Creates an AnthropicVertex client configured with VertexAI info.

    Loads info from args, or env var VERTEXAUTH_SUPERKEY, or file at SUPERKEY_DEFAULT_PATH.
    
    superkey: str, superkey value returned by create_superkey_env_value.
    
    superkey_path: path to a superkey file, whose path was returned by create_superkey_file
    
    Returns: AnthropicVertex object
    """
    d = _lvv(**kwargs)
    (gauth_proj_id, gauth_creds, region) = itemgetter('project_id','SAKF_path','region')(d)
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = gauth_creds
    os.environ["GOOGLE_CLOUD_PROJECT"]           = gauth_proj_id
    return AnthropicVertex(region=region, project_id=gauth_proj_id)
