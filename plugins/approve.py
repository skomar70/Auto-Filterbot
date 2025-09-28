pymongo import MongoClient
from info import ADMINS, VERIFY_LINK, MONGO_URI, DATABASE("Cluster0")

# ==========================
# MongoDB Collections
# ==========================
client = MongoClient(MONGO_URI)
db = client.get_database(গগগ)

users = db["users"]
files = db["files"]
settings = db["settings"]

# ==========================
# Utils
# ==========================
def get_shortlink(user_id=None, file_id=None):
    """
    Fetch verify link from DB and append user_id/file_id if provided
    """
    cfg = settings.find_one({"_id": "links"})
    base_url = cfg["verify_link"] if cfg and "verify_link" in cfg else VERIFY_LINK
    if user_id and file_id:
        return f"{base_url}?uid={user_id}&fid={file_id}"
    return base_url

def earn_money_button(user_id=None, file_id=None):
    """
    Create inline keyboard button for earning money
    """            
