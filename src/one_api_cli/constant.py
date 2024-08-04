import os

# Environment variables
base_url = os.getenv("ONE_API_BASE_URL")
access_token = os.getenv("ONE_API_ACCESS_TOKEN")
section_token = os.getenv("ONE_API_SECTION_TOKEN")


assert base_url, "ONE_API_BASE_URL is not set"
assert access_token or section_token, "Either ONE_API_ACCESS_TOKEN or ONE_API_SECTION_TOKEN must be set"

# Headers
if access_token:
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Authorization": f"Bearer {access_token}",
    }
else:
    section_token = section_token.lstrip("section=").strip("=")
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Cookie": f"section={section_token}=",
    }