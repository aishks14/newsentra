from fpdf import FPDF

def create_pdf(summary):
    pdf = FPDF()

    pdf.add_page()

    pdf.add_font(
        "DejaVu",
        "",
        "fonts/DejaVuSans.ttf",
        uni=True
    )

    pdf.set_font(
        "DejaVu",
        size=12
    )

    pdf.multi_cell(
        0,
        10,
        summary
    )

    file_name = "summary.pdf"
    pdf.output(file_name)
    return file_name