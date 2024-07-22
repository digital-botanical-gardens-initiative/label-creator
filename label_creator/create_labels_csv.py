import math
import os
import tkinter as tk
from typing import Any

import pandas as pd
import qrcode
from pandas import DataFrame
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas


def main(csv_labels_window: tk.Toplevel, root: tk.Tk, label: tk.Label) -> None:
    # Load variables
    file_path = os.environ.get("FILE_PATH")
    output_folder = os.environ.get("OUTPUT_FOLDER")
    parambig = os.environ.get("PARAMBIG")
    paramsmall = os.environ.get("PARAMSMALL")

    df = pd.read_csv(file_path, header=None)
    df["char_length"] = df[0].apply(lambda x: calculate_text_width(x, "Helvetica", 14))

    values = df[0].tolist()

    if parambig == "1":
        create_big_labels_pdf(df, values, output_folder)

    if paramsmall == "1":
        create_small_labels_pdf(df, values, output_folder)

    csv_labels_window.destroy()
    root.destroy()


def calculate_text_width(text: str, font_name: str, font_size: int) -> Any:
    root = tk.Tk()
    test_label = tk.Label(root, text=text, font=(font_name, font_size))
    test_label.pack()
    width_pixels = test_label.winfo_reqwidth()
    root.destroy()

    pixels_per_inch = get_screen_ppi()
    width_cm = width_pixels / (pixels_per_inch * (1 / 2.54))
    return width_cm


def get_screen_ppi() -> Any:
    root = tk.Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    screen_diagonal_pixels = math.sqrt(screen_width**2 + screen_height**2)
    screen_diagonal_inches = math.sqrt(
        (screen_width / root.winfo_fpixels("1i")) ** 2 + (screen_height / root.winfo_fpixels("1i")) ** 2
    )
    ppi = screen_diagonal_pixels / screen_diagonal_inches
    root.destroy()
    return ppi


def create_big_labels_pdf(df: DataFrame, values: list, output_folder: str) -> None:
    # Split values into groups of 80 (number of labels per page)
    value_groups = [values[i : i + 80] for i in range(0, len(values), 80)]

    # Set up the pdf canvas
    pdf_path = os.path.join(output_folder, "big_labels_generated.pdf")
    pdf = canvas.Canvas(pdf_path, pagesize=A4)

    # Set the dimensions of the labels in centimeters
    label_width_cm = 3.56 * cm
    label_height_cm = 1.69 * cm

    # Set the spacing between labels
    x_spacing = label_width_cm + 0.27 * cm
    y_spacing = label_height_cm

    # Set the initial position for drawing
    x_start = 0.2 * cm
    y_start = A4[1] - 1.33 * cm

    # Set the size of the QR box
    box_size = 13.5

    # Iterate over the value groups
    for group in value_groups:
        # Calculate the number of rows needed for this group
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

            # Retriev character length for each value
            char_length = df["char_length"][i]

            # launches the correct function depending on the character length
            if char_length <= 1.9:
                draw_label_and_qr_code(
                    pdf=pdf,
                    value=value,
                    pos_x=pos_x + 0.07 * cm,
                    pos_y=pos_y + 0.6 * cm,
                    font_size=8,
                    qr_pos_x_offset=1.5 * cm,
                    qr_pos_y_offset=0.3 * cm,
                    box_size=box_size,
                )
            elif 1.9 < char_length <= 3.8:
                draw_label_in_two_lines(
                    pdf=pdf,
                    value=value,
                    pos_x1=pos_x + 0.07 * cm,
                    pos_x2=pos_x + 0.07 * cm,
                    pos_y1=pos_y + 0.8 * cm,
                    pos_y2=pos_y + 0.45 * cm,
                    font_size=8,
                    qr_pos_x_offset=0.5 * cm,
                    box_size=box_size,
                )
            elif 3.8 < char_length <= 7:
                draw_label_in_two_lines(
                    pdf=pdf,
                    value=value,
                    pos_x1=pos_x + 0.07 * cm,
                    pos_x2=pos_x + 0.07 * cm,
                    pos_y1=pos_y + 0.8 * cm,
                    pos_y2=pos_y + 0.45 * cm,
                    font_size=8,
                    qr_pos_x_offset=0.5 * cm,
                    box_size=box_size,
                )
            elif 7 < char_length <= 9.5:
                draw_label_in_three_lines(
                    pdf=pdf,
                    value=value,
                    pos_x1=pos_x,
                    pos_x2=pos_x,
                    pos_x3=pos_x,
                    pos_y1=pos_y,
                    pos_y2=pos_y,
                    pos_y3=pos_y,
                    font_size=8,
                    box_size=box_size,
                )
            else:
                draw_truncated_label(pdf, value, pos_x, pos_y, 7, 8, 1.35 * cm, box_size)

        pdf.showPage()

    pdf.save()


