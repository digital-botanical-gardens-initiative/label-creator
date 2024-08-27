# To convert this script into a binary compatible with the OS where the command is executed:
# pyinstaller --onefile --paths=./ --hidden-import=sample_labels_csv --hidden-import=container_labels --hidden-import=csv_labels --hidden-import=new_site label_creator.py

import os
import tkinter as tk
import webbrowser
from tkinter import Event, filedialog, ttk
from typing import Any

import container_labels
import csv_labels
import new_site
import pandas as pd
import requests
import sample_labels
from fuzzywuzzy import process


class MainPage(tk.Frame):
    def __init__(self, parent: tk.Tk, *args: Any, **kwargs: Any):
        """
        Initializes an instance of the class.

        Args:
            parent(tk.Tk): The parent widget or window where this frame will be placed.

        Returns:
            None
        """

        # Create the tk page
        tk.Frame.__init__(self, parent, *args, **kwargs)

        # Send a request to github to know if this version is the las one
        release_url = "https://api.github.com/repos/digital-botanical-gardens-initiative/label-creator/releases/latest"
        session = requests.Session()
        response = session.get(release_url)
        data = response.json()["tag_name"]
        tag = float(str.replace(data, "v", ""))

        # Put white background
        self.configure(bg="white")

        if tag <= 2.0:
            # Create GUI elements for labels
            label_labels = tk.Label(self, text="Create labels", background="white", font=("Helvetica", 16))
            label_labels.pack()

            button_new_labels = tk.Button(
                self,
                text="Generate sample labels",
                width=40,
                font=("Helvetica", 11),
                background="#f0f0f0",
                relief="flat",
                command=self.open_sample_labels,
            )
            button_new_labels.pack()

            button_mobile_container = tk.Button(
                self,
                text="Generate containers labels",
                width=40,
                font=("Helvetica", 11),
                relief="flat",
                background="#f0f0f0",
                command=self.open_container_labels,
            )
            button_mobile_container.pack()

            button_existing = tk.Button(
                self,
                text="Print labels from a CSV",
                width=40,
                font=("Helvetica", 11),
                background="#f0f0f0",
                relief="flat",
                command=self.open_csv_labels,
            )
            button_existing.pack()

            # Create site frame to add a space
            frame_site = tk.Frame(self, background="white")
            frame_site.pack(pady=(70, 10))

            # Create GUI elements to add a new site
            label_new_site = tk.Label(
                frame_site, text="Add a new site to the database", background="white", font=("Helvetica", 16)
            )
            label_new_site.pack()

            button_new_site = tk.Button(
                frame_site,
                text="Add a new site",
                width=40,
                font=("Helvetica", 11),
                background="#f0f0f0",
                relief="flat",
                command=self.open_new_site,
            )
            button_new_site.pack()
        else:
            # Create frame to center the text
            frame_new = tk.Frame(self, background="white")
            frame_new.pack(pady=(100, 10))

            # Create GUI elements to ask user to download the latest version
            label_labels = tk.Label(
                frame_new,
                text="A new version is available, please download it.",
                background="white",
                font=("Helvetica", 16),
            )
            label_labels.pack()

            button_new_labels = tk.Button(
                frame_new,
                text=f"Download new release: {data}",
                width=40,
                background="#f0f0f0",
                relief="flat",
                command=self.download_last_version,
            )
            button_new_labels.pack()

    def open_sample_labels(self) -> None:
        # Create a new Toplevel window for the new labels
        sample_labels_window = tk.Toplevel(root)
        sample_labels_window.title("Generate sample labels")
        sample_labels_window.minsize(600, 650)
        # Launches the corresponding class
        sampleLabels(sample_labels_window, root)

    def open_container_labels(self) -> None:
        # Create a new Toplevel window for the mobile containers
        container_labels_window = tk.Toplevel(root)
        container_labels_window.title("Generate containers labels")
        container_labels_window.minsize(650, 580)
        # Launches the corresponding class
        containerLabels(container_labels_window, root)

    def open_csv_labels(self) -> None:
        # Create a new Toplevel window for the labels from CSV
        csv_labels_window = tk.Toplevel(root)
        csv_labels_window.title("Generate labels from a CSV")
        csv_labels_window.minsize(650, 470)
        # Launches the corresponding class
        csvLabels(csv_labels_window, root)

    def open_new_site(self) -> None:
        # Create a new Toplevel window to add a new site
        new_site_window = tk.Toplevel(root)
        new_site_window.title("Add a new site")
        new_site_window.minsize(550, 540)
        # Launches the corresponding class
        newSite(new_site_window, root)

    # Function that redirects user to the last software version
    def download_last_version(self) -> None:
        url = "https://github.com/digital-botanical-gardens-initiative/label-creator/releases/latest"
        webbrowser.open(url)


