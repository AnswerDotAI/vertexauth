# VertexAuth

This is a helper library for accessing Google Vertex AI models

To use it, get a Gcloud _Service Account Key File_ (SAKF), then create a vertexauth "superkey" file like so:

``` python
import vertexauth
path=vertexauth.create_superkey_file(SAKF_path='/path/to/gcloud/service_auth_key_file.json',
                                     region='us-east5',
                                     save_as_default=True)
```

This puts the SAKF and region info into a single file in your `.config` dir.

Then later, you can create a claudette client or AnthropicVertex client object like so:

``` python
import vertexauth, vertexauth.anthropic, vertexauth.claudette, claudette

# AnthropicVertex
anthropic_client = vertexauth.anthropic.get_anthropic_client()
# claudette.Client
claudette_client = vertexauth.claudette.get_claudette_client()
cl_chat = claudette.Chat(cli=claudette_client)
cl_chat("Hi, there!")
# just access the vals
val_dict = vertexauth.load_vertex_vals()
```

The main functions also let you pass a superkey path.

Also, they can read an env var, `VERTEXAUTH_SUPERKEY`, which contains a superkey embedded in one string. This lets you share it and use it like a normal API key, except that it will be about 3,000 characters long. Use `create_superkey_env_value` to create such embedded value.

## Huh, what's a Service Account Key File?

You probably wish you could just lay hands on a single API key value, like with other APIs. Me too.

But afaict the closest you can get to this with Google Vertex AI is to generate a "Service Account Key File" (SAKF), a json file with embedded credentials. And even once you have this, you need to supply it along with other coordinated pieces of information (like project ID and region) in order to make an API request against a model. So it's a bit of a hassle., and that's what this helps with.

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
- Also, within that panel, select "Credentials"
    - Click "+ Create Credentials"
    - Select "Service Account" 
    - Enter a name like "vertexaiserviceaccount" etc for the account, 
    - For permissions, give it the "Vertex AI Service Agent" role.
    - Go to keys, select "Add key" and select "JSON"


