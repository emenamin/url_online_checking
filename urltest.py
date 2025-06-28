import pandas as pd
import requests

# Load URLs from Excel file
df = pd.read_excel("URLTest.xlsx")  # File must be in the same folder as this script
statuses = []
signup_pages = []

# Common signup paths to test
signup_paths = ["/signup", "/register", "/join", "/create-account"]

# Loop through each URL
for url in df['URL']:
    if not url.startswith("http"):
        url = "https://" + url

    # Check if site is online
    try:
        res = requests.get(url, timeout=5)
        status = "Active" if res.status_code == 200 else f"Error {res.status_code}"
    except Exception:
        status = "Offline"

    statuses.append(status)

    # Check for signup page
    found_signup = False
    if status == "Active":
        for path in signup_paths:
            try:
                test_url = url.rstrip("/") + path
                r = requests.get(test_url, timeout=5)
                if r.status_code == 200:
                    found_signup = True
                    break
            except:
                continue

    signup_pages.append("Yes" if found_signup else "No")

# Save results
df['Status'] = statuses
df['Signup Page'] = signup_pages
df.to_excel("URLTest_result.xlsx", index=False)

print("✅ Done! Check 'URLTest_result.xlsx' for results.")
