"""
WORD OF WARNING:

This action accesses your local folder (the one you choose) and reads all files from it.
When you connect the @action to an AI app like ChatGPT, your data will go there, too.

Be mindful which folder you give access to.
"""

from robocorp.actions import action
from RPA.FileSystem import FileSystem
from RPA.PDF import PDF


@action
def read_local_files() -> str:
    """Reads data from a local folder to add more context to LLMs knowledge. Takes no input arguments.
    
    Returns:
        str: All the text content of the files in the given local folder.
    """

    # ------------
    # CHANGE THIS! Update the below folder to be something on the machine you run the Action Server on.
    # ------------
    path = "/Users/WHOAREYOU/Desktop/available_to_ai/"
    file_system = FileSystem()
    pdf_reader = PDF()
    all_content = ""

    # Iterate over all files in the given folder
    for file_name in file_system.find_files(path + "/*"):

        ext = file_system.get_file_extension(file_name)
        # Handle .txt files
        if ext == ".txt":
            try:
                file_content = file_system.read_file(file_name)
                all_content += f"------ FILE: {file_name} ------\n{file_content}\n\n"
            except Exception as e:
                all_content += f"------ FILE: {file_name} ------\nAn error occurred while reading the .txt file: {e}\n\n"
        # Handle .txt files
        elif ext == ".pdf":
            try:
                # For the demo purposes, and to avoid any insanities,
                # extract text from ONLY the first page of the PDF
                pdf_content = pdf_reader.get_text_from_pdf(file_name, pages=1)
                all_content += f"------ FILE: {file_name} ------\n{pdf_content}\n\n"
            except Exception as e:
                all_content += f"------ FILE: {file_name} ------\nAn error occurred while reading the .pdf file: {e}\n\n"
    
    return all_content