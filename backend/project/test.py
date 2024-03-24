from msal import ConfidentialClientApplication

app = ConfidentialClientApplication(
    "41f7c599-fe36-4d1b-9aae-8fdda0dadecb",
    authority="https://login.microsoftonline.com/d7811cde-ecef-496c-8f91-a1786241b99c",
    client_credential="VIx8Q~gkjlrbIdbB~rWuYOuPtDg1neDPaZcklbkG")


# initialize result variable to hold the token response
result = None 

# We now check the cache to see
# whether we already have some accounts that the end user already used to sign in before.
accounts = app.get_accounts()
if accounts:
    # If so, you could then somehow display these accounts and let end user choose
    print("Pick the account you want to use to proceed:")
    for a in accounts:
        print(a["username"])
    # Assuming the end user chose this one
    chosen = accounts[0]
    # Now let's try to find a token in cache for this account
    result = app.acquire_token_silent(["User.Read"], account=chosen)

if not result:
    # So no suitable token exists in cache. Let's get a new one from Azure AD.
    result = app.acquire_token_for_client(scopes=["user.read"])
if "access_token" in result:
    print(result["access_token"])  # Yay!
else:
    print(result.get("error"))
    print(result.get("error_description"))
    print(result.get("correlation_id"))  # You may need this when reporting a bug
