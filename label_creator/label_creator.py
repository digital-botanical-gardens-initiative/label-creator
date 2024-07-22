# To convert this script into a binary compatible with the OS where the command is executed: 
# pyinstaller --onefile --paths=./ --hidden-import=create_labels_csv --hidden-import=create_new_labels --hidden-import=create_new_mob_cont --hidden-import=create_new_site --hidden-import=create_new_stat_cont label_creator.py

import os
import tkinter as tk
import webbrowser
from tkinter import Event, filedialog, ttk
from typing import Any

import create_labels_csv
import create_new_labels
import create_new_mob_cont
import create_new_site
import create_new_stat_cont
import pandas as pd
import requests
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

        # Create widgets for the main page

        # Create GUI elements for labels
        label_labels = tk.Label(self, text="Create labels")
        label_labels.pack()

        button_new_labels = tk.Button(self, text="Generate labels from scratch", width=40, command=self.open_new_labels)
        button_new_labels.pack()

        button_mobile_container = tk.Button(
            self, text="Generate mobile containers labels from scratch", width=40, command=self.open_mobile_container
        )
        button_mobile_container.pack()

        button_static_container = tk.Button(
            self, text="Generate static containers labels from scratch", width=40, command=self.open_static_container
        )
        button_static_container.pack()

        button_existing = tk.Button(self, text="Print labels from a CSV", width=40, command=self.open_csv_labels)
        button_existing.pack()

        # Add some space to discriminate label generation from adding a new site
        label_space = tk.Label(self, text="")
        label_space.pack()

        label_space = tk.Label(self, text="")
        label_space.pack()

        # Create GUI elements to add a new site
        label_new_site = tk.Label(self, text="Add a new site to the database")
        label_new_site.pack()

        button_new_site = tk.Button(self, text="Add a new site", width=40, command=self.open_new_site)
        button_new_site.pack()

    def open_new_labels(self) -> None:
        # Create a new Toplevel window for the new labels
        new_labels_window = tk.Toplevel(root)
        new_labels_window.title("Generate new labels")
        # Launches the corresponding class
        newLabels(new_labels_window, root)

    def open_mobile_container(self) -> None:
        # Create a new Toplevel window for the mobile containers
        new_mob_cont_window = tk.Toplevel(root)
        new_mob_cont_window.title("Generate new mobile containers labels")
        # Launches the corresponding class
        newMobCont(new_mob_cont_window, root)

    def open_static_container(self) -> None:
        # Create a new Toplevel window for the static containers
        new_stat_cont_window = tk.Toplevel(root)
        new_stat_cont_window.title("Generate new static containers labels")
        # Launches the corresponding class
        newStatCont(new_stat_cont_window, root)

    def open_csv_labels(self) -> None:
        # Create a new Toplevel window for the labels from CSV
        csv_labels_window = tk.Toplevel(root)
        csv_labels_window.title("Generate labels from CSV")
        # Launches the corresponding class
        csvLabels(csv_labels_window, root)

    def open_new_site(self) -> None:
        # Create a new Toplevel window to add a new site
        new_site_window = tk.Toplevel(root)
        new_site_window.title("Add a new site")
        # Launches the corresponding class
        newSite(new_site_window, root)


