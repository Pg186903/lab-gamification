from supabase import create_client
from os import getenv

SUPABASE_URL = getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = getenv("SUPABASE_ANON_KEY")

supabase_client = create_client(
    SUPABASE_URL,
    SUPABASE_ANON_KEY,
)
