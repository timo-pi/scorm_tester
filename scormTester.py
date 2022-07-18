from xml.dom import minidom
import os
from tkinter import filedialog
from xmlHelper import xmlHelper as xhelp
import scormZipper as sz
import writeExcel as we
from pathlib import Path
import mediainfo
# import lms_upload as lms
import gui
import disable_time_score as dts

#*****************************************************
# Command to build exe:
# pyinstaller --noconfirm --onefile --add-data "writeExcel.py;." --add-data "xmlHelper.py;." --add-data "scormZipper.py;." --add-data "mediainfo.py;." --add-data "gui.py;." --add-data "exiftool.exe;." --add-data "run_20.js;." --add-data "run_21.js;." --add-data "disable_time_score.py;." --icon=schwarz.ico --clean scormTester.py
# pyinstaller --noconfirm --onedir --add-data "writeExcel.py;." --add-data "xmlHelper.py;." --add-data "scormZipper.py;." --add-data "mediainfo.py;." --add-data "gui.py;." --add-data "exiftool.exe;." --add-data "run_20.js;." --add-data "run_21.js;." --add-data "disable_time_score.py;." --icon=schwarz.ico --clean scormTester.py
#*****************************************************

version = "v2.6 | 17.07.2022"

multi_files_select = False
report_path = ""
report_saved = False
new_scorm_zip = False
#global checkbox_svg, label_characters, SCORM_2004_4, new_scorm_zip, label_scorm, label_namespace, label_item

def saveImsmanifest(rootnode, path):
    with open(path, 'w') as f:
        f.write(rootnode.toxml())
        # f.write(adln_presentation.toprettyxml())
        f.close()
    ##sz.zipScorm(path)