# Class to create new labels
class newLabels(tk.Frame):
    def __init__(self, new_labels_window: tk.Toplevel, root: tk.Tk):
        """
        Initializes an instance of the class.

        Args:
            csv_batch_window(tk.Toplevel): The parent widget where this frame will be placed.
            root(tk.Tk): The root window to perform actions on it.

        Returns:
            None
        """

        # Makes tk elements available across functions
        self.new_labels_window = new_labels_window
        self.root = root

        # Hide main page
        self.root.withdraw()

        # Associates the close button to a specific action managed by on_exit function
        self.new_labels_window.protocol("WM_DELETE_WINDOW", self.on_exit)

        # Create variables to store the user entered parameters
        self.username = tk.StringVar(None)
        self.password = tk.StringVar(None)
        self.number = tk.IntVar(None)
        self.project = tk.StringVar(None)

        # Create GUI elements for this class
        frame_info = tk.Frame(self.new_labels_window)
        frame_info.pack(pady=(10, 20))

        # Create widgets for the main page
        self.label = tk.Label(
            frame_info,
            text="Generates avery L4732 (https://www.avery.co.uk/product/mini-multipurpose-labels-l4732rev-25) labels and reserves the codes in directus",
            cursor="hand2",
        )
        self.label.pack()
        # Makes the link clickable
        self.label.bind("<Button-1>", self.open_link)

        # Create text entry fields
        label_username = tk.Label(self.new_labels_window, text="Directus username:")
        label_username.pack()
        entry_username = tk.Entry(self.new_labels_window, textvariable=self.username)
        entry_username.pack()

        label_password = tk.Label(self.new_labels_window, text="Directus password:")
        label_password.pack()
        entry_password = tk.Entry(self.new_labels_window, textvariable=self.password, show="*")
        entry_password.pack()

        # Extract the project names from directus
        collection_url = "http://directus.dbgi.org/items/EMI_codes"
        column = "emi_code"
        params = {"sort[]": f"{column}"}
        session = requests.Session()
        response = session.get(collection_url, params=params)
        data = response.json()["data"]
        project_names = [item[column] for item in data]

        # Choose the project
        project_label = tk.Label(self.new_labels_window, text="Choose your project:")
        project_label.pack()
        dropdown_project = tk.OptionMenu(self.new_labels_window, self.project, *project_names)
        dropdown_project.pack()

        # Number of labels
        number_label = tk.Label(self.new_labels_window, text="Number of labels:")
        number_label.pack()
        number_entry = tk.Entry(self.new_labels_window, textvariable=self.number)
        self.number.set(80)
        number_entry.pack()

        # Asks where to store the pdf
        output_label = tk.Label(self.new_labels_window, text="Select pdf output path:")
        output_label.pack()
        self.output_button = tk.Button(self.new_labels_window, text="select path", width=17, command=self.output_folder)
        self.output_button.pack()

        frame_submit = tk.Frame(self.new_labels_window)
        frame_submit.pack(pady=(50, 0))

        # Submit button
        button_submit = tk.Button(frame_submit, text="Submit", width=17, command=self.test_connection)
        button_submit.pack(side="left")

        # Back to main button
        button_back = tk.Button(frame_submit, text="Back to Main Page", width=17, command=self.on_exit)
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
        self.new_labels_window.destroy()
        self.root.deiconify()

    # Function to open the link to avery labels
    def open_link(self, event: Event) -> None:
        webbrowser.open_new("https://www.avery.co.uk/product/mini-multipurpose-labels-l4732rev-25")

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
        except:
            number_value = 0

        # Check if output directory has been selected
        try:
            if self.output_dir:
                output = self.output_dir
            else:
                output = "empty"

        except:
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

            # Define the Directus base URL
            base_url = "http://directus.dbgi.org"

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
                create_new_labels.main(self.new_labels_window, self.root, self.label)

            # If connection to directus failed, informs the user that connection failed.
            else:
                self.label.config(
                    text="Connexion to directus failed, verify your credentials/vpn connection!", foreground="red"
                )

        elif (
            (not self.username.get() or not self.password.get())
            and number_value > 0
            and output != "empty"
            and self.project.get()
        ):
            # If user didn't enter username or password
            self.label.config(text="Please provide correct Directus credentials!", foreground="red")

        elif (
            self.username.get()
            and self.password.get()
            and number_value == 0
            and output != "empty"
            and self.project.get()
        ):
            # If user enter a bad label number (for example text or 0)
            self.label.config(text="Please provide a correct number of labels!", foreground="red")

        elif (
            self.username.get()
            and self.password.get()
            and number_value > 0
            and output == "empty"
            and self.project.get()
        ):
            # If user didn't select an output dir
            self.label.config(text="Please select the output directory!", foreground="red")

        elif (
            self.username.get()
            and self.password.get()
            and number_value > 0
            and output != "empty"
            and not self.project.get()
        ):
            # If user didn't select an EMI project
            self.label.config(text="Please select an EMI code!", foreground="red")
        else:
            # If there are multiple parameters errors
            self.label.config(text="Multiple parameters errors!", foreground="red")