# Class to create new labels
class sampleLabels(tk.Frame):
    def __init__(self, sample_labels_window: tk.Toplevel, root: tk.Tk):
        """
        Initializes an instance of the class.

        Args:
            sample_labels_window(tk.Toplevel): The parent widget where this frame will be placed.
            root(tk.Tk): The root window to perform actions on it.

        Returns:
            None
        """

        # Makes tk elements available across functions
        self.sample_labels_window = sample_labels_window
        self.root = root

        # Hide main page
        self.root.withdraw()

        # Associates the close button to a specific action managed by on_exit function
        self.sample_labels_window.protocol("WM_DELETE_WINDOW", self.on_exit)

        # Make background white
        self.sample_labels_window.configure(bg="white")

        # Create variables to store the user entered parameters
        self.username = tk.StringVar(None)
        self.password = tk.StringVar(None)
        self.number = tk.IntVar(None)
        self.project = tk.StringVar(None)
        self.label_size = tk.IntVar(None)

        # Create informations GUI
        self.label_info = tk.Label(
            self.sample_labels_window,
            text="Generates avery L4736, L4732 or L4731 labels",
            background="white",
            font=("Helvetica", 16),
        )
        self.label_info.pack()

        # Create informations GUI
        self.label_info_2 = tk.Label(
            self.sample_labels_window,
            text="and reserves the codes in directus",
            background="white",
            font=("Helvetica", 16),
        )
        self.label_info_2.pack()

        # Create informations frame
        frame_info = tk.Frame(self.sample_labels_window, background="white")
        frame_info.pack(pady=(10, 20))

        # L4736 info
        self.label_l4736 = tk.Label(
            frame_info,
            text="L4736 informations",
            cursor="hand2",
            foreground="blue",
            background="white",
            font=("Helvetica", 11),
        )
        self.label_l4736.grid(row=0, column=0, padx=10)

        # Makes the link clickable
        self.label_l4736.bind("<Button-1>", lambda event: self.open_link(4736, event))

        # L4732 info
        self.label_l4732 = tk.Label(
            frame_info,
            text="L4732 informations",
            cursor="hand2",
            foreground="blue",
            background="white",
            font=("Helvetica", 11),
        )
        self.label_l4732.grid(row=0, column=1, padx=10)

        # Makes the link clickable
        self.label_l4732.bind("<Button-1>", lambda event: self.open_link(4732, event))

        # L4731 info
        self.label_l4731 = tk.Label(
            frame_info,
            text="L4731 Informations",
            cursor="hand2",
            foreground="blue",
            background="white",
            font=("Helvetica", 11),
        )
        self.label_l4731.grid(row=0, column=2, padx=10)

        # Makes the link clickable
        self.label_l4731.bind("<Button-1>", lambda event: self.open_link(4731, event))

        # Create text entry fields
        label_username = tk.Label(
            self.sample_labels_window, text="Directus username:", background="white", font=("Helvetica", 12)
        )
        label_username.pack(pady=(20, 5))
        entry_username = tk.Entry(
            self.sample_labels_window, textvariable=self.username, relief="flat", font=("Helvetica", 11)
        )
        entry_username.pack()

        label_password = tk.Label(
            self.sample_labels_window, text="Directus password:", background="white", font=("Helvetica", 12)
        )
        label_password.pack(pady=(20, 5))
        entry_password = tk.Entry(
            self.sample_labels_window, textvariable=self.password, show="*", relief="flat", font=("Helvetica", 11)
        )
        entry_password.pack()

        # Extract the project names from directus
        collection_url = "https://emi-collection.unifr.ch/directus/items/Projects"
        column = "project_id"
        params = {"sort[]": f"{column}"}
        session = requests.Session()
        response = session.get(collection_url, params=params)
        data = response.json()["data"]
        project_names = [item[column] for item in data]

        # Choose the project
        project_label = tk.Label(
            self.sample_labels_window, text="Choose your project:", background="white", font=("Helvetica", 12)
        )
        project_label.pack(pady=(20, 5))
        dropdown_project = tk.OptionMenu(self.sample_labels_window, self.project, *project_names)
        # Customizing the OptionMenu to appear flat
        dropdown_project.config(font=("Helvetica", 11), bg="#f0f0f0", fg="black", bd=0, highlightthickness=0)
        dropdown_project.pack()
        # Access and customize the drop-down menu
        menu = dropdown_project["menu"]
        menu.configure(
            bg="white", fg="black", activebackground="white", activeforeground="black", font=("Helvetica", 11)
        )

        # Create label to choose label format
        self.label_format = tk.Label(
            self.sample_labels_window, text="Choose the label format:", background="white", font=("Helvetica", 12)
        )
        self.label_format.pack(pady=(20, 5))

        # Frame to hold radio buttons
        radio_frame = tk.Frame(self.sample_labels_window, bg="white")
        radio_frame.pack()

        # Set to medium size by default
        self.label_size.set(2)

        # Create radio buttons for label sizes
        radio_big = tk.Radiobutton(
            radio_frame,
            text="big labels (avery L4736)",
            variable=self.label_size,
            value=1,
            background="white",
            font=("Helvetica", 11),
            highlightthickness=0,
        )
        radio_medium = tk.Radiobutton(
            radio_frame,
            text="medium labels (avery L4732)",
            variable=self.label_size,
            value=2,
            background="white",
            font=("Helvetica", 11),
            highlightthickness=0,
        )
        radio_small = tk.Radiobutton(
            radio_frame,
            text="small labels (avery L4731)",
            variable=self.label_size,
            value=3,
            background="white",
            font=("Helvetica", 11),
            highlightthickness=0,
        )

        # Pack radio buttons
        radio_big.pack(anchor="w", padx=20)
        radio_medium.pack(anchor="w", padx=20)
        radio_small.pack(anchor="w", padx=20)

        # Center the frame containing radio buttons
        radio_frame.pack(anchor="center")

        # Number of labels
        number_label = tk.Label(
            self.sample_labels_window, text="Number of labels:", background="white", font=("Helvetica", 12)
        )
        number_label.pack(pady=(20, 5))
        number_entry = tk.Entry(
            self.sample_labels_window, textvariable=self.number, relief="flat", font=("Helvetica", 11)
        )
        self.number.set(80)
        number_entry.pack()

        # Asks where to store the pdf
        output_label = tk.Label(
            self.sample_labels_window, text="Select pdf output path:", background="white", font=("Helvetica", 12)
        )
        output_label.pack(pady=(20, 5))
        self.output_button = tk.Button(
            self.sample_labels_window,
            text="select path",
            width=17,
            font=("Helvetica", 11),
            background="#f0f0f0",
            relief="flat",
            command=self.output_folder,
        )
        self.output_button.pack()

        # Create frame for action buttons
        frame_submit = tk.Frame(self.sample_labels_window)
        frame_submit.pack(pady=(50, 0))

        # Submit button
        button_submit = tk.Button(
            frame_submit,
            text="Submit",
            width=17,
            font=("Helvetica", 11),
            background="#f0f0f0",
            relief="flat",
            command=self.test_connection,
        )
        button_submit.pack(side="left")

        # Back to main button
        button_back = tk.Button(
            frame_submit,
            text="Back to Main Page",
            width=17,
            font=("Helvetica", 11),
            background="#f0f0f0",
            relief="flat",
            command=self.on_exit,
        )
        button_back.pack(side="right")

    # Function that manages the behaviour when user quits the page
    def on_exit(self) -> None:
        """
        Defines behaviour when user quits this window (by x button or specified button).

        Args:
            None

        Returns:
            None
        """
        # Destroy the actual page and reopen the main page
        self.sample_labels_window.destroy()
        self.root.deiconify()

    # Function to open the link to avery labels
    def open_link(self, model: int, event: Event) -> None:
        if model == 4736:
            webbrowser.open_new("https://www.avery.co.uk/product/mini-multipurpose-labels-l4736rev-25")
        elif model == 4732:
            webbrowser.open_new("https://www.avery.co.uk/product/mini-multipurpose-labels-l4732rev-25")
        else:
            webbrowser.open_new("https://www.avery.co.uk/product/mini-multipurpose-labels-l4731rev-25")

    # Function to select and retrieve output path
    def output_folder(self) -> None:
        """
        Asks the user to choose the output folder where PDF will be written.

        Args:
            None

        Returns:
            None
        """
        # Stores the user chosen path
        self.output_dir = filedialog.askdirectory()
        if self.output_dir:
            # Adds the output folder as button placeholder
            parts = self.output_dir.split("/")
            folder = parts[-1]
            self.output_button.config(text=folder)

    # Function to check the connection to directus
    def test_connection(self) -> None:
        """
        Controls that user has passed all the necessary arguments.
        If it is the case, it tries to connect to directus and if connection is successful,
        stores the access token for further requests.

        Args:
            None

        Returns:
            None
        """

        # Check if the number of labels is effectively an integer
        try:
            number_value = self.number.get()
        except Exception:
            number_value = 0

        # Check if output directory has been selected
        try:
            output = self.output_dir if self.output_dir else "empty"
        except Exception:
            output = "empty"

        # Check that user entered the correct values
        if (
            self.username.get()
            and self.password.get()
            and number_value > 0
            and output != "empty"
            and self.project.get()
        ):
            # Add the entered values to environment in order to pass them to processing scripts
            os.environ["USERNAME"] = self.username.get()
            os.environ["PASSWORD"] = self.password.get()
            os.environ["NUMBER"] = str(self.number.get())
            os.environ["OUTPUT_FOLDER"] = self.output_dir
            os.environ["PROJECT"] = self.project.get()
            os.environ["LABEL_SIZE"] = str(self.label_size.get())

            # Define the Directus base URL
            base_url = "https://emi-collection.unifr.ch/directus"

            # Define the login endpoint URL
            login_url = base_url + "/auth/login"
            # Create a session object for making requests
            session = requests.Session()
            # Send a POST request to the login endpoint
            response = session.post(login_url, json={"email": self.username.get(), "password": self.password.get()})
            # Test if connection is successful
            if response.status_code == 200:
                # Stores the access token
                data = response.json()["data"]
                access_token = data["access_token"]
                os.environ["ACCESS_TOKEN"] = str(access_token)
                # Launch the script to perform the labels creation
                sample_labels.main(self.sample_labels_window, self.root, self.label_info, self.label_info_2)

            # If connection to directus failed, informs the user that connection failed.
            else:
                self.label_info.config(text="Connexion to directus failed, verify your credentials!", foreground="red")
                self.label_info_2.config(text="")

        elif (
            (not self.username.get() or not self.password.get())
            and number_value > 0
            and output != "empty"
            and self.project.get()
        ):
            # If user didn't enter username or password
            self.label_info.config(text="Please provide correct Directus credentials!", foreground="red")
            self.label_info_2.config(text="")

        elif (
            self.username.get()
            and self.password.get()
            and number_value == 0
            and output != "empty"
            and self.project.get()
        ):
            # If user enter a bad label number (for example text or 0)
            self.label_info.config(text="Please provide a correct number of labels!", foreground="red")
            self.label_info_2.config(text="")

        elif (
            self.username.get()
            and self.password.get()
            and number_value > 0
            and output == "empty"
            and self.project.get()
        ):
            # If user didn't select an output dir
            self.label_info.config(text="Please select the output directory!", foreground="red")
            self.label_info_2.config(text="")

        elif (
            self.username.get()
            and self.password.get()
            and number_value > 0
            and output != "empty"
            and not self.project.get()
        ):
            # If user didn't select an EMI project
            self.label_info.config(text="Please select an EMI project!", foreground="red")
            self.label_info_2.config(text="")
        else:
            # If there are multiple parameters errors
            self.label_info.config(text="Multiple parameters errors!", foreground="red")
            self.label_info_2.config(text="")


