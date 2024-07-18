import tkinter as tk


def main(new_site_window: tk.Toplevel, root: tk.Tk, label: tk.Label) -> None:
    import os

    import pandas as pd
    import requests

    alpha_two_code = os.environ.get("ALPHA_TWO_CODE")
    web_pages = os.environ.get("WEB_PAGES")
    country = os.environ.get("COUNTRY")
    state = os.environ.get("STATE")
    site = os.environ.get("SITE")
    domains = os.environ.get("DOMAINS")
    access_token = os.environ.get("ACCESS_TOKEN")

    # Define the Directus URLs
    base_url = "http://directus.dbgi.org"
    collection_url = base_url + "/items/University"

    # Create a session object for making requests
    session = requests.Session()

    # Create template dataframe to reserve labels
    raw_data = {
        "University_name": site,
        "status": "Active",
        "country": country,
        "alpha_two": alpha_two_code,
        "web_pages": web_pages,
        "state": state,
        "domains": domains,
    }

    template = pd.DataFrame(
        [raw_data for _ in range(1)],
        columns=["University_name", "status", "country", "alpha_two", "web_pages", "state", "domains"],
    )

    record = template.to_json(orient="records")

    headers = {"Content-Type": "application/json"}

    # Add the site to the database
    session.headers.update({"Authorization": f"Bearer {access_token}"})
    response = session.post(url=collection_url, headers=headers, data=record)
    if response.status_code == 200:
        new_site_window.destroy()
        root.destroy()

    elif response.status_code == 400:
        label.config(text="Site already entered in the database.", foreground="red")
