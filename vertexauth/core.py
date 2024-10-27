import json, hashlib,gzip,base64, os, shutil
from pathlib import Path

SUPERKEY_ENV_VAR = 'VERTEXAUTH_SUPERKEY'

_superkey_path_root = Path.home() / ".config" / "vertexauth" 
SUPERKEY_DEFAULT_PATH = _superkey_path_root / "default" / "superkey.json"

def load_vertex_vals(superkey:str|None=None,superkey_path:str|None=None) -> dict:
    """
    Loads VertexAI vals from arg, or env var VERTEXAUTH_SUPERKEY, or file at SUPERKEY_DEFAULT_PATH.
    
    superkey: str, superkey value returned by create_superkey_env_value.
    
    superkey_path: path to a superkey file, whose path was returned by create_superkey_file
    
    Returns: dict with {project_id, SAKF_path, region}
    """
    if superkey is not None:              path = _superkey_from_env_value(superkey)
    elif superkey_path is not None:       path = Path(superkey_path)
    elif SUPERKEY_ENV_VAR in os.environ:  path = _superkey_from_env_value(os.getenv(SUPERKEY_ENV_VAR))
    elif SUPERKEY_DEFAULT_PATH.is_file(): path = SUPERKEY_DEFAULT_PATH
    else: raise Exception(f"No env var {SUPERKEY_ENV_VAR} found")
    try: d = json.loads(path.read_text())
    except (json.JSONDecodeError, FileNotFoundError) as e:
        raise Exception(f"Failed to read JSON from {path}: {e}")
    if 'region' not in d or 'type' not in d or d['type'] != 'service_account':
        raise Exception(f"""The superkey path {path} does not contain both the expected key 'region' and the expected k/v 'type':'service_cconut'. This is not a superkey file saved by create_superkey_file. Aborting""")
    return dict(project_id=d['project_id'],
                    SAKF_path=str(path),
                    region=d['region'])


def create_superkey_env_value(SAKF_path, region) -> str:
    """Generates a superkey value, from VertexAI values.

    This value can be saved and loaded from the env var VERTEXAUTH_SUPERKEY

    SAKF_path : str
        path to a GCloud Service Account Key File, associated with a
        GCloud project, which permissions to access the model of
        interest in the specified region. region: region

    region : str
        region where the project has permissions to access the model
    """
    d = _superkey_dict_from_vals(SAKF_path, region)
    p = _save_dict(d)
    return _env_value(p)
    
    

def create_superkey_file(SAKF_path, region, save_as_default=False) -> Path:
    """Saves a Vertex AI auth to a superkey file, returning its path.

    SAKF_path : str
        path to a GCloud Service Account Key File, associated with a
        GCloud project, which permissions to access the model of
        interest in the specified region. region: region

    region : str
        region where the project has permissions to access the model
    """
    d = _superkey_dict_from_vals(SAKF_path, region)
    path = _save_dict(d)
    if save_as_default:
        SUPERKEY_DEFAULT_PATH.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(path,SUPERKEY_DEFAULT_PATH)
        path = SUPERKEY_DEFAULT_PATH
    return path


def _superkey_dict_from_vals(SAKF_path, region) -> dict:
    """Generates a superkey dict from VAI auth vals """
    try:
        d = json.loads(Path(SAKF_path).read_text())
    except (json.JSONDecodeError, FileNotFoundError) as e:
        raise Exception(f"Failed to read JSON from {path_SAKF}: {e}")
    if 'type' not in d or d['type'] != 'service_account':
        raise Exception(f"The SAKF_path {SAKF_path} is to a JSON file which does not contain a k/v pair indicating it is a service account file. Aborting")
    d["region"]=region
    return d


def _save_dict(d:dict) -> Path:
    """Saves dictionary in managed location, returning its path"""
    s = json.dumps(d)
    md5h = hashlib.md5(s.encode()).hexdigest()
    path = _superkey_path_root / md5h / "superkey.json"
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(s)
    path.chmod(0o600)
    return path


def _env_value(superkey_path:Path) -> str:
    "Generates a str value to use for the env var VERTEX_SUPERKEY"
    content = open(str(superkey_path),'r').read()
    compressed = gzip.compress(content.encode())
    return base64.b64encode(compressed).decode()


def _superkey_from_env_value(val) -> Path:
    "Returns a superkey path built from val, an env var val"
    compressed = base64.b64decode(val)
    s = gzip.decompress(compressed).decode()
    d = json.loads(s)
    p = _save_dict(d)
    return p

    
