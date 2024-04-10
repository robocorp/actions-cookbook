"""
AI Actions to interact with local Excel files.
NOTE: the file location is statically defined in the Package
"""

from robocorp.actions import action
from RPA.Excel.Files import Files
from typing import Annotated, List
from pydantic import BaseModel, Field

class Row(BaseModel):
    columns: Annotated[List[str], Field(description="The columns that make up the row")]

class RowData(BaseModel):
    rows: Annotated[List[Row], Field(description="The rows that need to be added")]

path = "my-excel.xlsx"

@action(is_consequential=False)
def get_excel_metadata() -> str:
    """
    Gets the list of worksheets in the excel file, and a few example rows of each of them. Use this action once
    to get context of what the user's excel file contains.

    Returns:
        str: List of worksheets and a few sample rows of each of them
    """
    excel = Files()
    excel.open_workbook(path)
    
    sheet_names = excel.list_worksheets()
    result = "Your excel sheet contains the following worksheets:\n\n"
    
    for sheet_name in sheet_names:
        sheet_data = excel.read_worksheet(sheet_name, header=True)
        # Get the first 3 rows, if available
        first_three_rows = sheet_data[:3] if len(sheet_data) >= 3 else sheet_data
        result += f"Sheet: {sheet_name} with total {len(sheet_data)} of rows.\nSample data: {first_three_rows}\n\n"
    
    excel.close_workbook()
    return result

@action(is_consequential=False)
def get_worksheet_data(sheet_name: str) -> str:
    """
    Gets data (up to 1000 rows) from a specified excel worksheet.
    Only use names of the sheets you can obtain with method get_excel_metadata.

    Args:
        sheet_name (str): Name of the worksheet which data to get. Example "Sheet 1"

    Returns:
        str: All contents of a selected sheet
    """
    excel = Files()
    max_rows = 1000
    excel.open_workbook(path)
    
    # Read the specified sheet. If the sheet has more than 1000 rows, only the first 1000 will be read.
    sheet_data = excel.read_worksheet(sheet_name, header=True)[:max_rows]
    
    excel.close_workbook()
    print(sheet_data)
    return f"{sheet_data}"

@action
def add_new_rows(sheet_name: str, new_rows: RowData) -> str:
    """
    Action to add multiple rows to the Excel sheet. Get the sheets with get_excel_metadata if you don't know
    the names or data structure.  Make sure the values are in correct columns (needs to be ordered the same as in the sample).
    Strictly adhere to the schema.

    Args:
        sheet_name: Name of the sheet where the data is added to
        new_rows: the rows to be added to the sheet
    Returns:
        str: The result of the operation.
    """
    excel = Files()
    excel.open_workbook(path)

    print(new_rows)
    
    raw_data = []
    
    try:
        for row in new_rows.rows:
            raw_data.append(row.columns)

        # Append new rows to the specified sheet. If the sheet has headers, set header=True.
        excel.append_rows_to_worksheet(content=raw_data, name=sheet_name, header=False)
        
        excel.save_workbook()
        excel.close_workbook()
        return "Data added"
    except:
        return "Error adding data"