class containerLabels(tk.Frame):
    def __init__(self, container_labels_window: tk.Toplevel, root: tk.Tk):
        """
        Initializes an instance of the class.

        Args:
            container_labels_window(tk.Toplevel): The parent widget where this frame will be placed.
            root(tk.Tk): The root window to perform actions on it.

        Returns:
            None
        """

        # Make tk elements available across functions
        self.container_labels_window = container_labels_window
        self.root = root

        # Hide main page
        self.root.withdraw()

        # Define behaviour of the closing button with function on_exit
        self.container_labels_window.protocol("WM_DELETE_WINDOW", self.on_exit)

        # Make background white
        self.container_labels_window.configure(bg="white")

        # Create a variable to store the entered text
        self.username = tk.StringVar(None)
        self.password = tk.StringVar(None)
        self.label_size = tk.IntVar(None)
        self.number = tk.IntVar(None)

        # Create informations GUI
        self.label_info = tk.Label(
            self.container_labels_window,
            text="Generates avery L4736, L4732 or L4731 container labels",
            background="white",
            font=("Helvetica", 16),
        )
        self.label_info.pack()

        # Create informations GUI
        self.label_info_2 = tk.Label(
            self.container_labels_window,
            text="and reserves the codes in directus",
            background="white",
            font=("Helvetica", 16),
        )
        self.label_info_2.pack()

        # Create informations frame
        frame_info = tk.Frame(self.container_labels_window, background="white")
        frame_info.pack(pady=(10, 20))

        # L4736 info
        self.label_l4736 = tk.Label(
            frame_info,
            text="L4736 informations",
            cursor="hand2",
            foreground="blue",
            background="white",
            font=("Helvetica", 11),
        )
        self.label_l4736.grid(row=0, column=0, padx=10)

        # Makes the link clickable
        self.label_l4736.bind("<Button-1>", lambda event: self.open_link(4736, event))

        # L4732 info
        self.label_l4732 = tk.Label(
            frame_info,
            text="L4732 informations",
            cursor="hand2",
            foreground="blue",
            background="white",
            font=("Helvetica", 11),
        )
        self.label_l4732.grid(row=0, column=1, padx=10)

        # Makes the link clickable
        self.label_l4732.bind("<Button-1>", lambda event: self.open_link(4732, event))

        # L4731 info
        self.label_l4731 = tk.Label(
            frame_info,
            text="L4731 Informations",
            cursor="hand2",
            foreground="blue",
            background="white",
            font=("Helvetica", 11),
        )
        self.label_l4731.grid(row=0, column=2, padx=10)

        # Makes the link clickable
        self.label_l4731.bind("<Button-1>", lambda event: self.open_link(4731, event))

        # Create text entry fields
        label_username = tk.Label(
            self.container_labels_window, text="Directus username:", background="white", font=("Helvetica", 12)
        )
        label_username.pack(pady=(20, 5))
        entry_username = tk.Entry(
            self.container_labels_window, textvariable=self.username, relief="flat", font=("Helvetica", 11)
        )
        entry_username.pack()

        label_password = tk.Label(
            self.container_labels_window, text="Directus password:", background="white", font=("Helvetica", 12)
        )
        label_password.pack(pady=(20, 5))
        entry_password = tk.Entry(
            self.container_labels_window, textvariable=self.password, show="*", relief="flat", font=("Helvetica", 11)
        )
        entry_password.pack()

        # Create label to choose label format
        self.label_format = tk.Label(
            self.container_labels_window, text="Choose the label format:", background="white", font=("Helvetica", 12)
        )
        self.label_format.pack(pady=(20, 5))

        # Frame to hold radio buttons
        radio_frame = tk.Frame(self.container_labels_window, bg="white")
        radio_frame.pack()

        # Set to medium size by default
        self.label_size.set(2)

        # Create radio buttons for label sizes
        radio_big = tk.Radiobutton(
            radio_frame,
            text="big labels (avery L4736)",
            variable=self.label_size,
            value=1,
            background="white",
            font=("Helvetica", 11),
            highlightthickness=0,
        )
        radio_medium = tk.Radiobutton(
            radio_frame,
            text="medium labels (avery L4732)",
            variable=self.label_size,
            value=2,
            background="white",
            font=("Helvetica", 11),
            highlightthickness=0,
        )
        radio_small = tk.Radiobutton(
            radio_frame,
            text="small labels (avery L4731)",
            variable=self.label_size,
            value=3,
            background="white",
            font=("Helvetica", 11),
            highlightthickness=0,
        )

        # Pack radio buttons
        radio_big.pack(anchor="w", padx=20)
        radio_medium.pack(anchor="w", padx=20)
        radio_small.pack(anchor="w", padx=20)

        # Center the frame containing radio buttons
        radio_frame.pack(anchor="center")

        # Number of labels
        number_label = tk.Label(
            self.container_labels_window, text="Number of labels:", background="white", font=("Helvetica", 12)
        )
        number_label.pack(pady=(20, 5))
        number_entry = tk.Entry(
            self.container_labels_window, textvariable=self.number, relief="flat", font=("Helvetica", 11)
        )
        self.number.set(80)
        number_entry.pack()

        # Asks where to store the pdf
        output_label = tk.Label(
            self.container_labels_window, text="Select pdf output path:", background="white", font=("Helvetica", 12)
        )
        output_label.pack(pady=(20, 5))
        self.output_button = tk.Button(
            self.container_labels_window,
            text="select path",
            font=("Helvetica", 11),
            width=17,
            background="#f0f0f0",
            relief="flat",
            command=self.output_folder,
        )
        self.output_button.pack()

        # Frame for action buttons
        frame_submit = tk.Frame(self.container_labels_window)
        frame_submit.pack(pady=(50, 0))

        # Submit button
        button_submit = tk.Button(
            frame_submit,
            text="Submit",
            width=17,
            font=("Helvetica", 11),
            background="#f0f0f0",
            relief="flat",
            command=self.test_parameters,
        )
        button_submit.pack(side="left")

        # Back to main button
        button_back = tk.Button(
            frame_submit,
            text="Back to Main Page",
            width=17,
            font=("Helvetica", 11),
            background="#f0f0f0",
            relief="flat",
            command=self.on_exit,
        )
        button_back.pack(side="right")

    # Function that closes gracefully the active page when user decides to quit
    def on_exit(self) -> None:
        """
        Defines behaviour when user quits this window (by x button or specified button).

        Args:
            None

        Returns:
            None
        """
        # Destroy actual page and displays the main page
        self.container_labels_window.destroy()
        self.root.deiconify()

    # Function to open the link to avery labels
    def open_link(self, model: int, event: Event) -> None:
        if model == 4736:
            webbrowser.open_new("https://www.avery.co.uk/product/mini-multipurpose-labels-l4736rev-25")
        elif model == 4732:
            webbrowser.open_new("https://www.avery.co.uk/product/mini-multipurpose-labels-l4732rev-25")
        else:
            webbrowser.open_new("https://www.avery.co.uk/product/mini-multipurpose-labels-l4731rev-25")

    # Function to select and retrieve output path
    def output_folder(self) -> None:
        """
        Asks the user to choose the output folder where PDF will be written.

        Args:
            None

        Returns:
            None
        """
        # Stores the user chosen path
        self.output_dir = filedialog.askdirectory()
        if self.output_dir:
            # Adds the output folder as button placeholder
            parts = self.output_dir.split("/")
            folder = parts[-1]
            self.output_button.config(text=folder)

    def test_parameters(self) -> None:
        """
        Controls that user has passed all the necessary arguments.

        Args:
            None

        Returns:
            None
        """

        # Check if the row number is effectively an integer
        try:
            number_value = self.number.get()
        except Exception:
            number_value = 0

        # Check if output directory has been selected
        try:
            output = self.output_dir if self.output_dir else "empty"
        except Exception:
            output = "empty"

        # Check that user entered the correct values
        if self.username.get() and self.password.get() and number_value > 0 and output != "empty":
            self.test_connection()

        elif (not self.username.get() or not self.password.get()) and number_value > 0 and output != "empty":
            # If user didn't enter username or password
            self.label_info.config(text="Please provide correct Directus credentials!", foreground="red")
            self.label_info_2.config(text="")

        elif self.username.get() and self.password.get() and number_value > 0 and output == "empty":
            # If user didn't select an output dir
            self.label_info.config(text="Please select the output directory!", foreground="red")
            self.label_info_2.config(text="")

        else:
            # If there are multiple parameters errors
            self.label_info.config(text="Multiple parameters errors!", foreground="red")
            self.label_info_2.config(text="")

    def test_connection(self) -> None:
        """
        Tries to connect to directus and if connection is successful,
        stores the access token for further requests.

        Args:
            None

        Returns:
            None
        """
        # Retrieve the entered values
        os.environ["USERNAME"] = self.username.get()
        os.environ["PASSWORD"] = self.password.get()
        os.environ["LABEL_SIZE"] = str(self.label_size.get())
        os.environ["NUMBER"] = str(self.number.get())
        os.environ["OUTPUT_FOLDER"] = self.output_dir

        # Define the Directus base URL
        base_url = "https://emi-collection.unifr.ch/directus"

        # Define the login endpoint URL
        login_url = base_url + "/auth/login"
        # Create a session object for making requests
        session = requests.Session()
        # Send a POST request to the login endpoint
        response = session.post(login_url, json={"email": self.username.get(), "password": self.password.get()})
        # Test if connection is successful
        if response.status_code == 200:
            # Stores the access token
            data = response.json()["data"]
            access_token = data["access_token"]
            os.environ["ACCESS_TOKEN"] = str(access_token)
            container_labels.main(self.container_labels_window, self.root, self.label_info, self.label_info_2)

        # If connection to directus failed, informs the user that connection failed.
        else:
            self.label_info.config(text="Connexion to directus failed, verify your credentials!", foreground="red")
            self.label_info_2.config(text="")


