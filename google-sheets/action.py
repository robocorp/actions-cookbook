
from robocorp.actions import action
from RPA.Cloud.Google import Google

google = Google()
creds = "credentials.json"
sheet_id = "YOUR_SHEET_ID_HERE"


@action(is_consequential=False)
def get_google_spreadsheet_schema() -> str:
    """
    Action to get necessary information to be able to work with a Google Sheet Spreadsheets correctly.
    Use this action minimumn once before anything else, so that you will learn about the structure
    of the Spreadsheet. It will contain one or more Sheets, and the method will return the first few rows
    of each Sheet as an example.

    Returns:
        str: Names of the sheets, and a couple of first rows from each sheet to explain the context.
    """

    google.init_sheets(creds)

    spreadsheet = google.get_spreadsheet_basic_information(sheet_id)
    output = "Here are the sheets and their first rows. You can print the headers to user but not any other row values.\n\n"

    for sheet in spreadsheet["sheets"]:

        result = google.get_all_sheet_values(sheet_id, sheet["title"])
        output += f"SHEET NAME: {sheet['title']}\n"

        if "values" in result:
            # Handle the situation with less than 5 rows.
            number_of_rows = len(result["values"])
            for i in range(min(5, number_of_rows)):
                row = result["values"][i]
                row_string = ", ".join(map(str, row))
                output += row_string + "\n"
            output += "\n"
        else:
            output += "Empty sheet\n"

    return output


@action(is_consequential=False)
def create_new_google_sheet(name: str) -> str:
    """
    Creates a new empty Sheet in user's Google Spreadsheet.

    Args:
        name (str): Name of the Sheet. You must refer to this Sheet name later when adding or reading date from the Sheet.

    Returns:
        str: True if operation was success, and False if it failed.
    """
    google.init_sheets(creds)
    
    try:
        result = google.create_sheet(sheet_id, name)
    except:
        return "False"
    
    return "True"


@action(is_consequential=False)
def add_sheet_rows(sheet: str, rows: str) -> str:
    """
    Action to add multiple rows to the Google sheet. You need to specify witch sheet first. Get the sheets with get_google_spreadsheet_schema
    if you don't know the names or data structure.  Make sure the values are in correct columns (needs to be ordered the same as you have
    seen in the sample). Strictly adhere to the schema. Do not add any example data, just the values that needs to be added to the sheet rows.
    
    Args:
        sheet (str): Name of the sheet where the data is added to
        rows (str): Values for the new row separated by comma. Example of one row: "John,Doe,john.doe@example.com, 600000". Do not use commas in the content, including the numbers. Separate rows with newline character.

    Returns:
        str: The result of the operation.
    """

    google.init_sheets(creds)

    lines = rows.splitlines()

    for line in lines:

        values = line.split(",")
        values_list = [values]

        # Create variable 'range_string' based on the amount of list items.
        # 4 items -> "A:D"...
        start_ascii = ord("A")
        end_ascii = start_ascii + len(values) - 1
        range_string = f"{sheet}!A:{chr(end_ascii)}"
        google.insert_sheet_values(sheet_id, range_string, values_list, "ROWS")

    return "Row(s) were successfully added"


@action(is_consequential=False)
def get_sheet_contents(sheet: str) -> str:
    """
    Get all content from the chosen Google Spreadsheet Sheet.

    Args:
        sheet (str): Name of the sheet from which to get the data

    Returns:
        str: Sheet data as string, rows separated by newlines
    """

    google.init_sheets(creds)
    try:
        result = google.get_all_sheet_values(sheet_id, sheet)
    except:
        return "Sheet not found"

    output = f"Your sheet {sheet} contains following rows:\n\n"

    if "values" in result:
        # Limited to max 100 rows for now
        number_of_rows = len(result["values"])
        for i in range(min(100, number_of_rows)):
            row = result["values"][i]
            row_string = ", ".join(map(str, row))
            output += row_string + "\n"
        output += "\n"
    else:
        output += "Empty sheet\n"

    return output
