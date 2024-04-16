# To convert this script into a .exe file: pyinstaller --onefile label_creator.py in anaconda prompt

import os
import tkinter as tk
from tkinter import filedialog
from typing import Any
import webbrowser

import requests
import create_new_labels


class MainPage(tk.Frame):
    def __init__(self, parent:tk.Tk, *args: Any, **kwargs: Any):
        """
        Initializes an instance of the class.

        Args:
            parent(tk.Tk): The parent widget or window where this frame will be placed.
            csv_path(str): CSV path and name.

        Returns:
            None
        """
        
        tk.Frame.__init__(self, parent, *args, **kwargs)

        # Create widgets for the main page

        # To create labels
        label_labels = tk.Label(self, text="Create labels")
        label_labels.pack()

        button_new_labels = tk.Button(self, text="Generate labels from scratch", width = 40, command=self.open_new_labels)
        button_new_labels.pack()

        button_mobile_container = tk.Button(self, text="Generate mobile containers labels from scratch", width = 40, command=self.open_mobile_container)
        button_mobile_container.pack()

        button_static_container = tk.Button(
            self, text="Generate static containers labels from scratch", width = 40, command=self.open_static_container)
        button_static_container.pack()

        button_existing= tk.Button(self, text="Print already existing labels from a table", width = 40, command=self.open_existing_label)
        button_existing.pack()

        # Add some space to discriminate label generation from adding a new site
        label_space = tk.Label(self, text="")
        label_space.pack()

        label_space = tk.Label(self, text="")
        label_space.pack()

        # to add a new site
        label_new_site = tk.Label(self, text="Add a new site to the database")
        label_new_site.pack()

        button_new_site = tk.Button(self, text="Add a new site", width = 40, command=self.open_new_site)
        button_new_site.pack()

    def open_new_labels(self):
        # Create a new Toplevel window for the new labels
        new_labels_window = tk.Toplevel(root)
        new_labels_window.title("Generate new labels")
        newLabels(new_labels_window, root)

    def open_mobile_container(self):
        # Hide the main page and open Window 2
        self.pack_forget()
        window1 = Window2(self.master)
        window1.pack()

    def open_static_container(self):
        # Hide the main page and open Window 3
        self.pack_forget()
        window3 = Window3(self.master)
        window3.pack()

    def open_existing_label(self):
        # Hide the main page and open Window 4
        self.pack_forget()
        window4 = Window4(self.master)
        window4.pack()

    def open_new_site(self):
        # Hide the main page and open Window 4
        self.pack_forget()
        window_static_container = WindowStaticContainer(self.master)
        window_static_container.pack()


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
        self.new_labels_window = new_labels_window
        self.root = root

        # Hide main page
        self.root.withdraw()

        self.new_labels_window.protocol("WM_DELETE_WINDOW", self.on_exit)

        # Create a variable to store the entered text
        self.username = tk.StringVar(None)
        self.password = tk.StringVar(None)
        self.number = tk.IntVar(None)
        self.project = tk.StringVar(None)

        frame_info = tk.Frame(self.new_labels_window)
        frame_info.pack(pady=(10, 20))

        # Create widgets for the main page
        self.label = tk.Label(frame_info, text="Generates avery L4732 (https://www.avery.co.uk/template-l4732) labels and reserves the codes in directus", cursor="hand2")
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

        #Extract the project names from directus
        collection_url = "http://directus.dbgi.org/items/EMI_codes"
        column = 'emi_code'
        params = {'sort[]': f'{column}'}
        session = requests.Session()
        response = session.get(collection_url, params=params)
        data = response.json()['data']
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
        button_submit = tk.Button(frame_submit, text="Submit", width=17, command=self.show_values)
        button_submit.pack(side="left")

        # Back to main button
        button_back = tk.Button(frame_submit, text="Back to Main Page", width=17, command=self.on_exit)
        button_back.pack(side="right")

    def on_exit(self) -> None:
        """
        Defines behaviour when user quits this window (by x button or specified button).

        Args:
            None

        Returns:
            None
        """
        self.new_labels_window.destroy()
        self.root.deiconify()

    def open_link(self, event):
        webbrowser.open_new("https://www.avery.co.uk/template-l4732")

    def output_folder(self) -> None:
        """
        Asks the user to choose the output folder where PDF will be written.

        Args:
            None

        Returns:
            None
        """
        output_folder = filedialog.askdirectory()
        if output_folder:
            os.environ["OUTPUT_FOLDER"] = output_folder
            parts = output_folder.split("/")
            folder = parts[-1]
            self.output_button.config(text=folder)

    def show_values(self) -> None:
        """
        Stores all the parameters to the environment when user confirms his choice.

        Args:
            clicked_button(str): A string ("new" or "csv"), that defines which window will be launched after home page.

        Returns:
            None
        """

        # Retrieve the entered values
        os.environ["USERNAME"] = self.username.get()
        os.environ["PASSWORD"] = self.password.get()
        os.environ["NUMBER"] = str(self.number.get())
        os.environ["PROJECT"] = self.project.get()
        self.test_connection()

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
        username = os.environ.get("USERNAME")
        password = os.environ.get("PASSWORD")
        number = os.environ.get("NUMBER")
        output_folder = os.environ.get("OUTPUT_FOLDER")
        project = os.environ.get("PROJECT")

        if (
            username
            and password
            and number
            and output_folder
            and project
        ):
            # Define the Directus base URL
            base_url = "http://directus.dbgi.org"

            # Define the login endpoint URL
            login_url = base_url + "/auth/login"
            # Create a session object for making requests
            session = requests.Session()
            # Send a POST request to the login endpoint
            response = session.post(login_url, json={"email": username, "password": password})
            # Test if connection is successful
            if response.status_code == 200:
                # Stores the access token
                data = response.json()["data"]
                access_token = data["access_token"]
                os.environ["ACCESS_TOKEN"] = str(access_token)
                create_new_labels.main(self.new_labels_window, self.root)

            # If connection to directus failed, informs the user that connection failed.
            else:
                self.label.config(
                    text="Connexion to directus failed, verify your credentials/vpn connection", foreground="red"
                )

        else:
            # If user didn't enter all necessary values, shows this message
            self.label.config(text="Please provide all asked values", foreground="red")



