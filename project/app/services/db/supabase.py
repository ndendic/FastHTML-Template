
import os

from supabase import create_client, AClient
from dotenv import load_dotenv

load_dotenv()

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
service_role: str = os.getenv("SUPABASE_SERVICE_KEY")
supabase: AClient = create_client(url,key)
supabase_admin: AClient = create_client(url,service_role)

# print(supabase_admin.auth.admin.list_users())
# print(supabase_admin.auth.admin.update_user_by_id())
# response = supabase_admin.table("contactmodel").select("*").execute()
# print(response)
