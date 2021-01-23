from xml.dom import minidom
import os
import tkinter as tk
from tkinter import filedialog, IntVar, Checkbutton
from xmlHelper import xmlHelper as xhelp
import scormZipper as sz
import writeExcel as we
from pathlib import Path
import mediainfo

#**************************************************+++
# Command to build exe:
# pyinstaller --add-data "writeExcel.py;." --add-data "xmlHelper.py;." --add-data "scormZipper.py;." --onefile --clean -y scormTester.py
# pyinstaller --add-data "writeExcel.py;." --add-data "xmlHelper.py;." --add-data "scormZipper.py;." --add-data "mediainfo.py;." --add-data "exiftool.exe;." --icon=schwarz.ico --clean -y scormTester.py
#*****************************************************

version = "v2.2 | 23.01.2021"

multi_files_select = False
report_path = ""
report_saved = False
check_media_files = True
global checkbox_svg

def saveImsmanifest(rootnode, path):
    with open(path, 'w') as f:
        f.write(rootnode.toxml())
        # f.write(adln_presentation.toprettyxml())
        f.close()
    ##sz.zipScorm(path)

def runChecks(path):
    path = path.replace('\\', '/')
    report_data = [path]
    print("PATH: " + str(path))
    SCORM_2004_4 = False
    # open xml document
    try:
        domtree = minidom.parse(path + "/imsmanifest.xml")
        rootnode = domtree.documentElement
    except:
        print("Error parsing imsmanifest.xml - not found or faulty.")
        clearLabels()
        label_scorm = tk.Label(root, textvariable=text_scorm, anchor="w", background='#fe5f55')
        label_scorm.place(x=20, y=20, width=460, height=30)
        text_scorm.set("Error parsing imsmanifest.xml - not found or faulty.")
        label_namespace = tk.Label(root, textvariable=text_namespace, anchor="w", background='#fe5f55')
        label_namespace.place(x=20, y=50, width=460, height=30)
        text_namespace.set("Please check your SCORM-File manually.")
        return 0

    # check SCORM version
    clearLabels()
    scorm_version = xhelp.checkScormVersion(rootnode)
    if "2004 4th Edition" in scorm_version:
        print("SCORM Version: 2004 4th Edition")
        SCORM_2004_4 = True
        label_scorm = tk.Label(root, textvariable=text_scorm, anchor="w", background='#c7d66d')
        label_scorm.place(x=20, y=20, width=460, height=30)
        text_scorm.set('SCORM Version: 2004 4th Edition')
        # write to excel if multiple files selected
        if multi_files_select: report_data.append(scorm_version)
    elif "CAM 1.3" in scorm_version or "2004 2nd Edition" in scorm_version:
        print("SCORM 2004 2nd Edition")
        label_scorm = tk.Label(root, textvariable=text_scorm, anchor="w", background='#fe5f55')
        label_scorm.place(x=20, y=20, width=460, height=30)
        text_scorm.set('SCORM 2004 2nd Edition')
        # write to excel if multiple files selected
        if multi_files_select: report_data.append("SCORM 2004 2nd Edition")
    elif scorm_version == "1.2":
        print("SCORM Version: SCORM 1.2")
        label_scorm = tk.Label(root, textvariable=text_scorm, anchor="w", background='#c7d66d')
        label_scorm.place(x=20, y=20, width=460, height=30)
        text_scorm.set('SCORM Version: 1.2')
        # write to excel if multiple files selected
        if multi_files_select: report_data.append("SCORM 1.2")
    elif "2004 3rd Edition" in scorm_version:
        print("SCORM 2004 3rd Edition")
        label_scorm = tk.Label(root, textvariable=text_scorm, anchor="w", background='#c7d66d')
        label_scorm.place(x=20, y=20, width=460, height=30)
        text_scorm.set('SCORM Version: 2004 3rd Edition')
        # write to excel if multiple files selected
        if multi_files_select: report_data.append(scorm_version)
    else:
        print("SCORM  Version: unknown")
        label_scorm = tk.Label(root, textvariable=text_scorm, anchor="w", background='#fe5f55')
        label_scorm.place(x=20, y=20, width=460, height=30)
        text_scorm.set('SCORM Version: unknown')
        # write to excel if multiple files selected
        if multi_files_select: report_data.append(scorm_version)

    # check for multiple items
    if xhelp.checkOneItemOnly(rootnode):
        label_item = tk.Label(root, textvariable=text_item, anchor="w", background='#c7d66d')
        label_item.place(x=20, y=80, width=460, height=30)
        text_item.set("Passed: Only one Item element present.")
        # write to excel if multiple files selected
        if multi_files_select: report_data.append("Passed: Only one Item element present.")
    else:
        label_item = tk.Label(root, textvariable=text_item, anchor="w", background='#fe5f55')
        label_item.place(x=20, y=80, width=460, height=30)
        text_item.set("FAILED: More than one Item element present!")
        # write to excel if multiple files selected
        if multi_files_select: report_data.append("FAILED: More than one Item element present!")

    ### check for adlnav namespace in manifest
    if SCORM_2004_4:
        global ns_problem_found
        ns_problem_found = False
        test = rootnode.getAttribute("xmlns:adlnav")
        # add adlnav attribute to manifest
        if test == "":
            ns_problem_found = True
            print("adlnav-namespace NOT found in manifest tag!")
            rootnode.setAttribute("xmlns:adlnav", "http://www.adlnet.org/xsd/adlnav_v1p3")
            print("Created namespace entry: " + rootnode.getAttribute("xmlns:adlnav"))

        # check for adlnav presentation in item element
        if xhelp.checkAdlnavPresentation(rootnode):
            pass
        else:
            ns_problem_found = True
            xhelp.adlnavHideElements(domtree)
        # write namespace info to excel if multiple files selected
        if multi_files_select:
            if ns_problem_found:
                 report_data.append("WARNING: Namespace was missing - new SCORM package has been created!")
            else:
                report_data.append("Passed: Namespace present or not relevant for this SCORM version")

        # zip scorm package
        if ns_problem_found:
            ##file_paths = sz.retrieve_file_paths(path)

            #file_name = os.path.basename(os.path.dirname(path + "/imsmanifest.xml")) + '_SF.zip'
            parent_path = Path(path).parent
            zip_path = os.path.join(parent_path.parent, os.path.basename(os.path.dirname(path + "/imsmanifest.xml"))) + '_SF.zip'
            #new_zip_file_path = os.path.join(os.path.dirname(path), file_name)
            setLabelStatus("imsmanifest.xml adjusted and new SCORM package created!", '#ffd275')

            # save manifest.xml
            saveImsmanifest(rootnode, path + "/imsmanifest.xml")
            ##sz.zipScorm(file_paths, zip_path)
            sz.zipDir(path, os.path.basename(path) + '_sf')

            setNamespaceLabel("New imsmanifest.xml has been created!", '#ffd275')
        else:
            setNamespaceLabel("Passed: adlnav-Namespace present", '#c7d66d')
    else:
        label_namespace = tk.Label(root, textvariable=text_namespace, anchor="w", background='#c7d66d')
        label_namespace.place(x=20, y=50, width=460, height=30)
        text_namespace.set("Passed: Namespace not relevant for this SCORM version.")
        # write to excel if multiple files selected
        if multi_files_select: report_data.append("Passed: Namespace not relevant for this SCORM version.")

    # check filenames for special characters
    if xhelp.checkSpecialCharsInFileNames(rootnode, (os.path.dirname(path + "/imsmanifest.xml") + '_SPECIAL_CHARACTERS.xlsx')):
        label_characters = tk.Label(root, textvariable=text_characters, anchor="w", background='#c7d66d') #green
        label_characters.place(x=20, y=110, width=460, height=30)
        text_characters.set("Passed: No special characters in file or title elements.")
        # write to excel if multiple files selected
        if multi_files_select: report_data.append("Passed: No special characters in file or title elements.")
    else:
        label_characters = tk.Label(root, textvariable=text_characters, anchor="w", background='#fe5f55') #red
        label_characters.place(x=20, y=110, width=460, height=30)
        text_characters.set("Failed: special characters or .swf files detected!")
        setLabelStatus("Pls. check report/ imsmanifest.xml for special characters!", '#fe5f55')
        # write to excel if multiple files selected
        if multi_files_select: report_data.append("Failed: Special Characters in file or title element(s)!")

    # save Report if multiple files selected
    if multi_files_select:
        report_data.append(os.path.dirname(path + "/imsmanifest.xml") + '_SF.zip')
        global report_saved
        report_saved = we.writeReport(report_path, report_data)
        if report_saved:
            clearLabels()
            setLabelStatus('Multiple files selected - pls. check SCORM-Test-Report.xlsx', '#ffd275')
        else:
            print("Error saving report - file may be open")
            clearLabels()
            setLabelStatus('Report could not be saved (maybe open?)', '#fe5f55')
    return path