def runChecks(path):
    SCORM_2004_4 = False
    path = path.replace('\\', '/')
    report_data = [path]
    print("PATH: " + str(path))
    global new_scorm_zip
    # open xml document
    try:
        domtree = minidom.parse(path + "/imsmanifest.xml")
        rootnode = domtree.documentElement
    except:
        print("Error parsing imsmanifest.xml - not found or faulty.")
        gui.clearLabels()
        label_scorm = gui.tk.Label(gui.root, textvariable=gui.text_scorm, anchor="c", bg='#ff0000')
        label_scorm.place(x=20, y=20, width=460, height=30)
        gui.text_scorm.set("Error parsing imsmanifest.xml - not found or faulty.")
        label_namespace = gui.tk.Label(gui.root, textvariable=gui.text_namespace, anchor="c", bg='#ff0000')
        label_namespace.place(x=20, y=50, width=460, height=30)
        gui.text_namespace.set("Please check your SCORM-File manually.")
        return 0

    gui.clearLabels()

    # check SCORM version and assessment-mode
    if gui.checkbox_runjs.get():
        ttkf_assessment = xhelp.checkAssessment(rootnode, path)
        # runjs_time_score_message = str(runjs_time_score_message + " | " + ttkf_assessment[0])
        gui.setLabelTtkf(ttkf_assessment[0], ttkf_assessment[1])

        if ttkf_assessment[0] != 'No TTKF Assessment':
            report_data.append(ttkf_assessment[0])
            new_scorm_zip = True
        else:
            report_data.append(ttkf_assessment[0])
    else:
        report_data.append('Assessment-Check off')

    # disable learning time + score for ttkf, Storyline, Rise content
    if gui.checkbox_disable_time_score.get():
        result = dts.disable_time_score(path)
        print("RESULT:")
        print(result)
        if result == "Scormdriver has been modified!" or result == "run.js has been modified":
            new_scorm_zip = True
            gui.setLabelTimeScore(result, '#00ff00')
        else:
            gui.setLabelTimeScore(result, '#ffff00')
        report_data.append(result)

    scorm_version = xhelp.checkScormVersion(domtree)
    gui.setLabelStatus("Overall Status: OK.", '#00ff00')
    if "2004 4th Edition" in scorm_version:
        print("SCORM Version: 2004 4th Edition")
        SCORM_2004_4 = True
        label_scorm = gui.tk.Label(gui.root, textvariable=gui.text_scorm, anchor="c", bg='#00ff00')
        label_scorm.place(x=20, y=20, width=460, height=30)
        gui.text_scorm.set('SCORM Version: 2004 4th Edition')
        # write to excel if multiple files selected
        if multi_files_select: report_data.append(scorm_version)
    elif "CAM 1.3" in scorm_version or "2004 2nd Edition" in scorm_version:
        print("SCORM 2004 2nd Edition")
        label_scorm = gui.tk.Label(gui.root, textvariable=gui.text_scorm, anchor="c", bg='#ff0000')
        label_scorm.place(x=20, y=20, width=460, height=30)
        gui.text_scorm.set('SCORM 2004 2nd Edition')
        # write to excel if multiple files selected
        if multi_files_select: report_data.append("SCORM 2004 2nd Edition")
    elif scorm_version == "1.2":
        print("SCORM Version: SCORM 1.2")
        label_scorm = gui.tk.Label(gui.root, textvariable=gui.text_scorm, anchor="c", bg='#00ff00')
        label_scorm.place(x=20, y=20, width=460, height=30)
        gui.text_scorm.set('SCORM Version: 1.2')
        # write to excel if multiple files selected
        if multi_files_select: report_data.append("SCORM 1.2")
    elif "2004 3rd Edition" in scorm_version:
        print("SCORM 2004 3rd Edition")
        label_scorm = gui.tk.Label(gui.root, textvariable=gui.text_scorm, anchor="c", bg='#00ff00')
        label_scorm.place(x=20, y=20, width=460, height=30)
        gui.text_scorm.set('SCORM Version: 2004 3rd Edition')
        # write to excel if multiple files selected
        if multi_files_select: report_data.append(scorm_version)
    else:
        print("SCORM  Version: unknown")
        label_scorm = gui.tk.Label(gui.root, textvariable=gui.text_scorm, anchor="c", bg='#ff0000')
        label_scorm.place(x=20, y=20, width=460, height=30)
        gui.text_scorm.set('SCORM Version: unknown')
        # write to excel if multiple files selected
        if multi_files_select: report_data.append(scorm_version)

    # check for multiple items
    if xhelp.checkOneItemOnly(rootnode):
        label_item = gui.tk.Label(gui.root, textvariable=gui.text_item, anchor="c", bg='#00ff00')
        label_item.place(x=20, y=80, width=460, height=30)
        gui.text_item.set("Passed: Only one Item element present.")
        # write to excel if multiple files selected
        if multi_files_select: report_data.append("Passed: Only one Item element present.")
    else:
        label_item = gui.tk.Label(gui.root, textvariable=gui.text_item, anchor="c", bg='#ff0000')
        label_item.place(x=20, y=80, width=460, height=30)
        gui.text_item.set("FAILED: More than one Item element present!")
        # write to excel if multiple files selected
        if multi_files_select: report_data.append("FAILED: More than one Item element present!")

    ### check for adlnav namespace in manifest
    if SCORM_2004_4:
        # new_scorm_zip = False
        test = rootnode.getAttribute("xmlns:adlnav")
        # add adlnav attribute to manifest
        if test == "":
            new_scorm_zip = True
            print("adlnav-namespace NOT found in manifest tag!")
            rootnode.setAttribute("xmlns:adlnav", "http://www.adlnet.org/xsd/adlnav_v1p3")
            print("Created namespace entry: " + rootnode.getAttribute("xmlns:adlnav"))

        # check for adlnav presentation in item element
        if xhelp.checkAdlnavPresentation(rootnode):
            gui.setNamespaceLabel("Passed: adlnav-Namespace present", '#00ff00')
        else:
            new_scorm_zip = True
            xhelp.adlnavHideElements(domtree)
            gui.setNamespaceLabel("New imsmanifest.xml has been created!", '#ffff00')
        # write namespace info to excel if multiple files selected
        if multi_files_select:
            if new_scorm_zip:
                 report_data.append("WARNING: Namespace was missing - new SCORM package has been created!")
            else:
                report_data.append("Passed: Namespace present or not relevant for this SCORM version")

    else:
        label_namespace = gui.tk.Label(gui.root, textvariable=gui.text_namespace, anchor="c", bg='#00ff00')
        label_namespace.place(x=20, y=50, width=460, height=30)
        gui.text_namespace.set("Passed: Namespace not relevant for this SCORM version.")
        # write to excel if multiple files selected
        if multi_files_select: report_data.append("Passed: Namespace not relevant for this SCORM version.")

    # zip scorm package
    if new_scorm_zip:
        parent_path = Path(path).parent
        os.path.join(parent_path.parent, os.path.basename(os.path.dirname(path + "/imsmanifest.xml"))) + '_sf.zip'
        gui.setLabelStatus("New SCORM package created!", '#ffff00')

        # save manifest.xml
        saveImsmanifest(rootnode, path + "/imsmanifest.xml")
        sz.zipDir(path, os.path.basename(path) + '_sf')

    # check filenames for special characters
    parent_path = str(Path(path).parent.parent)
    report_name = "\\SPECIAL_CHARACTERS_" + str(os.path.basename(path)) + ".xlsx"
    if xhelp.checkSpecialCharsInFileNames(rootnode, (parent_path + report_name)):
        label_characters = gui.tk.Label(gui.root, textvariable=gui.text_characters, anchor="c", bg='#00ff00') #green
        label_characters.place(x=20, y=110, width=460, height=30)
        gui.text_characters.set("Passed: No special characters in file or title elements.")
        # write to excel if multiple files selected
        if multi_files_select: report_data.append("Passed: No special characters in file or title elements.")
    else:
        label_characters = gui.tk.Label(gui.root, textvariable=gui.text_characters, anchor="c", bg='#ff0000') #red
        label_characters.place(x=20, y=110, width=460, height=30)
        gui.text_characters.set("Failed: special characters or .swf files detected!")
        gui.setLabelStatus("Pls. check report/ imsmanifest.xml for special characters!", '#ff0000')
        # write to excel if multiple files selected
        if multi_files_select: report_data.append("Failed: Special Characters in file or title element(s)!")

    # save Report if multiple files selected
    if multi_files_select:
        global report_saved
        report_saved = we.writeReport(report_path, report_data)
        if report_saved:
            gui.clearLabels()
            gui.setLabelStatus('Multiple files selected - pls. check SCORM-Test-Report.xlsx', '#ffff00')
        else:
            print("Error saving report - file may be open")
            gui.clearLabels()
            gui.setLabelStatus('Report could not be saved (file maybe open?)', '#ff0000')
    return path