class csvLabels(tk.Frame):
    def __init__(self, csv_labels_window: tk.Toplevel, root: tk.Tk):
        """
        Initializes an instance of the class.

        Args:
            csv_labels_window(tk.Toplevel): The parent widget where this frame will be placed.
            root(tk.Tk): The root window to perform actions on it.

        Returns:
            None
        """

        # Make tk elements available across functions
        self.csv_labels_window = csv_labels_window
        self.root = root

        # Hide main page
        self.root.withdraw()

        # Define behaviour of the closing button with function on_exit
        self.csv_labels_window.protocol("WM_DELETE_WINDOW", self.on_exit)

        # Make background white
        self.csv_labels_window.configure(bg="white")

        # Create a variable to store the entered text
        self.number_ext = tk.StringVar(None)
        self.number_inj = tk.StringVar(None)
        self.label_size = tk.IntVar(None)

        # Create informations GUI
        self.label_info = tk.Label(
            self.csv_labels_window,
            text="Generates avery L4736, L4732 or L4731 labels from a CSV file",
            background="white",
            font=("Helvetica", 16),
        )
        self.label_info.pack()

        # Create informations frame
        frame_info = tk.Frame(self.csv_labels_window, background="white")
        frame_info.pack(pady=(10, 20))

        # L4736 info
        self.label_l4736 = tk.Label(
            frame_info,
            text="L4736 informations",
            cursor="hand2",
            foreground="blue",
            background="white",
            font=("Helvetica", 11),
        )
        self.label_l4736.grid(row=0, column=0, padx=10)

        # Makes the link clickable
        self.label_l4736.bind("<Button-1>", lambda event: self.open_link(4736, event))

        # L4732 info
        self.label_l4732 = tk.Label(
            frame_info,
            text="L4732 informations",
            cursor="hand2",
            foreground="blue",
            background="white",
            font=("Helvetica", 11),
        )
        self.label_l4732.grid(row=0, column=1, padx=10)

        # Makes the link clickable
        self.label_l4732.bind("<Button-1>", lambda event: self.open_link(4732, event))

        # L4731 info
        self.label_l4731 = tk.Label(
            frame_info,
            text="L4731 Informations",
            cursor="hand2",
            foreground="blue",
            background="white",
            font=("Helvetica", 11),
        )
        self.label_l4731.grid(row=0, column=2, padx=10)

        # Makes the link clickable
        self.label_l4731.bind("<Button-1>", lambda event: self.open_link(4731, event))

        import_label = tk.Label(
            self.csv_labels_window,
            text="CSV is expected to have a unique column containing codes, without header.",
            background="white",
            font=("Helvetica", 11),
        )
        import_label.pack()

        warning_label = tk.Label(
            self.csv_labels_window,
            text="Be careful, this mode doesn't verify that labels are unique and doesn't enter them into Directus.",
            foreground="orange",
            background="white",
            font=("Helvetica", 11),
        )
        warning_label.pack()

        # Import the CSV
        self.csv_label = tk.Label(
            self.csv_labels_window, text="Choose your CSV", background="white", font=("Helvetica", 12)
        )
        self.csv_label.pack(pady=(20, 5))
        self.import_button = tk.Button(
            self.csv_labels_window,
            text="select CSV:",
            width=17,
            font=("Helvetica", 11),
            background="#f0f0f0",
            relief="flat",
            command=self.import_csv,
        )
        self.import_button.pack()

        # Create label to choose label format
        self.label_format = tk.Label(
            self.csv_labels_window, text="Choose the label format:", background="white", font=("Helvetica", 12)
        )
        self.label_format.pack(pady=(20, 5))

        # Frame to hold radio buttons
        radio_frame = tk.Frame(self.csv_labels_window, bg="white")
        radio_frame.pack()

        # Set to medium size by default
        self.label_size.set(2)

        # Create radio buttons for label sizes
        radio_big = tk.Radiobutton(
            radio_frame,
            text="big labels (avery L4736)",
            variable=self.label_size,
            value=1,
            background="white",
            font=("Helvetica", 11),
            highlightthickness=0,
        )
        radio_medium = tk.Radiobutton(
            radio_frame,
            text="medium labels (avery L4732)",
            variable=self.label_size,
            value=2,
            background="white",
            font=("Helvetica", 11),
            highlightthickness=0,
        )
        radio_small = tk.Radiobutton(
            radio_frame,
            text="small labels (avery L4731)",
            variable=self.label_size,
            value=3,
            background="white",
            font=("Helvetica", 11),
            highlightthickness=0,
        )

        # Pack radio buttons
        radio_big.pack(anchor="w", padx=20)
        radio_medium.pack(anchor="w", padx=20)
        radio_small.pack(anchor="w", padx=20)

        # Center the frame containing radio buttons
        radio_frame.pack(anchor="center")

        # Create elements to select output directory
        output_label = tk.Label(
            self.csv_labels_window,
            text="Select the output path for the pdf files:",
            background="white",
            font=("Helvetica", 12),
        )
        output_label.pack(pady=(20, 5))
        self.output_button = tk.Button(
            self.csv_labels_window,
            text="select path",
            width=17,
            font=("Helvetica", 11),
            background="#f0f0f0",
            relief="flat",
            command=self.output_folder,
        )
        self.output_button.pack()

        # Frame for action buttons
        frame_submit = tk.Frame(self.csv_labels_window)
        frame_submit.pack(pady=(50, 0))

        # Submit button
        button_submit = tk.Button(
            frame_submit,
            text="Submit",
            width=17,
            font=("Helvetica", 11),
            background="#f0f0f0",
            relief="flat",
            command=self.submit_result,
        )
        button_submit.pack(side="left")

        # Back to main button
        button_back = tk.Button(
            frame_submit,
            text="Back to Main Page",
            width=17,
            font=("Helvetica", 11),
            background="#f0f0f0",
            relief="flat",
            command=self.on_exit,
        )
        button_back.pack(side="right")

    # Function that closes gracefully the active page when user decides to quit
    def on_exit(self) -> None:
        """
        Defines behaviour when user quits this window (by x button or specified button).

        Args:
            None

        Returns:
            None
        """
        # Destroy actual page and displays the main page
        self.csv_labels_window.destroy()
        self.root.deiconify()

    # Function to open the link to avery labels
    def open_link(self, model: int, event: Event) -> None:
        if model == 4736:
            webbrowser.open_new("https://www.avery.co.uk/product/mini-multipurpose-labels-l4736rev-25")
        elif model == 4732:
            webbrowser.open_new("https://www.avery.co.uk/product/mini-multipurpose-labels-l4732rev-25")
        else:
            webbrowser.open_new("https://www.avery.co.uk/product/mini-multipurpose-labels-l4731rev-25")

    # Function to select and retrieve CSV path
    def import_csv(self) -> None:
        """
        Asks the path to input CSV.

        Args:
            None

        Returns:
            None
        """
        # Stores the user chosen path
        self.csv_file = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if self.csv_file:
            # Adds the output folder as button placeholder
            parts = self.csv_file.split("/")
            file = parts[-1]
            self.import_button.config(text=file)

    # Function to select and retrieve output path
    def output_folder(self) -> None:
        """
        Asks the user to choose the output folder where PDF will be written.

        Args:
            None

        Returns:
            None
        """
        # Stores the user chosen path
        self.output_dir = filedialog.askdirectory()
        if self.output_dir:
            # Adds the output folder as button placeholder
            parts = self.output_dir.split("/")
            folder = parts[-1]
            self.output_button.config(text=folder)

    # Function to check if user entered parameters are correct and launches the process script
    def submit_result(self) -> None:
        """
        performs modifications on the CSV, submit them to directus and writes the output csv.

        Args:
            None

        Returns:
            None
        """

        # Check if a CSV file has been selected
        try:
            csv = self.csv_file if self.csv_file else "empty"
        except Exception:
            csv = "empty"

        # Check if output directory has been selected
        try:
            output = self.output_dir if self.output_dir else "empty"
        except Exception:
            output = "empty"

        # Check that user entered the correct values
        if csv != "empty" and output != "empty":
            # Add size parameters to environment
            os.environ["LABEL_SIZE"] = str(self.label_size.get())
            os.environ["FILE_PATH"] = self.csv_file
            os.environ["OUTPUT_FOLDER"] = self.output_dir
            csv_labels.main(self.csv_labels_window, self.root)

        elif csv == "empty" and output != "empty":
            # If no CSV selected
            self.label_info.config(text="Please select a CSV!", foreground="red")

        elif csv != "empty" and output == "empty":
            # If no output dir selected
            self.label_info.config(text="Please select the output directory!", foreground="red")

        else:
            # If there are multiple parameters errors
            self.label_info.config(text="Multiple parameters errors!", foreground="red")