def selectFiles():
    root.filenames = filedialog.askopenfilenames(initialdir="/", title="Select file", filetypes=(("all files", "*.*"), ("all files", "*.*")))
    if len(root.filenames) == 1:
        print("FILE: " + str(root.filenames))
        media_path = runChecks(sz.extractScorm(root.filenames[0]))
        if checkbox_media_test.get():
            mediainfo.checkMediaFiles([media_path], checkbox_svg)
        else:
            print("Media files check disabled.")

    # MULTIPLE FILES SELECTED
    elif len(root.filenames) > 1:
        global multi_files_select, report_path, report_saved
        multi_files_select = True
        report_path = os.path.dirname(root.filenames[0])
        report_saved = we.createReport(report_path)
        for i in root.filenames:
            print("FILE: " + str(i))
            clearLabels()
            media_path = runChecks(sz.extractScorm(i))
            if checkbox_media_test.get():
                mediainfo.checkMediaFiles([media_path], checkbox_svg.get())
            else:
                print("Media files check disabled.")

def clearLabels():
    label_scorm = tk.Label(root, textvariable="", anchor="w")
    label_scorm.place(x=20, y=20, width=460, height=30)
    label_namespace = tk.Label(root, textvariable="", anchor="w")
    label_namespace.place(x=20, y=50, width=460, height=30)
    label_item = tk.Label(root, textvariable="", anchor="w")
    label_item.place(x=20, y=80, width=460, height=30)
    label_characters = tk.Label(root, textvariable="", anchor="w")
    label_characters.place(x=20, y=110, width=460, height=30)
    label_status = tk.Label(root, textvariable="", borderwidth=2, relief="groove", anchor="w")
    label_status.place(x=10, y=170, width=480, height=30)