class newMobCont(tk.Frame):
    def __init__(self, new_mob_cont_window: tk.Toplevel, root: tk.Tk):
        """
        Initializes an instance of the class.

        Args:
            new_mob_cont_window(tk.Toplevel): The parent widget where this frame will be placed.
            root(tk.Tk): The root window to perform actions on it.

        Returns:
            None
        """

        # Make tk elements available across functions
        self.new_mob_cont_window = new_mob_cont_window
        self.root = root

        # Hide main page
        self.root.withdraw()

        # Define behaviour of the closing button with function on_exit
        self.new_mob_cont_window.protocol("WM_DELETE_WINDOW", self.on_exit)

        # Create a variable to store the entered text
        self.username = tk.StringVar(None)
        self.password = tk.StringVar(None)
        self.number_rows = tk.IntVar(None)
        self.number_cols = tk.IntVar(None)
        self.number = tk.IntVar(None)

        # Create a frame for the informations
        frame_info = tk.Frame(self.new_mob_cont_window)
        frame_info.pack(pady=(10, 20))

        # Adds the information label
        self.label = tk.Label(
            frame_info,
            text="Generates avery L4732 (https://www.avery.co.uk/product/mini-multipurpose-labels-l4732rev-25) mobile container labels and reserves the codes in directus",
            cursor="hand2",
        )
        self.label.pack()

        # Makes the link clickable
        self.label.bind("<Button-1>", self.open_link)

        # Create text entry fields
        label_username = tk.Label(self.new_mob_cont_window, text="Directus username:")
        label_username.pack()
        entry_username = tk.Entry(self.new_mob_cont_window, textvariable=self.username)
        entry_username.pack()

        label_password = tk.Label(self.new_mob_cont_window, text="Directus password:")
        label_password.pack()
        entry_password = tk.Entry(self.new_mob_cont_window, textvariable=self.password, show="*")
        entry_password.pack()

        # Number of rows
        number_rows = tk.Label(self.new_mob_cont_window, text="Container's rows number:")
        number_rows.pack()
        number_entry_rows = tk.Entry(self.new_mob_cont_window, textvariable=self.number_rows)
        number_entry_rows.pack()

        # Number of columns
        number_columns = tk.Label(self.new_mob_cont_window, text="Container's columns number:")
        number_columns.pack()
        number_entry_columns = tk.Entry(self.new_mob_cont_window, textvariable=self.number_cols)
        number_entry_columns.pack()

        # Number of labels
        number_label = tk.Label(self.new_mob_cont_window, text="Number of labels:")
        number_label.pack()
        number_entry = tk.Entry(self.new_mob_cont_window, textvariable=self.number)
        self.number.set(80)
        number_entry.pack()

        # Asks where to store the pdf
        output_label = tk.Label(self.new_mob_cont_window, text="Select pdf output path:")
        output_label.pack()
        self.output_button = tk.Button(
            self.new_mob_cont_window, text="select path", width=17, command=self.output_folder
        )
        self.output_button.pack()

        # Frame for action buttons
        frame_submit = tk.Frame(self.new_mob_cont_window)
        frame_submit.pack(pady=(50, 0))

        # Submit button
        button_submit = tk.Button(frame_submit, text="Submit", width=17, command=self.test_connection)
        button_submit.pack(side="left")

        # Back to main button
        button_back = tk.Button(frame_submit, text="Back to Main Page", width=17, command=self.on_exit)
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
        self.new_mob_cont_window.destroy()
        self.root.deiconify()

    # Function to open the labels link when user clicks ont the information label
    def open_link(self, event: Event) -> None:
        webbrowser.open_new("https://www.avery.co.uk/product/mini-multipurpose-labels-l4732rev-25")

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

        # Check if the row number is effectively an integer
        try:
            number_row = self.number_rows.get()
        except:
            number_row = 0

        # Check if the column number is effectively an integer
        try:
            number_col = self.number_cols.get()
        except:
            number_col = 0

        # Check if the number of labels is effectively an integer
        try:
            number_value = self.number.get()
        except:
            number_value = 0

        # Check if output directory has been selected
        try:
            if self.output_dir:
                output = self.output_dir
            else:
                output = "empty"

        except:
            output = "empty"

        # Check that user entered the correct values
        if (
            self.username.get()
            and self.password.get()
            and number_row > 0
            and number_col > 0
            and number_value > 0
            and output != "empty"
        ):
            # Retrieve the entered values
            os.environ["USERNAME"] = self.username.get()
            os.environ["PASSWORD"] = self.password.get()
            os.environ["NUMBER_ROWS"] = str(self.number_rows.get())
            os.environ["NUMBER_COLS"] = str(self.number_cols.get())
            os.environ["NUMBER"] = str(self.number.get())
            os.environ["OUTPUT_FOLDER"] = self.output_dir

            # Define the Directus base URL
            base_url = "http://directus.dbgi.org"

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
                create_new_mob_cont.main(self.new_mob_cont_window, self.root, self.label)

            # If connection to directus failed, informs the user that connection failed.
            else:
                self.label.config(
                    text="Connexion to directus failed, verify your credentials/vpn connection", foreground="red"
                )

        elif (
            (not self.username.get() or not self.password.get())
            and number_row > 0
            and number_col > 0
            and number_value > 0
            and output != "empty"
        ):
            # If user didn't enter username or password
            self.label.config(text="Please provide correct Directus credentials!", foreground="red")

        elif (
            self.username.get()
            and self.password.get()
            and number_row == 0
            and number_col > 0
            and number_value > 0
            and output != "empty"
        ):
            # If user enter a bad row number (for example text or 0)
            self.label.config(text="Please provide a correct row number!", foreground="red")

        elif (
            self.username.get()
            and self.password.get()
            and number_row > 0
            and number_col == 0
            and number_value > 0
            and output != "empty"
        ):
            # If user enter a bad column number (for example text or 0)
            self.label.config(text="Please provide a correct column number!", foreground="red")

        elif (
            self.username.get()
            and self.password.get()
            and number_row > 0
            and number_col > 0
            and number_value == 0
            and output != "empty"
        ):
            # If user enter a bad label number (for example text or 0)
            self.label.config(text="Please provide a correct number of labels!", foreground="red")

        elif (
            self.username.get()
            and self.password.get()
            and number_row > 0
            and number_col > 0
            and number_value > 0
            and output == "empty"
        ):
            # If user didn't select an output dir
            self.label.config(text="Please select the output directory!", foreground="red")

        else:
            # If there are multiple parameters errors
            self.label.config(text="Multiple parameters errors!", foreground="red")


