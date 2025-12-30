from supabase import create_client
from os import getenv
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = getenv("SUPABASE_ANON_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

EMAIL = "dmanas@gmail.com"
PASSWORD = "Find1234"

# res = supabase.auth.sign_up({
#     "email": EMAIL,
#     "password": PASSWORD,
# })

# print("SIGNED UP USER ID:", res.user.id)

res = supabase.auth.sign_in_with_password({
    "email": EMAIL,
    "password": PASSWORD,
})

print("USER ID:", res.user.id)
print("ACCESS TOKEN:", res.session.access_token)