def selectFiles():
    gui.root.filenames = filedialog.askopenfilenames(initialdir="/", title="Select file", filetypes=(("all files", "*.*"), ("all files", "*.*")))
    if len(gui.root.filenames) == 1:
        print("FILE: " + str(gui.root.filenames))
        media_path = runChecks(sz.extractScorm(gui.root.filenames[0]))
        if gui.checkbox_media_test.get():
            mediainfo.checkMediaFiles([media_path], gui.checkbox_svg.get())
        else:
            print("Media files check disabled.")

        # LMS-Upload
        # if gui.checkbox_lms.get():
        #     lms.start_upload(media_path)


    # MULTIPLE FILES SELECTED
    elif len(gui.root.filenames) > 1:
        global multi_files_select, report_path, report_saved
        multi_files_select = True
        report_path = os.path.dirname(gui.root.filenames[0])
        report_saved = we.createReport(report_path)
        for i in gui.root.filenames:
            print("FILE: " + str(i))
            gui.clearLabels()
            media_path = runChecks(sz.extractScorm(i))
            if gui.checkbox_media_test.get():
                mediainfo.checkMediaFiles([media_path], gui.checkbox_svg.get())
            else:
                print("Media files check disabled.")

print("Scorm-Tester " + version)

btn_select = gui.tk.Button(gui.root, text="Select File(s)", command=selectFiles, bg='grey')
btn_select.place(x=180, y=350, width=140, height=30)
gui.root.mainloop()
