# VertexAuth

This is a package to streamline the process of accessing AI models served by Google's Vertex AI.

You probably wish you could just lay hands on a single API key value, like with other APIs. Me too!

Alas, afaict, the closest you can get to this with Google Vertex AI is to generate a "Service Account Key File", a json file. And even once you have this, you need to supply it along with other coordinated pieces of information to use the API.

Once you have that file, this library will let you save it with the other information at a single path, and provide convenience functions to create a valid `AnthropicVertex` object for a claudette `Client` object, for accessing Anthropic models easily.

First, create a vertexauth "superkey"

``` python
import vertexauth
superkey_path vertexauth.save_vertex_vals('/path/to/your/service_auth_key_file.json','us-east5')
```

Then later, use it to create a claudette client object

``` python
import claudette
import vertexauth.claudette

claudette_client = vertexauth.claudette.get_claudette_client(superkey_path,'claude-3-5-sonnet-v2@20241022')
cl_chat = claudette.Chat(cli=claudette_client)
cl_chat("Hi, there!")
```

Or you can use it to initialize an AnthropicVertex client object, or to load the values directly:

``` python
import vertexauth, vertexauth.claudette, vertexauth.anthropic
vals = vertexauth.load_vertex_vals(superkey_path) # vals has values needed for auth
anthropic_client = vertexauth.anthropic.get_anthropic_client(superkey_path)
```


## But how do I get this blessed Service Account Key File from Google

It's rough. Here's approximately what you need to do in the Google Cloud console:

- Select a project
- Go to APIs & Services
- Go to Enabled APIs and Services
- Select "Vertex AI API" from the list and ensure that it is Enabled"
- Within that panel, select "Quotas and System Limits"
    - In the filter control, enter the property name "Online prediction requests per base model per minute per region per base_model" to find that row.
    - Scope to a particular `region` (e.g., "us-east5") and  and `base_model` (e.g., "anthropic-claude-3-5-sonnet-v2")
    - Use "Edit Quota" to ensure that you have a non-zero quote for it
- Also, within that panel, select "Credentials"
    - Click "+ Create Credentials"
    - Select "Service Account" 
    - Enter a name like "vertexaiserviceaccount" etc for the account, 
    - For permissions, give it the "Vertex AI Service Agent" role.
    - Go to keys, select "Add key" and select "JSON"