def create_small_labels_pdf(df: DataFrame, values: list, output_folder: str) -> None:
    value_groups = [values[i : i + 189] for i in range(0, len(values), 189)]
    pdf_path = os.path.join(output_folder, "small_labels_generated.pdf")
    pdf = canvas.Canvas(pdf_path, pagesize=A4)

    label_width_cm = 2.54 * cm
    label_height_cm = 0.999 * cm
    x_spacing = label_width_cm + 0.25 * cm
    y_spacing = label_height_cm

    x_start = 0.1 * cm
    y_start = A4[1] - 1.46 * cm

    box_size = 8

    for group in value_groups:
        num_rows = (len(group) - 1) // 7 + 1
        num_cols = min(len(group), 7)
        total_width = num_cols * x_spacing
        total_height = num_rows * y_spacing
        x = x_start + (A4[0] - total_width) / 2
        y = y_start - total_height

        for i, value in enumerate(group):
            pos_x = x + (i % 7) * x_spacing
            pos_y = y + (i // 7) * y_spacing
            char_length = df["char_length"][i]

            if char_length <= 1.9:
                draw_label_and_qr_code(
                    pdf=pdf,
                    value=value,
                    pos_x=pos_x + 0.07 * cm,
                    pos_y=pos_y + 0.6 * cm,
                    font_size=8,
                    qr_pos_x_offset=1.5 * cm,
                    qr_pos_y_offset=0.3 * cm,
                    box_size=box_size,
                )
            elif 1.9 < char_length <= 3.6:
                draw_label_in_two_lines(
                    pdf=pdf,
                    value=value,
                    pos_x1=pos_x + 0.07 * cm,
                    pos_x2=pos_x + 0.07 * cm,
                    pos_y1=pos_y + 0.8 * cm,
                    pos_y2=pos_y + 0.45 * cm,
                    font_size=8,
                    qr_pos_x_offset=0.5 * cm,
                    box_size=box_size,
                )
            elif 3.6 < char_length <= 7:
                draw_label_in_three_lines(
                    pdf=pdf,
                    value=value,
                    pos_x1=pos_x,
                    pos_x2=pos_x,
                    pos_x3=pos_x,
                    pos_y1=pos_y,
                    pos_y2=pos_y,
                    pos_y3=pos_y,
                    font_size=8,
                    box_size=box_size,
                )
            elif 7 < char_length <= 9.2:
                draw_label_in_three_lines(
                    pdf=pdf,
                    value=value,
                    pos_x1=pos_x,
                    pos_x2=pos_x,
                    pos_x3=pos_x,
                    pos_y1=pos_y,
                    pos_y2=pos_y,
                    pos_y3=pos_y,
                    font_size=8,
                    box_size=box_size,
                )
            else:
                draw_truncated_label(
                    pdf=pdf, value=value, pos_x=pos_x, pos_y=pos_y, font_size=6, max_chars=7, box_size=box_size
                )

        pdf.showPage()

    pdf.save()


def draw_label_and_qr_code(
    pdf: Any,
    value: str,
    pos_x: str,
    pos_y: str,
    font_size: int,
    qr_pos_x_offset: str,
    qr_pos_y_offset: str,
    box_size: float,
) -> None:
    pdf.setFont("Helvetica", font_size)
    pdf.drawString(pos_x, pos_y, value)
    draw_qr_code(pdf, value, pos_x + qr_pos_x_offset, pos_y + qr_pos_y_offset, box_size)


def draw_qr_code(pdf: Any, value: str, pos_x: str, pos_y: str, box_size: float) -> None:
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=box_size,
        border=1,
    )
    qr.add_data(value)
    qr.make(fit=True)
    img = qr.make_image(fill="black", back_color="white")

    img_path = f"{value}.png"
    img.save(img_path)

    pdf.drawImage(img_path, pos_x, pos_y, qr_size, qr_size)
    os.remove(img_path)


def draw_label_in_two_lines(
    pdf: Any, value: str, pos_x1: str, pos_x2: str, pos_y1: str, pos_y2: str, font_size: int, box_size: float
) -> None:
    semi_length = round(len(value) / 2)
    pdf.setFont("Helvetica", font_size)
    pdf.drawString(pos_x1, pos_y1, value[:semi_length])
    pdf.drawString(pos_x2, pos_y2, value[semi_length:])
    draw_qr_code(pdf, value, pos_x + 1.9 * cm, pos_y + 0.2 * cm, qr_size, box_size)


def draw_label_in_three_lines(
    pdf: Any,
    value: str,
    pos_x1: str,
    pos_x2: str,
    pos_x3,
    pos_y1: str,
    pos_y2: str,
    pos_y3: str,
    font_size: int,
    box_size: float,
) -> None:
    third_length = round(len(value) / 3)
    pdf.setFont("Helvetica", font_size)
    pdf.drawString(pos_x1 + 0.07 * cm, pos_y1 + 1.2 * cm, value[:third_length])
    pdf.drawString(pos_x2 + 0.07 * cm, pos_y2 + 0.8 * cm, value[third_length : 2 * third_length])
    pdf.drawString(pos_x3 + 0.07 * cm, pos_y3 + 0.4 * cm, value[2 * third_length :])
    draw_qr_code(pdf, value, pos_x + 1.9 * cm, pos_y + 0.2 * cm, qr_size, box_size)


def draw_truncated_label(
    pdf: Any, value: str, pos_x: str, pos_y: str, font_size: int, max_chars: int, box_size: float
) -> None:
    truncated_value = value[:max_chars] + "..."
    pdf.setFont("Helvetica", font_size)
    pdf.drawString(pos_x + 0.07 * cm, pos_y + 0.8 * cm, truncated_value)
    draw_qr_code(pdf, truncated_value, pos_x + 1.9 * cm, pos_y + 0.2 * cm, qr_size, box_size)
