import tkinter as tk


def main(new_site_window: tk.Toplevel, root: tk.Tk, label: tk.Label) -> None:
    import os

    import pandas as pd
    import requests

    # Load variables
    alpha_two_code = os.environ.get("ALPHA_TWO_CODE")
    web_pages = os.environ.get("WEB_PAGES")
    country = os.environ.get("COUNTRY")
    state = os.environ.get("STATE")
    site = os.environ.get("SITE")
    domains = os.environ.get("DOMAINS")
    access_token = os.environ.get("ACCESS_TOKEN")

    # Define the Directus URLs
    base_url = "https://emi-collection.unifr.ch/directus"
    collection_url = base_url + "/items/Universities"

    # Create a session object for making requests
    session = requests.Session()

    # Create template dataframe to reserve labels
    raw_data = {
        "university_name": site,
        "status": "active",
        "country": country,
        "alpha_two": alpha_two_code,
        "web_pages": web_pages,
        "state": state,
        "domains": domains,
    }

    # Create a dataframe template to store the values
    template = pd.DataFrame(
        [raw_data for _ in range(1)],
        columns=["university_name", "status", "country", "alpha_two", "web_pages", "state", "domains"],
    )

    # Transform the dataframe to a json
    record = template.to_json(orient="records")

    # Create request headers
    headers = {"Content-Type": "application/json"}

    # Add the site to the database
    session.headers.update({"Authorization": f"Bearer {access_token}"})
    response = session.post(url=collection_url, headers=headers, data=record)
    if response.status_code == 200:
        # If request is a success, close the application
        new_site_window.destroy()
        root.destroy()

    elif response.status_code == 400:
        # If request fails with code 400, informs user that the site is already in the database
        label.config(
            text="Site already entered in the database and usable in the project. You can add another site.",
            foreground="red",
        )

    else:
        label.config(text=f"The request failed: {response.json()['errors'][0]['message']}.", foreground="red")
