import http.client
import json

conn = http.client.HTTPSConnection("google.serper.dev")

query = "samsung inc"

payload = json.dumps({
  "q": query,
  "location": "Brazil",
  "gl": "br",
  "hl": "pt-br"
})

headers = {
  'X-API-KEY': 'ce34436514015496ffd5664d978e68c8b8302efb',
  'Content-Type': 'application/json'
}

conn.request("POST", "/search", payload, headers)
res = conn.getresponse()
data = res.read()

new_dict = data.decode("utf-8")

print(type(new_dict))