class Window2(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        # Create a variable to store the entered text
        self.username = tk.StringVar(None)
        self.password = tk.StringVar(None)
        self.number_rows = tk.IntVar(None)
        self.number_cols = tk.IntVar(None)
        self.number = tk.IntVar(None)
        self.location = tk.StringVar(None)
        self.storage = tk.StringVar(None)

        # Create widgets for the main page
        label = tk.Label(self, text="Generate mobile containers labels from scratch")
        label.pack()

        # Create text entry fields
        label_username = tk.Label(self, text="Your directus username:")
        label_username.pack()
        entry_username = tk.Entry(self, textvariable=self.username)
        entry_username.pack()

        label_password = tk.Label(self, text="Your directus password:")
        label_password.pack()
        entry_password = tk.Entry(self, textvariable=self.password, show="*")
        entry_password.pack()

        # Nuber of rows
        number_rows = tk.Label(self, text="Container's rows number:")
        number_rows.pack()
        number_entry_rows = tk.Entry(self, textvariable=self.number_rows)
        number_entry_rows.pack()

        # Nuber of columns
        number_columns = tk.Label(self, text="Container's columns number:")
        number_columns.pack()
        number_entry_columns = tk.Entry(self, textvariable=self.number_cols)
        number_entry_columns.pack()

        # Number of labels
        number_label = tk.Label(self, text="Number of labels you want:")
        number_label.pack()
        number_entry = tk.Entry(self, textvariable=self.number)
        number_entry.pack()

        output_label = tk.Label(self, text="Select the output path for the pdf file")
        output_label.pack()
        output_button = tk.Button(self, text="select path", command=self.output_folder)
        output_button.pack()

        button_submit = tk.Button(self, text="Submit", command=self.show_values)
        button_submit.pack()

        button_back = tk.Button(self, text="Back to Main Page", command=self.back_to_main)
        button_back.pack()

    def back_to_main(self):
        # Destroy Window 2 and show the main page
        self.destroy()
        main_page.pack()

    def output_folder(self):
        os.environ["output_folder"] = filedialog.askdirectory()

    def show_values(self):
        # Retrieve the entered values
        os.environ["username"] = self.username.get()
        os.environ["password"] = self.password.get()
        os.environ["number_rows"] = str(self.number_rows.get())
        os.environ["number_cols"] = str(self.number_cols.get())
        os.environ["number"] = str(self.number.get())
        os.environ["location"] = self.location.get()
        os.environ["storage"] = self.storage.get()
        self.master.destroy()
        gui_Processing_mobile_containers.main()


class WindowStaticContainer(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        # Create a variable to store the entered text
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.number_rows = tk.IntVar()
        self.number_cols = tk.IntVar()
        self.number = tk.IntVar()
        self.location = tk.StringVar()
        self.storage = tk.StringVar()

        # Create widgets for the main page
        label = tk.Label(self, text="Generate static containers labels from scratch")
        label.pack()

        # Create text entry fields
        label_username = tk.Label(self, text="Your directus username:")
        label_username.pack()
        entry_username = tk.Entry(self, textvariable=self.username)
        entry_username.pack()

        label_password = tk.Label(self, text="Your directus password:")
        label_password.pack()
        entry_password = tk.Entry(self, textvariable=self.password, show="*")
        entry_password.pack()

        # Number of labels
        number_label = tk.Label(self, text="Number of labels you want:")
        number_label.pack()
        number_entry = tk.Entry(self, textvariable=self.number)
        number_entry.pack()

        # Where the labels will be stored
        storage_label = tk.Label(self, text="Storage location:")
        storage_label.pack()
        storages = ["University of Fribourg", "Université de Neuchâtel"]
        dropdown_storage = tk.OptionMenu(self, self.storage, *storages)
        dropdown_storage.pack()

        output_label = tk.Label(self, text="Select the output path for the pdf file")
        output_label.pack()
        output_button = tk.Button(self, text="select path", command=self.output_folder)
        output_button.pack()

        button_submit = tk.Button(self, text="Submit", command=self.show_values)
        button_submit.pack()

        button_back = tk.Button(self, text="Back to Main Page", command=self.back_to_main)
        button_back.pack()

    def back_to_main(self):
        # Destroy Window 2 and show the main page
        self.destroy()
        main_page.pack()

    def output_folder(self):
        os.environ["output_folder"] = filedialog.askdirectory()

    def show_values(self):
        # Retrieve the entered values
        os.environ["username"] = self.username.get()
        os.environ["password"] = self.password.get()
        os.environ["number_rows"] = str(self.number_rows.get())
        os.environ["number_cols"] = str(self.number_cols.get())
        os.environ["number"] = str(self.number.get())
        os.environ["location"] = self.location.get()
        os.environ["storage"] = self.storage.get()
        self.master.destroy()
        gui_Processing_static_containers.main()


class Window3(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        # Create a variable to store the entered text
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.number = tk.IntVar()
        self.location = tk.StringVar()
        self.storage = tk.StringVar()

        # Create widgets for the main page
        label = tk.Label(self, text="Register a new site")
        label.pack()

        # Create text entry fields
        label_username = tk.Label(self, text="Your directus username:")
        label_username.pack()
        entry_username = tk.Entry(self, textvariable=self.username)
        entry_username.pack()

        label_password = tk.Label(self, text="Your directus password:")
        label_password.pack()
        entry_password = tk.Entry(self, textvariable=self.password, show="*")
        entry_password.pack()

        button_submit = tk.Button(self, text="Submit", command=self.show_values)
        button_submit.pack()

        button_back = tk.Button(self, text="Back to Main Page", command=self.back_to_main)
        button_back.pack()

    def back_to_main(self):
        # Destroy Window 2 and show the main page
        self.destroy()
        main_page.pack()

    def output_folder(self):
        os.environ["output_folder"] = filedialog.askdirectory()

    def show_values(self):
        # Retrieve the entered values
        os.environ["username"] = self.username.get()
        os.environ["password"] = self.password.get()
        self.master.destroy()
        gui_Select_university.main()


class Window4(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        # Create a variable to store the entered text
        self.number_ext = tk.StringVar()
        self.number_inj = tk.StringVar()
        self.parambig = tk.IntVar()
        self.paramsmall = tk.IntVar()

        # Create widgets for the main page
        label = tk.Label(self, text="Print already existing labels using a CSV")
        label.pack()

        import_label = tk.Label(self, text="CSV is expected to have a unique column containing codes, without header")
        import_label.pack()
        import_button = tk.Button(self, text="Import your CSV", command=self.import_csv)
        import_button.pack()

        output_label = tk.Label(self, text="Select the output path for the pdf files")
        output_label.pack()
        output_button = tk.Button(self, text="select path", command=self.output_folder)
        output_button.pack()

        # Choose big labels
        check_big = tk.Checkbutton(self, text="big labels (avery L4732)", variable=self.parambig)
        check_big.pack()

        # Choose small labels extraction
        check_small = tk.Checkbutton(self, text="small labels (avery L4731)", variable=self.paramsmall)
        check_small.pack()

        button_submit = tk.Button(self, text="Submit", command=self.show_values)
        button_submit.pack()

        button_back = tk.Button(self, text="Back to Main Page", command=self.back_to_main)
        button_back.pack()

    def import_csv(self):
        os.environ["file_path"] = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])

    def output_folder(self):
        os.environ["output_folder"] = filedialog.askdirectory()

    def back_to_main(self):
        # Destroy Window 2 and show the main page
        self.destroy()
        main_page.pack()

    def show_values(self):
        # Retrieve the entered values
        os.environ["parambig"] = str(self.parambig.get())
        os.environ["paramsmall"] = str(self.paramsmall.get())
        self.master.destroy()
        gui_Processing_existing.main()


# Create the main window
root = tk.Tk()
root.title("DBGI labels creator")
root.minsize(600, 300)

# Create the main page
main_page = MainPage(root)
main_page.pack()

root.mainloop()