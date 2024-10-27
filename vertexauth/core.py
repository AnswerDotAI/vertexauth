import json, hashlib
from pathlib import Path

def load_vertex_vals(p:str):
    """
    p: path to a superkey
    Returns: dict with keys {project_id, SAKF_path, region}
    """
    try:
        proj_id = project_id_from_SAKF(p)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        raise Exception(f"Failed to read JSON from {p}: {e}")
    else:
        d = json.loads(Path(p).read_text())
        region = d['region']
        return dict(project_id=proj_id, SAKF_path=p, region=region)

def save_vertex_vals(project_id, SAKF_path, region) -> str:
    "Returns path to saved superkey"
    loaded_proj_id = project_id_from_SAKF(SAKF_path)
    if project_id != loaded_proj_id:
        raise Exception(f"service access key file has an embedded project id {loaded_proj_id} which does not match the project_id {project_id} you are trying to save. This access key is not obviously compatible with this project")
    d = json.loads(Path(SAKF_path).read_text())
    d["region"]=region
    path = _save_dict(d)
    return path
    

def _save_dict(d:dict) -> str:
    """saves dictionary in managed path"""
    s = json.dumps(d)
    md5h = hashlib.md5(s.encode()).hexdigest()
    path = Path.home() / ".config" / "vertexauth" / md5h / "superkey.json"
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(s)
    path.chmod(0o600)
    return str(path)
    
def project_id_from_SAKF(path_SAKF:str):
    try:
        d = json.loads(Path(path_SAKF).read_text())
    except (json.JSONDecodeError, FileNotFoundError) as e:
        raise Exception(f"Failed to read JSON from {path_SAKF}: {e}")
    else:
        return d['project_id']