class newStatCont(tk.Frame):
    def __init__(self, new_stat_cont_window: tk.Toplevel, root: tk.Tk):
        """
        Initializes an instance of the class.

        Args:
            new_stat_cont_window(tk.Toplevel): The parent widget where this frame will be placed.
            root(tk.Tk): The root window to perform actions on it.

        Returns:
            None
        """

        # Make tk elements available across functions
        self.new_stat_cont_window = new_stat_cont_window
        self.root = root

        # Hide main page
        self.root.withdraw()

        # Define behaviour of the closing button with function on_exit
        self.new_stat_cont_window.protocol("WM_DELETE_WINDOW", self.on_exit)

        # Create a variable to store the entered text
        self.username = tk.StringVar(None)
        self.password = tk.StringVar(None)
        self.number = tk.IntVar(None)

        # Create a frame for the informations
        frame_info = tk.Frame(self.new_stat_cont_window)
        frame_info.pack(pady=(10, 20))

        # Adds the information label
        self.label = tk.Label(
            frame_info,
            text="Generates avery L4732 (https://www.avery.co.uk/product/mini-multipurpose-labels-l4732rev-25) static container labels and reserves the codes in directus",
            cursor="hand2",
        )
        self.label.pack()

        # Makes the link clickable
        self.label.bind("<Button-1>", self.open_link)

        # Create text entry fields
        label_username = tk.Label(self.new_stat_cont_window, text="Directus username:")
        label_username.pack()
        entry_username = tk.Entry(self.new_stat_cont_window, textvariable=self.username)
        entry_username.pack()

        label_password = tk.Label(self.new_stat_cont_window, text="Directus password:")
        label_password.pack()
        entry_password = tk.Entry(self.new_stat_cont_window, textvariable=self.password, show="*")
        entry_password.pack()

        # Number of labels
        number_label = tk.Label(self.new_stat_cont_window, text="Number of labels:")
        number_label.pack()
        number_entry = tk.Entry(self.new_stat_cont_window, textvariable=self.number)
        self.number.set(80)
        number_entry.pack()

        # Asks where to store the pdf
        output_label = tk.Label(self.new_stat_cont_window, text="Select pdf output path:")
        output_label.pack()
        self.output_button = tk.Button(
            self.new_stat_cont_window, text="select path", width=17, command=self.output_folder
        )
        self.output_button.pack()

        # Frame for action buttons
        frame_submit = tk.Frame(self.new_stat_cont_window)
        frame_submit.pack(pady=(50, 0))

        # Submit button
        button_submit = tk.Button(frame_submit, text="Submit", width=17, command=self.test_connection)
        button_submit.pack(side="left")

        # Back to main button
        button_back = tk.Button(frame_submit, text="Back to Main Page", width=17, command=self.on_exit)
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
        self.new_stat_cont_window.destroy()
        self.root.deiconify()

    # Function to open the labels link when user clicks ont the information label
    def open_link(self, event: Event) -> None:
        webbrowser.open_new("https://www.avery.co.uk/product/mini-multipurpose-labels-l4732rev-25")

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
        except:
            number_value = 0

        # Check if output directory has been selected
        try:
            if self.output_dir:
                output = self.output_dir
            else:
                output = "empty"

        except:
            output = "empty"

        # Check that user entered the correct values
        if self.username.get() and self.password.get() and number_value > 0 and output != "empty":
            # Retrieve the entered values
            os.environ["USERNAME"] = self.username.get()
            os.environ["PASSWORD"] = self.password.get()
            os.environ["NUMBER"] = str(self.number.get())
            os.environ["OUTPUT_FOLDER"] = self.output_dir

            # Define the Directus base URL
            base_url = "http://directus.dbgi.org"

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
                create_new_stat_cont.main(self.new_stat_cont_window, self.root, self.label)

            # If connection to directus failed, informs the user that connection failed.
            else:
                self.label.config(
                    text="Connexion to directus failed, verify your credentials/vpn connection", foreground="red"
                )

        elif (not self.username.get() or not self.password.get()) and number_value > 0 and output != "empty":
            # If user didn't enter username or password
            self.label.config(text="Please provide correct Directus credentials!", foreground="red")

        elif self.username.get() and self.password.get() and number_value == 0 and output != "empty":
            # If user enter a bad label number (for example text or 0)
            self.label.config(text="Please provide a correct number of labels!", foreground="red")

        elif self.username.get() and self.password.get() and number_value > 0 and output == "empty":
            # If user didn't select an output dir
            self.label.config(text="Please select the output directory!", foreground="red")

        else:
            # If there are multiple parameters errors
            self.label.config(text="Multiple parameters errors!", foreground="red")


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

        # Create a variable to store the entered text
        self.number_ext = tk.StringVar(None)
        self.number_inj = tk.StringVar(None)
        self.parambig = tk.IntVar(None)
        self.paramsmall = tk.IntVar(None)

        # Create a frame for the informations
        frame_info = tk.Frame(self.csv_labels_window)
        frame_info.pack(pady=(10, 20))

        # Adds the information label
        self.label = tk.Label(
            frame_info,
            text="Generates avery L4732 (https://www.avery.co.uk/product/mini-multipurpose-labels-l4732rev-25) or L4731 (https://www.avery.co.uk/product/mini-multipurpose-labels-l4731rev-25) labels from a CSV",
            cursor="hand2",
        )
        self.label.pack()

        # Makes the link clickable
        self.label.bind("<Button-1>", self.open_link)

        # Create information and warning labels
        self.label = tk.Label(self.csv_labels_window, text="Print labels using a CSV")
        self.label.pack()

        import_label = tk.Label(
            self.csv_labels_window, text="CSV is expected to have a unique column containing codes, without header."
        )
        import_label.pack()

        warning_label = tk.Label(
            self.csv_labels_window,
            text="Be careful, this mode doesn't verify that labels are unique and doesn't enter them into Directus.",
            foreground="orange",
        )
        warning_label.pack()

        # Create button to import the CSV
        self.import_button = tk.Button(self.csv_labels_window, text="Import your CSV", command=self.import_csv)
        self.import_button.pack()

        # Create elements to select output directory
        output_label = tk.Label(self.csv_labels_window, text="Select the output path for the pdf files")
        output_label.pack()

        self.output_button = tk.Button(self.csv_labels_window, text="select path", command=self.output_folder)
        self.output_button.pack()

        # Create tickboxes to select the type of labels
        check_big = tk.Checkbutton(self.csv_labels_window, text="big labels (avery L4732)", variable=self.parambig)
        check_big.pack()

        check_small = tk.Checkbutton(
            self.csv_labels_window, text="small labels (avery L4731)", variable=self.paramsmall
        )
        check_small.pack()

        # Frame for action buttons
        frame_submit = tk.Frame(self.csv_labels_window)
        frame_submit.pack(pady=(50, 0))

        # Submit button
        button_submit = tk.Button(frame_submit, text="Submit", command=self.submit_result)
        button_submit.pack(side="left")

        # Back to main button
        button_back = tk.Button(frame_submit, text="Back to Main Page", command=self.on_exit)
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

    # Function to open the labels link when user clicks ont the information label
    def open_link(self, event: Event) -> None:
        webbrowser.open_new("https://www.avery.co.uk/template-l4732")

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
            if self.csv_file:
                csv = self.csv_file
            else:
                csv = "empty"

        except:
            csv = "empty"

        # Check if output directory has been selected
        try:
            if self.output_dir:
                output = self.output_dir
            else:
                output = "empty"

        except:
            output = "empty"

        # Check that user entered the correct values
        if (self.parambig.get() != 0 or self.paramsmall.get() != 0) and csv != "empty" and output != "empty":
            # Add size parameters to environment
            os.environ["PARAMBIG"] = str(self.parambig.get())
            os.environ["PARAMSMALL"] = str(self.paramsmall.get())
            os.environ["FILE_PATH"] = self.csv_file
            os.environ["OUTPUT_FOLDER"] = self.output_dir
            create_labels_csv.main(self.csv_labels_window, self.root, self.label)

        elif (self.parambig.get() != 0 or self.paramsmall.get() != 0) and csv == "empty" and output != "empty":
            # If no CSV selected
            self.label.config(text="Please select a CSV!", foreground="red")

        elif (self.parambig.get() != 0 or self.paramsmall.get() != 0) and csv != "empty" and output == "empty":
            # If no output dir selected
            self.label.config(text="Please select the output directory!", foreground="red")

        elif self.parambig.get() == 0 and self.paramsmall.get() == 0 and csv != "empty" and output != "empty":
            # If no label format selected
            self.label.config(text="Please select at least one label format!", foreground="red")

        else:
            # If there are multiple parameters errors
            self.label.config(text="Multiple parameters errors!", foreground="red")


