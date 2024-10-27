import claudette
from .anthropic import get_anthropic_client

def get_claudette_client(p:str,model:str) -> claudette.Client:
    vertex_client = get_anthropic_client(p)
    return claudette.Client(model, vertex_client)
