

def SetValuesAndFormatCells(worksheet, values=None, startRow=0, rowCount=1, startCol=0, colCount=1, cellFormat=None):
    """
    This is the function to input value of cells and set format of cells.

    :type sheet: sheet created by xlsxwriter.
          values: list to input in cells. (For example: [["a", "b", "c"], ["aa", "bb", "cc"], .... ])
                    a   b   c
                    aa  bb  cc
          startRow: integer of start row to set format of cells.(default value: 0, type: integer)
          rowCount: count of rows to set format of cells.(default value: 1, type: integer)
          startCol: integer of start col to set format of cells.(default value: 0, type: integer)
          colCount: count of cols to set format of cells.(default value: 1, type: integer)
          cellFormat: format of cell to set. (default value : None)
    :return None
    """

    if values:
        # If there are values, it ignores rowCount and colCount because rowCount and colCount are prescribed by values.
        for row, rowVals in enumerate(values):
            for col, val in enumerate(rowVals):
                worksheet.write(startRow + row, startCol + col, val, cellFormat)
    else:
        # If there are no values, it ignores rowCount and colCount.
        # This case is to set format of cells in empty cells.
        for row in range(rowCount):
            for col in range(colCount):
                worksheet.write(startRow + row, startCol + col, '', cellFormat)
    pass