class newSite(tk.Frame):
    def __init__(self, new_site_window: tk.Toplevel, root: tk.Tk):
        """
        Initializes an instance of the class.

        Args:
            csv_labels_window(tk.Toplevel): The parent widget where this frame will be placed.
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

        # Create a variable to store the entered text
        self.username = tk.StringVar(None)
        self.password = tk.StringVar(None)

        # Create information label
        self.label = tk.Label(self.new_site_window, text="Register a new site")
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
            label_username = tk.Label(self.new_site_window, text="Your directus username:")
            label_username.pack()
            entry_username = tk.Entry(self.new_site_window, textvariable=self.username)
            entry_username.pack()

            label_password = tk.Label(self.new_site_window, text="Your directus password:")
            label_password.pack()
            entry_password = tk.Entry(self.new_site_window, textvariable=self.password, show="*")
            entry_password.pack()

            # Create the country selection box
            label_country = tk.Label(self.new_site_window, text="Search for a country")
            label_country.pack()

            self.combobox_country = ttk.Combobox(self.new_site_window)
            self.combobox_country.pack()

            self.listbox_country = tk.Listbox(self.new_site_window, height=3, width=50, font=("Helvetica", 10))
            self.listbox_country.pack()

            # Create the university selection box
            label_university = tk.Label(self.new_site_window, text="Search for a university")
            label_university.pack()

            self.combobox_university = ttk.Combobox(self.new_site_window)
            self.combobox_university.pack()

            self.listbox_university = tk.Listbox(self.new_site_window, height=3, width=50, font=("Helvetica", 10))
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
            self.label_info = tk.Label(self.new_site_window, text="Selected site:")
            self.label_info.pack()

            # Create the frame for action buttons
            frame_submit = tk.Frame(self.new_site_window)
            frame_submit.pack(pady=(50, 0))

            # Submit button
            button_submit = tk.Button(frame_submit, text="Submit", width=17, command=self.test_connection)
            button_submit.pack(side="left")

            # Back to main button
            button_back = tk.Button(frame_submit, text="Back to Main Page", width=17, command=self.on_exit)
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
            if self.selected_country:
                country = self.selected_country
            else:
                country = "empty"

        except:
            country = "empty"

        # Check if a country has been selected
        try:
            if self.selected_university:
                university = self.selected_university
            else:
                university = "empty"

        except:
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
            base_url = "http://directus.dbgi.org"

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
                create_new_site.main(self.new_site_window, self.root, self.label)

            # If connection to directus failed, informs the user that connection failed.
            else:
                self.label.config(
                    text="Connexion to directus failed, verify your credentials/vpn connection", foreground="red"
                )

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
root.minsize(600, 300)

# Create the main page
main_page = MainPage(root)
main_page.pack()

root.mainloop()
