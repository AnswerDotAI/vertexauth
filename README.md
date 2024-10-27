# VertexAuth

This is a package to streamline the process of using Vertex AI models served by Google's Vertex AI.

Once you have Service Account Key File, create a vertexauth "superkey".

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

Alternatively, you can use it to initialize an AnthropicVertex client object, or to load the values directly:

``` python
import vertexauth, vertexauth.claudette, vertexauth.anthropic
vals = vertexauth.load_vertex_vals(superkey_path) # vals has values needed for auth
anthropic_client = vertexauth.anthropic.get_anthropic_client(superkey_path)
```

## Huh, what's a Service Account Key File?

Look. You probably wish you could just lay hands on a single API key value, like with other APIs. Me too!

Alas, afaict, the closest you can get to this with Google Vertex AI is to generate a "Service Account Key File" (SAKF), a json file with embedded credentials. And even once you have this, you need to supply it along with other coordinated pieces of information (like project ID and region) in order to make an API request against a model, so it's still a bit of a hassle.

This library is only able to help with that last part, by saving all the information into one file, a "superkey" file. With that file, it helps you create a valid `AnthropicVertex` object for a claudette `Client` object, for accessing Anthropic models easily.

## But how do I get this blessed Service Account Key File from Google

My friends, it's ugly. Here's approximately what you need to do in the Google Cloud console:

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


