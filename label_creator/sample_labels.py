import os
import tkinter as tk
from io import BytesIO

import pandas as pd
import qrcode
import requests
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas


def main(sample_labels_window: tk.Toplevel, root: tk.Tk, label_info: tk.Label, label_info_2: tk.Label) -> None:
    # Load variables
    number = int(str(os.environ.get("NUMBER")))
    output_folder = str(os.environ.get("OUTPUT_FOLDER"))
    access_token = os.environ.get("ACCESS_TOKEN")
    project = os.environ.get("PROJECT")
    label_size = int(str(os.environ.get("LABEL_SIZE")))

    # Define the Directus URLs
    field_name = "container_id"
    base_url = "https://emi-collection.unifr.ch/directus"
    collection_url = base_url + "/items/Containers"
    request_url = collection_url + f"?filter[{field_name}][_starts_with]={project}_&&limit=1"

    # Define session
    session = requests.Session()

    # Extract the last label entry
    params = {"sort[]": f"-{field_name}"}
    response = session.get(request_url, params=params)
    last_value = response.json()["data"][0][field_name] if response.json()["data"] else "null"

    # Retrieve the last number
    last_number = int(last_value.split("_")[1]) if last_value != "null" else 0

    # Define the first number of the list (last number + 1)
    first_number = last_number + 1

    # Create template dataframe to reserve labels
    row_data = {"reserved": "True"}

    # Create a dataframe with a row for each code requested by the user
    template = pd.DataFrame([row_data for _ in range(number)], columns=["reserved"])

    # Define containers as not used until they are used
    template["used"] = "False"

    # Define containers as finite
    template["is_finite"] = "True"

    # Generate the container IDs
    template["container_id"] = [f"{project}_" "{:06d}".format(first_number + i) for i in range(number)]

    # Define containers as present
    template["status"] = "present"

    # Define columns and rows capacity as 1, because it's sample containers
    template["columns"] = 1
    template["columns_numeric"] = "True"
    template["rows"] = 1
    template["rows_numeric"] = "True"

    # Create request headers
    headers = {"Content-Type": "application/json"}

    # Create a list with the asked codes beginning with the first number
    values = [f"{project}_{first_number + i:06d}" for i in range(number)]
    records = template.to_json(orient="records")

    # Add the codes to the database
    session.headers.update({"Authorization": f"Bearer {access_token}"})
    response = session.post(url=collection_url, headers=headers, data=records)

    if response.status_code == 200:
        # Launch correct process depending on the user choice
        if label_size == 1:
            create_big_labels_pdf(values, output_folder)
        elif label_size == 2:
            create_medium_labels_pdf(values, output_folder)
        elif label_size == 3:
            create_small_labels_pdf(values, output_folder)

        sample_labels_window.destroy()
        root.destroy()

    else:
        label_info.config(text=f"The request failed: {response.json()['errors'][0]['message']}.", foreground="red")
        label_info_2.config(text="")


def create_big_labels_pdf(values: list, output_folder: str) -> None:
    # Splitting the values into groups of 48 (number of labels per page)
    value_groups = [values[i : i + 48] for i in range(0, len(values), 48)]

    # Set up the PDF canvas
    pdf_path = f"{output_folder}/big_sample_labels_L4736.pdf"
    pdf = canvas.Canvas(pdf_path, pagesize=A4)

    # Set the font size and line height
    font_size = 16

    # Set the dimensions of the labels in centimeters
    label_width_cm = 4.57 * cm
    label_height_cm = 2.12 * cm

    # Set the spacing between labels
    x_spacing = label_width_cm + 0.27 * cm
    y_spacing = label_height_cm

    # Set the initial position for drawing
    x_start = 0.2 * cm
    y_start = A4[1] - 2.15 * cm

    # Iterate over the value groups
    for group in value_groups:
        # Calculate the number of rows and columns needed for this group
        num_rows = (len(group) - 1) // 4 + 1
        num_cols = min(len(group), 4)

        # Calculate the total width and height needed for this group
        total_width = num_cols * x_spacing
        total_height = num_rows * y_spacing

        # Calculate the starting position for this group
        x = x_start + (A4[0] - total_width) / 2
        y = y_start - total_height

        # Iterate over the values in the group
        for i, value in enumerate(group):
            # Calculate the position for drawing the value and QR code
            pos_x = x + (i % 4) * x_spacing
            pos_y = y + (i // 4) * y_spacing

            # Draw the label text
            pdf.setFont("Helvetica", font_size)
            pdf.drawString(pos_x + 0.55 * cm, pos_y + 1.1 * cm, value[:5])
            pdf.setFont("Helvetica", font_size)  # Reduce font size for the second line
            pdf.drawString(pos_x + 0.3 * cm, pos_y + 0.4 * cm, value[5:])

            # Draw the QR code
            qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=17.5, border=0)
            qr.add_data(value)
            qr.make(fit=True)
            qr_img = qr.make_image(fill_color="black", back_color="white")

            # Calculate the position for drawing the QR code
            qr_pos_x = pos_x + 2.5 * cm
            qr_pos_y = pos_y + 0.2 * cm

            # Draw the QR code
            qr_img_path = BytesIO()
            qr_img.save(qr_img_path, format="PNG")
            qr_img_path.seek(0)
            image = ImageReader(qr_img_path)
            pdf.drawImage(image, qr_pos_x, qr_pos_y, width=1.75 * cm, height=1.75 * cm)

        # Move to the next page
        pdf.showPage()

    # Save and close the PDF file
    pdf.save()
    qr_img_path.close()


