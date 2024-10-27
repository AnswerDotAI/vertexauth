import os
from operator import itemgetter
from anthropic import AnthropicVertex
from .core import load_vertex_vals as _lvv

def get_anthropic_client(p:str) -> AnthropicVertex:
    d = _lvv(p)
    (gauth_proj_id, gauth_creds, region) = itemgetter('project_id','SAKF_path','region')(d)
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = gauth_creds
    os.environ["GOOGLE_CLOUD_PROJECT"]           = gauth_proj_id
    return AnthropicVertex(region=region, project_id=gauth_proj_id)
