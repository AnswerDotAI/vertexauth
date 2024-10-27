# VertexAuth

This is a helper library for accessing Google Vertex AI models

To use it, get a GCloud _Service Account Key File_ (SAKF), then save a default "superkey" file into your `.config` dir, like so:

``` python
from vertexauth import create_superkey_file
path=create_superkey_file(SAKF_path='/path/to/gcloud/service_auth_key_file.json',
                                     region='us-east5',
                                     save_as_default=True)
```

The superkey file is just the SAKF file with region information added.

Then later, you can create a [claudette](https://claudette.answer.ai/) client or [AnthropicVertex](https://docs.anthropic.com/en/api/claude-on-vertex-ai) client object like so:

``` python
from vertexauth import get_anthropic_client, get_claudette_client, load_vertex_vals
from claudette import Chat

# AnthropicVertex
anthropic_client = get_anthropic_client()

# claudette.Client
claudette_client = get_claudette_client()
cl_chat = Chat(cli=claudette_client)
cl_chat("Hi, there!")

# just read the vals
val_dict = load_vertex_vals()
```

These functions also let you pass a path to a specific superkey, instad of loading the default one.

Alternatively, they can read an env var, `VERTEXAUTH_SUPERKEY`, which contains a superkey as a string. This lets you share it and use it like a normal API key. However, it's a bit long -- around 2,500 characters, since it's simply the gzipped, base64-encoded contents of the file. Use `create_superkey_env_value` to create one.

## Huh, what's a Service Account Key File?

Yes it would be easier of course if Google just gave us a single API key value. But they don't.

afaict the closest you can get to this with Google Vertex AI is to generate a "Service Account Key File" (SAKF), a JSON file with embedded credentials. But even once you have this, you need to supply it along with other coordinated pieces of information (like project ID and region) in order to make an API request against a VertexAI model. So it's a bit of a hassle., and that's what this library helps with. That's all.

## But how do I get this blessed Service Account Key File from Google

It's not pretty. Here's approximately what you need to do:

- Go to Google Cloud console
- Select a project
- Go to APIs & Services
- Go to Enabled APIs and Services
- Select "Vertex AI API" from the list and ensure that it is Enabled"
- Within that panel, select "Quotas and System Limits"
    - In the filter control, enter the property name "Online
      prediction requests per base model per minute per region per
      base_model" to find that row.
    - Scope to a particular `region` (e.g., "us-east5") and and
      `base_model` (e.g., "anthropic-claude-3-5-sonnet-v2")
    - Use "Edit Quota" to ensure that you have a non-zero quote for it
- Also, within that same panel, select "Credentials"
    - Click "+ Create Credentials"
    - Select "Service Account" 
    - Enter a name like "vertexaiserviceaccount" etc for the account, 
    - For permissions, give it the "Vertex AI Service Agent" role.
    - Go to keys, select "Add key" and select "JSON"