def create_medium_labels_pdf(values: list, output_folder: str) -> None:
    # Splitting the values into groups of 80 (number of labels per page)
    value_groups = [values[i : i + 80] for i in range(0, len(values), 80)]

    # Set up the PDF canvas
    pdf_path = f"{output_folder}/medium_sample_labels_L4732.pdf"
    pdf = canvas.Canvas(pdf_path, pagesize=A4)

    # Set the font size and line height
    font_size = 12

    # Set the dimensions of the labels in centimeters
    label_width_cm = 3.56 * cm
    label_height_cm = 1.69 * cm

    # Set the spacing between labels
    x_spacing = label_width_cm + 0.27 * cm
    y_spacing = label_height_cm

    # Set the initial position for drawing
    x_start = 0.2 * cm
    y_start = A4[1] - 1.33 * cm

    # Iterate over the value groups
    for group in value_groups:
        # Calculate the number of rows and columns needed for this group
        num_rows = (len(group) - 1) // 5 + 1
        num_cols = min(len(group), 5)

        # Calculate the total width and height needed for this group
        total_width = num_cols * x_spacing
        total_height = num_rows * y_spacing

        # Calculate the starting position for this group
        x = x_start + (A4[0] - total_width) / 2
        y = y_start - total_height

        # Iterate over the values in the group
        for i, value in enumerate(group):
            # Calculate the position for drawing the value and QR code
            pos_x = x + (i % 5) * x_spacing
            pos_y = y + (i // 5) * y_spacing

            # Draw the label text
            pdf.setFont("Helvetica", font_size)
            pdf.drawString(pos_x + 0.55 * cm, pos_y + 0.9 * cm, value[:5])
            pdf.setFont("Helvetica", font_size)  # Reduce font size for the second line
            pdf.drawString(pos_x + 0.3 * cm, pos_y + 0.4 * cm, value[5:])

            # Draw the QR code
            qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=13.5, border=0)
            qr.add_data(value)
            qr.make(fit=True)
            qr_img = qr.make_image(fill_color="black", back_color="white")

            # Calculate the position for drawing the QR code
            qr_pos_x = pos_x + 1.9 * cm
            qr_pos_y = pos_y + 0.2 * cm

            # Draw the QR code
            qr_img_path = BytesIO()
            qr_img.save(qr_img_path, format="PNG")
            qr_img_path.seek(0)
            image = ImageReader(qr_img_path)
            pdf.drawImage(image, qr_pos_x, qr_pos_y, width=1.35 * cm, height=1.35 * cm)

        # Move to the next page
        pdf.showPage()

    # Save and close the PDF file
    pdf.save()
    qr_img_path.close()


def create_small_labels_pdf(values: list, output_folder: str) -> None:
    # Splitting the values into groups of 80 (number of labels per page)
    value_groups = [values[i : i + 189] for i in range(0, len(values), 189)]

    # Set up the PDF canvas
    pdf_path = f"{output_folder}/small_sample_labels_L4731.pdf"
    pdf = canvas.Canvas(pdf_path, pagesize=A4)

    # Set the font size and line height
    font_size = 8

    # Set the dimensions of the labels in centimeters
    label_width_cm = 2.54 * cm
    label_height_cm = 0.999 * cm

    # Set the spacing between labels
    x_spacing = label_width_cm + 0.25 * cm
    y_spacing = label_height_cm

    # Set the initial position for drawing
    x_start = 0.1 * cm
    y_start = A4[1] - 1.46 * cm

    # Iterate over the value groups
    for group in value_groups:
        # Calculate the number of rows and columns needed for this group
        num_rows = (len(group) - 1) // 7 + 1
        num_cols = min(len(group), 7)

        # Calculate the total width and height needed for this group
        total_width = num_cols * x_spacing
        total_height = num_rows * y_spacing

        # Calculate the starting position for this group
        x = x_start + (A4[0] - total_width) / 2
        y = y_start - total_height

        # Iterate over the values in the group
        for i, value in enumerate(group):
            # Calculate the position for drawing the value and QR code
            pos_x = x + (i % 7) * x_spacing
            pos_y = y + (i // 7) * y_spacing

            # Draw the label text
            pdf.setFont("Helvetica", font_size)
            pdf.drawString(pos_x + 0.4 * cm, pos_y + 0.7 * cm, value[:5])
            pdf.setFont("Helvetica", font_size)  # Reduce font size for the second line
            pdf.drawString(pos_x + 0.2 * cm, pos_y + 0.4 * cm, value[5:])

            # Draw the QR code
            qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=8, border=0)
            qr.add_data(value)
            qr.make(fit=True)
            qr_img = qr.make_image(fill_color="black", back_color="white")

            # Calculate the position for drawing the QR code
            qr_pos_x = pos_x + 1.5 * cm
            qr_pos_y = pos_y + 0.3 * cm

            # Draw the QR code
            qr_img_path = BytesIO()
            qr_img.save(qr_img_path, format="PNG")
            qr_img_path.seek(0)
            image = ImageReader(qr_img_path)
            pdf.drawImage(image, qr_pos_x, qr_pos_y, width=0.8 * cm, height=0.8 * cm)

        # Move to the next page
        pdf.showPage()

    # Save and close the PDF file
    pdf.save()
    qr_img_path.close()
