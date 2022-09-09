from openpyxl import Workbook, load_workbook
import os

def createReport(path):
    wb = Workbook()
    ws = wb.active
    ws.column_dimensions['A'].width = 72
    ws.column_dimensions['B'].width = 40
    ws.column_dimensions['C'].width = 36
    ws.column_dimensions['D'].width = 62
    ws.column_dimensions['E'].width = 44
    ws.column_dimensions['F'].width = 40

    # Rows can also be appended
    ws.append(["COURSE FILE PATH", "LEARNING TIME/ SCORE", "TTKF-Mode", "SCORM VERSION", "ONE ITEM CHECK", "ADLNAV NAMESPACE (2004 4th only)", "SPECIAL CHARACTERS CHECK"])
    try:
        wb.save(os.path.join(path, "SCORM-Test-Report.xlsx"))
        wb.close()
    except:
        print("Not possible to create SCORM-Report - file maybe open?")
        return True

def writeReport(path, data):
    try:
        wb = load_workbook(os.path.join(path, "SCORM-Test-Report.xlsx"))
        ws = wb.active
        ws.append(data)
        wb.save(os.path.join(path, "SCORM-Test-Report.xlsx"))
        wb.close()
        return True
    except:
        return False

def createItemsReport(path, data):
    wb = Workbook()
    ws = wb.active
    ws.column_dimensions['A'].width = 120
    ws.append(['SPECIAL CHARACTERS IN IMSMANIFEST.XML'])
    for i in data:
        row = []
        row.append(i)
        ws.append(row)
    try:
        wb.save(path)
        wb.close()
    except:
        print("Not possible to write items-report - file maybe open?")

def write_lms_upload_sheet(path, data):
    wb = Workbook()
    ws = wb.active
    ws.column_dimensions['A'].width = 120
    ws.append(['ZIP-FILES for LMS-Upload'])
    for i in data:
        row = []
        row.append(i)
        ws.append(row)
    try:
        wb.save(os.path.join(path, "LMS-Upload-Sheet.xlsx"))
        wb.close()
    except:
        print("Not possible to write LMS-Upload-Sheet - file maybe open?")

def lms_upload_sheet(path):
    try:
        wb = load_workbook(os.path.join(path, "LMS-Upload-Sheet.xlsx"))
        print(os.path.join(path, "LMS-Upload-Sheet.xlsx"))
        ws = wb.active
        row_a = ws['A']
        scorm_files = []
        for i in row_a:
            print(i.value)
            scorm_files.append(i.value)
        scorm_files.pop(0)
        print(scorm_files)
        wb.close()
        return scorm_files
    except:
        return False

def add_items_to_upload_sheet(path, item, lms):

    try:
        wb = load_workbook(os.path.join(path, "LMS-Upload-Sheet.xlsx"))
        sheets = wb.sheetnames
        if 'Items' in sheets:
            ws = wb.get_sheet_by_name('Items')
            row = []
            row.append(item)
            row.append(lms)
            ws.append(row)
        else:
            ws2 = wb.create_sheet()
            ws2.title = "Items"
            ws2.column_dimensions['A'].width = 50
            row = []
            row.append(item)
            row.append(lms)
            ws2.append(row)
        wb.save(os.path.join(path, "LMS-Upload-Sheet.xlsx"))
        wb.close()
    except:
        return False