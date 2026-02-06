import os
import json
import msal
import sys
from dotenv import load_dotenv

# Search for .env in the current folder and the parent folder
load_dotenv() # checks current folder
load_dotenv("../.env") # checks root folder

CLIENT_ID = os.getenv("AZURE_CLIENT_ID")
TENANT_ID = os.getenv("AZURE_TENANT_ID")

# TRY THIS: Changing authority to 'common' can sometimes bypass tenant-level 
# blocks for user-delegated permissions if the app is configured correctly.
AUTHORITY = "https://login.microsoftonline.com/common"

# Scopes required
SCOPES = ["Mail.Read", "Mail.ReadWrite"]

def get_token_interactively():
    if not CLIENT_ID:
        print(f"ERROR: AZURE_CLIENT_ID missing from .env")
        return

    # PublicClientApplication for Device Flow
    app = msal.PublicClientApplication(
        CLIENT_ID, 
        authority=AUTHORITY
    )
    
    print("Initiating login flow...")
    # Attempting to initiate flow
    flow = app.initiate_device_flow(scopes=SCOPES)
    
    if "user_code" not in flow:
        print("ERROR: Could not start device flow.")
        print(f"Details: {flow.get('error_description', 'No error description provided.')}")
        # If 'common' fails, try the specific tenant one last time
        print("Retrying with specific Tenant ID...")
        app = msal.PublicClientApplication(CLIENT_ID, authority=f"https://login.microsoftonline.com/{TENANT_ID}")
        flow = app.initiate_device_flow(scopes=SCOPES)
        if "user_code" not in flow:
            return

    print("\n" + "="*50)
    print(f"ACTION REQUIRED")
    print(f"1. Go to: {flow['verification_uri']}")
    print(f"2. Enter code: {flow['user_code']}")
    print("="*50 + "\n")
    print("Waiting for authentication...")
    
    result = app.acquire_token_by_device_flow(flow)
    
    if "access_token" in result:
        with open("token.json", "w") as f:
            json.dump(result, f, indent=4)
        print("\nSUCCESS: 'token.json' has been created.")
    else:
        # If you see 'AADSTS65001' here, it definitely needs Admin Consent.
        print(f"\nLOGIN FAILED: {result.get('error_description')}")
        print("\nNote: If the error mentions 'Admin Consent', you MUST ask your IT admin ")
        print("to click 'Grant Admin Consent' in the Azure Portal for this App ID.")

if __name__ == "__main__":
    get_token_interactively()