def create_txt(summary):
    filename = "summary.txt"

    with open(
        filename,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(summary)
        
    return filename