class newSite(tk.Frame):
    def __init__(self, new_site_window: tk.Toplevel, root: tk.Tk):
        """
        Initializes an instance of the class.

        Args:
            new_site_window(tk.Toplevel): The parent widget where this frame will be placed.
            root(tk.Tk): The root window to perform actions on it.

        Returns:
            None
        """

        # Make tk elements available across functions
        self.new_site_window = new_site_window
        self.root = root

        # Hide main page
        self.root.withdraw()

        # Define behaviour of the closing button with function on_exit
        self.new_site_window.protocol("WM_DELETE_WINDOW", self.on_exit)

        # Make background white
        self.new_site_window.configure(bg="white")

        # Create a variable to store the entered text
        self.username = tk.StringVar(None)
        self.password = tk.StringVar(None)

        # Create information label
        self.label = tk.Label(
            self.new_site_window, text="Register a new site", background="white", font=("Helvetica", 16)
        )
        self.label.pack()

        # Request the university list
        list_uni = requests.get("http://universities.hipolabs.com/search?", timeout=1000)

        # If the request is successfull
        if list_uni.status_code == 200:
            # Retrieves the list as a json
            data = list_uni.json()

            # Extract the needed values from the list
            self.dataf = pd.DataFrame(
                data=data, columns=["alpha_two_code", "web_pages", "country", "state-province", "name", "domains"]
            )

            # Sort universities by country
            unique_countries = self.dataf["country"].drop_duplicates().reset_index(drop=True)
            self.sorted_countries = pd.DataFrame(unique_countries).sort_values("country").reset_index(drop=True)

            # Create Directus connexion fields
            label_username = tk.Label(
                self.new_site_window, text="Directus username:", background="white", font=("Helvetica", 12)
            )
            label_username.pack(pady=(20, 5))
            entry_username = tk.Entry(
                self.new_site_window, textvariable=self.username, relief="flat", font=("Helvetica", 11)
            )
            entry_username.pack()

            label_password = tk.Label(
                self.new_site_window, text="Directus password:", background="white", font=("Helvetica", 12)
            )
            label_password.pack(pady=(20, 5))
            entry_password = tk.Entry(
                self.new_site_window, textvariable=self.password, show="*", relief="flat", font=("Helvetica", 11)
            )
            entry_password.pack()

            # Create the country selection box
            label_country = tk.Label(
                self.new_site_window, text="Search for a country:", background="white", font=("Helvetica", 12)
            )
            label_country.pack(pady=(20, 5))

            # Create a style for the combobox
            style = ttk.Style()
            style.configure(
                "TCombobox",
                background="white",
                relief="flat",
                borderwidth=0.5,
                highlightthickness=0,
                bordercolor="#f0f0f0",
            )

            self.combobox_country = ttk.Combobox(self.new_site_window)
            self.combobox_country.pack()

            self.listbox_country = tk.Listbox(
                self.new_site_window, height=3, width=50, font=("Helvetica", 10), relief="flat"
            )
            self.listbox_country.pack()

            # Create the university selection box
            label_university = tk.Label(
                self.new_site_window, text="Search for a university:", background="white", font=("Helvetica", 12)
            )
            label_university.pack(pady=(20, 5))

            self.combobox_university = ttk.Combobox(self.new_site_window)
            self.combobox_university.pack()

            self.listbox_university = tk.Listbox(
                self.new_site_window, height=3, width=50, font=("Helvetica", 10), relief="flat"
            )
            self.listbox_university.pack()

            # Bind the event handlers for country and university selection
            self.listbox_country.bind("<<ListboxSelect>>", self.on_country_select)
            self.listbox_university.bind("<<ListboxSelect>>", self.on_university_select)

            # Bind event handlers for updating suggestions
            self.combobox_country.bind("<KeyRelease>", lambda event: root.after(50, self.update_country_suggestions))
            self.combobox_university.bind(
                "<KeyRelease>", lambda event: root.after(50, self.update_university_suggestions)
            )

            # prints the selected site to inform the user which site is actually selected
            self.label_info = tk.Label(
                self.new_site_window, text="Selected site:", background="white", font=("Helvetica", 12)
            )
            self.label_info.pack(pady=(20, 5))

            # Create the frame for action buttons
            frame_submit = tk.Frame(self.new_site_window)
            frame_submit.pack(pady=(50, 0))

            # Submit button
            button_submit = tk.Button(
                frame_submit,
                text="Submit",
                width=17,
                font=("Helvetica", 11),
                background="#f0f0f0",
                relief="flat",
                command=self.test_connection,
            )
            button_submit.pack(side="left")

            # Back to main button
            button_back = tk.Button(
                frame_submit,
                text="Back to Main Page",
                width=17,
                font=("Helvetica", 11),
                background="#f0f0f0",
                relief="flat",
                command=self.on_exit,
            )
            button_back.pack(side="right")

        # If API request to Hipo fails, informs the user
        else:
            self.label.config(text="No access to Hipo API, please verify your internet connection.", foreground="red")

    # Function that closes gracefully the active page when user decides to quit
    def on_exit(self) -> None:
        """
        Defines behaviour when user quits this window (by x button or specified button).

        Args:
            None

        Returns:
            None
        """
        # Destroy actual page and displays the main page
        self.new_site_window.destroy()
        self.root.deiconify()

    # Function to update the country list when user types the beginning of the country
    def update_country_suggestions(self) -> None:
        selected_item = self.combobox_country.get()
        if selected_item:
            # Use fuzzywuzzy to get the 3 best matches for countries
            matches = process.extract(selected_item, self.sorted_countries["country"].tolist(), limit=3)
            self.country_suggestions = [match for match, _ in matches if _ >= 50]

            # Update the listbox with country suggestions
            self.listbox_country.delete(0, tk.END)
            for suggestion in self.country_suggestions:
                self.listbox_country.insert(tk.END, suggestion)

    # Function to update the university list when user types the beginning of the university
    def update_university_suggestions(self) -> None:
        if self.selected_country:
            # Filter universities based on selected country
            country_filtered_universities = self.dataf[self.dataf["country"] == self.selected_country]
            selected_item = self.combobox_university.get()
            if selected_item:
                # Use fuzzywuzzy to get the 7 best matches for universities in the selected country
                matches = process.extract(selected_item, country_filtered_universities["name"].tolist(), limit=7)
                university_suggestions = [match for match, _ in matches if _ >= 50]

                # Update the listbox with university suggestions
                self.listbox_university.delete(0, tk.END)
                for suggestion in university_suggestions:
                    self.listbox_university.insert(tk.END, suggestion)

    # Function to define behaviour when user chooses a country
    def on_country_select(self, event: Event) -> None:
        selected_index = self.listbox_country.curselection()
        if selected_index:
            # Retrieves the user's country choice
            self.selected_country = self.listbox_country.get(selected_index)
            # Clean the user entered text
            self.combobox_country.delete(0, tk.END)
            # Insert the selected country in the field
            self.combobox_country.insert(tk.END, self.selected_country)
            # update university list
            self.update_university_suggestions()

    # Function to define behaviour when user chooses a country
    def on_university_select(self, event: Event) -> None:
        selected_index = self.listbox_university.curselection()
        if selected_index:
            # Retrieves the user's university choice
            self.selected_university = self.listbox_university.get(selected_index)
            # Clean the user entered text
            self.combobox_university.delete(0, tk.END)
            # Insert the selected university in the field
            self.combobox_university.insert(tk.END, self.selected_university)
            # Adds the selected university to the information label
            self.label_info.config(text=f"Selected site: {self.selected_university}")
            # Create a subset of the universities dataframe to retrieve selected university information
            self.subset = self.dataf[self.dataf["name"] == self.selected_university]

    def test_connection(self) -> None:
        """
        Controls that user has passed all the necessary arguments.
        If it is the case, it tries to connect to directus and if connection is successful,
        stores the access token for further requests.

        Args:
            None

        Returns:
            None
        """

        # Check if a country has been selected
        try:
            country = self.selected_country if self.selected_country else "empty"
        except Exception:
            country = "empty"

        # Check if a country has been selected
        try:
            university = self.selected_university if self.selected_university else "empty"
        except Exception:
            university = "empty"

        # Check that user entered the correct values
        if self.username.get() and self.password.get() and country != "empty" and university != "empty":
            # Retrieve the entered values
            os.environ["USERNAME"] = self.username.get()
            os.environ["PASSWORD"] = self.password.get()
            os.environ["ALPHA_TWO_CODE"] = str(self.subset["alpha_two_code"].values[0])
            os.environ["WEB_PAGES"] = str(self.subset["web_pages"].values[0])
            os.environ["COUNTRY"] = str(self.subset["country"].values[0])
            os.environ["STATE"] = str(self.subset["state-province"].values[0])
            os.environ["SITE"] = str(self.subset["name"].values[0])
            os.environ["DOMAINS"] = str(self.subset["domains"].values[0])

            # Define the Directus base URL
            base_url = "https://emi-collection.unifr.ch/directus"

            # Define the login endpoint URL
            login_url = base_url + "/auth/login"
            # Create a session object for making requests
            session = requests.Session()
            # Send a POST request to the login endpoint
            response = session.post(login_url, json={"email": self.username.get(), "password": self.password.get()})
            # Test if connection is successful
            if response.status_code == 200:
                # Stores the access token
                data = response.json()["data"]
                access_token = data["access_token"]
                os.environ["ACCESS_TOKEN"] = str(access_token)
                new_site.main(self.new_site_window, self.root, self.label)

            # If connection to directus failed, informs the user that connection failed.
            else:
                self.label.config(text="Connexion to directus failed, verify your credentials!", foreground="red")

        elif (not self.username.get() or not self.password.get()) and country != "empty" and university != "empty":
            # If user didn't enter username or password
            self.label.config(text="Please provide correct Directus credentials!", foreground="red")

        elif self.username.get() and self.password.get() and country == "empty":
            # If user didn't choose a country
            self.label.config(text="Please select a country!", foreground="red")

        elif self.username.get() and self.password.get() and university == "empty":
            # If user didn't choose a university
            self.label.config(text="Please select a university!", foreground="red")

        else:
            # If there are multiple parameters errors
            self.label.config(text="Multiple parameters errors!", foreground="red")


# Create the main window
root = tk.Tk()
root.title("EMI Label Creator")
root.minsize(600, 260)
root.configure(bg="white")

# Create the main page
main_page = MainPage(root)
main_page.pack()

root.mainloop()
