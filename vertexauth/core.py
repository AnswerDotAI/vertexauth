import json, hashlib
from pathlib import Path

def load_vertex_vals(superkey_path:str) -> dict:
    """
    Loads values for authenticating with Vertex AI.
    
    superkey_path: path to a superkey, which is a file saved by save_vertex_vals
    Returns: dict with keys {project_id, SAKF_path, region}
    """
    try:
        d = json.loads(Path(superkey_path).read_text())
    except (json.JSONDecodeError, FileNotFoundError) as e:
        raise Exception(f"Failed to read JSON from {superkey_path}: {e}")
    if 'region' not in d or 'type' not in d or d['type'] != 'service_account':
        raise Exception(f"""The superkey path {superkey_path} does not contain both the expected key 'region' and the expected k/v 'type':'service_cconut'. This is not a superkey file saved by save_vertex_vals. Aborting""")
    return dict(project_id=d['project_id'],
                    SAKF_path=superkey_path,
                    region=d['region'])

def save_vertex_vals(SAKF_path, region) -> str:
    """Saves Vertex AI auth to a superkey file, returning its path.

    SAKF_path : str
        path to a GCloud Service Account Key File, associated with a
        GCloud project, which permissions to access the model of
        interest in the specified region. region: region

    region : str
        region where the project has permissions to access the model
    """
    try:
        d = json.loads(Path(SAKF_path).read_text())
    except (json.JSONDecodeError, FileNotFoundError) as e:
        raise Exception(f"Failed to read JSON from {path_SAKF}: {e}")
    if 'type' not in d or d['type'] != 'service_account':
        raise Exception(f"The SAKF_path {SAKF_path} is to a JSON file which does not contain a k/v pair indicating it is a service account file. Aborting")
    d["region"]=region
    path = _save_dict(d)
    return path
    

def _save_dict(d:dict) -> str:
    """Saves dictionary in managed location, returning its path"""
    s = json.dumps(d)
    md5h = hashlib.md5(s.encode()).hexdigest()
    path = Path.home() / ".config" / "vertexauth" / md5h / "superkey.json"
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(s)
    path.chmod(0o600)
    return str(path)
    