def setLabelStatus(text, color):
    text_status.set(text)
    label_status = tk.Label(root, textvariable=text_status, borderwidth=2, anchor="w", background=color)
    label_status.place(x=20, y=175, width=460, height=20)

def setNamespaceLabel(text, color):
    text_namespace.set(text)
    label_namespace = tk.Label(root, textvariable=text_namespace, anchor="w", background=color)
    label_namespace.place(x=20, y=50, width=460, height=30)

def toggleMediaCheck():
    global check_media_files
    if check_media_files:
        check_media_files = False
    else:
        check_media_files = True

def toggleSvgCheck():
    global checkbox_svg
    if checkbox_svg:
        checkbox_svg = False
    else:
        checkbox_svg = True

print("Scorm-Tester " + version)

# GUI
root = tk.Tk()
text_scorm, text_namespace, text_item, text_characters, text_status = tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar()
text_scorm.set("SCORM Version:")
text_namespace.set("Namespace check (adlnav):")
text_item.set("Only one Item present:")
text_characters.set("Special characters check:")
text_status.set("    Overall status:")

root.geometry('500x400')
#root.configure(background='#676767')
#root.iconbitmap('./schwarz.ico')
root.title('SIT | SCORM Tester')

# Buttons
btn_select = tk.Button(root, text="Select File(s)", command=selectFiles)
btn_quit = tk.Button(root, text="Quit", command=lambda: root.destroy())
btn_select.place(x=180, y=280, width=140, height=30)
btn_quit.place(x=180, y=320, width=140, height=30)

# Checkboxes
checkbox_media_test = IntVar()
checkbox_media_test.set(True)
Checkbutton(root, text="Create Media Files Report", command=toggleMediaCheck, variable=checkbox_media_test).place(x=180, y=215)

checkbox_svg = IntVar()
checkbox_svg.set(True)
Checkbutton(root, text="exclude ttkf player directory", command=toggleSvgCheck, variable=checkbox_svg).place(x=180, y=240)

# Labels
label_group = tk.Label(root, borderwidth=2, relief="groove")
label_group.place(x=10, y=10, width=480, height=140)
label_scorm = tk.Label(root, textvariable=text_scorm, anchor="w")
label_scorm.place(x=20, y=20, width=460, height=30)
label_namespace = tk.Label(root, textvariable=text_namespace, anchor="w")
label_namespace.place(x=20, y=50, width=460, height=30)
label_item = tk.Label(root, textvariable=text_item, anchor="w")
label_item.place(x=20, y=80, width=460, height=30)
label_characters = tk.Label(root, textvariable=text_characters, anchor="w")
label_characters.place(x=20, y=110, width=460, height=30)
label_status = tk.Label(root, textvariable=text_status, borderwidth=2, relief="groove", anchor="w")
label_status.place(x=10, y=170, width=480, height=30)

root.mainloop()
