def get_api_headers(token=""):
    if token:
        return {
            "Authorization": f"Token {token}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
    return {"Accept": "application/json", "Content-Type": "application/json"}
