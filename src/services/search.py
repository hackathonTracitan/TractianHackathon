import http.client
import json

CONN = http.client.HTTPSConnection("google.serper.dev")
HEADERS = {
  'X-API-KEY': 'ce34436514015496ffd5664d978e68c8b8302efb',
  'Content-Type': 'application/json'
}

def get_links(result_dict : dict) -> list:
    links = []

    for result in result_dict["organic"]:
        links.append(result["link"])

    return links

def do_query(query : str) -> list:
  payload = json.dumps({
    "q": query,
    "location": "Brazil",
    "gl": "br",
    "hl": "pt-br"
  })

  CONN.request("POST", "/search", payload, HEADERS)

  query_result = json.loads(CONN.getresponse().read().decode("utf-8"))

  return get_links(query_result)