from googleapiclient.discovery import build

api_key = "AIzaSyA7AFqujn1LhAEzrM86jnxXXzgXPc3h6as"
cse_id = "c2df58d429fce41b8"  # you must create this in Google Custom Search

def google_search(query):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=query, cx=cse_id).execute()
    for item in res['items']:
        print(item['title'])
        print(item['link'])
        print()

# Example usage
google_search("who is krishna")
