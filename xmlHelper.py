import os, re
import xlsxwriter
import writeExcel as we
from pathlib import Path

class xmlHelper:

    # Check for special characters (not safe - do not use)
    def checkSpecialCharsGlobal(url):
        xml_string = open(url)
        print("1. Valid! - no special characters found" if re.match("""^[a-zA-Z0-9_=.":/<>?_\-\s]*$""", xml_string.read()) else "1. Invalid!!! - special characters found!")

    # Check if only one Item present
    def checkOneItemOnly(rootnode):
        return True if len(rootnode.getElementsByTagName('item')) == 1 else False

    # check filenames for special characters
    def checkSpecialCharsInFileNames(rootnode, path):
        parent_path = Path(path).parent
        report_path = os.path.join(parent_path.parent, os.path.basename(os.path.dirname(path + "/imsmanifest.xml")))

        file_strings = rootnode.getElementsByTagName('file')
        title_strings = rootnode.getElementsByTagName('title')
        item_strings = rootnode.getElementsByTagName('item')

        report_data = []
        isValid = True

        # check for special chars in file names
        for fs in file_strings:
            if fs.hasAttribute('href'):
                if re.match("""^[a-zA-Z0-9_./\-]*$""", fs.getAttribute('href')):
                    pass
                else:
                    isValid = False
                    print("Invalid Special Character in " + str(fs.getAttribute('href')))
                    report_data.append('<file href="' + str(fs.getAttribute('href')) + '" />')

        # check for .swf files
        for swf in file_strings:
            if swf.hasAttribute('href'):
                if swf.getAttribute('href')[-3:] == 'swf':
                    isValid = False
                    print("Warning: Flash Content detected!" + str(swf.getAttribute('href')))
                    report_data.append('Flash file: <file href="' + str(swf.getAttribute('href')) + '" />')

        for item_s in item_strings:
            if item_s.hasAttribute('identifier'):
                if re.match("""^[a-zA-Z0-9_./\-]*$""", item_s.getAttribute('href')):
                    pass
                else:
                    isValid = False
                    print("Invalid Special Character in item identifier: " + str(item_s.getAttribute('identifier')))
                    report_data.append('<item identifier="' + str(item_s.getAttribute('identifier')))

        for ts in title_strings:
            try:
                if re.match("""^[a-zA-Z0-9_./\-]*$""", ts.firstChild.nodeValue):
                    pass
                else:
                    isValid = False
                    report_data.append('<title>' + ts.firstChild.nodeValue + '</title>')
                    # print("SPECIAL CHARS DETECTED: " + str(ts.firstChild.nodeValue))
            except:
                print("Exception during special characters Check.")

        if len(report_data) > 0:
            we.createItemsReport(report_path, report_data)

        return isValid

    # check if adlnav presentation element is already present
    def checkAdlnavPresentation(rootnode):
        try:
            adlnav_pres_handler = rootnode.getElementsByTagName('adlnav:hideLMSUI')
            if len(adlnav_pres_handler) < 1:
                return False
            else:
                return True
        except:
            return False

    # create adlnav presentation element
    def adlnavHideElements(domtree):
        adln_presentation = domtree.createElement('adlnav:presentation')
        adln_navigation = adln_presentation.appendChild(domtree.createElement('adlnav:navigationInterface'))
        hide_continue = domtree.createElement('adlnav:hideLMSUI')
        hide_continue.appendChild(domtree.createTextNode('continue'))
        hide_previous = domtree.createElement('adlnav:hideLMSUI')
        hide_previous.appendChild(domtree.createTextNode('previous'))
        hide_exit = domtree.createElement('adlnav:hideLMSUI')
        hide_exit.appendChild(domtree.createTextNode('exit'))
        hide_exitAll = domtree.createElement('adlnav:hideLMSUI')
        hide_exitAll.appendChild(domtree.createTextNode('exitAll'))
        hide_suspendAll = domtree.createElement('adlnav:hideLMSUI')
        hide_suspendAll.appendChild(domtree.createTextNode('suspendAll'))
        hide_abandonAll = domtree.createElement('adlnav:hideLMSUI')
        hide_abandonAll.appendChild(domtree.createTextNode('abandonAll'))
        adln_navigation.appendChild(hide_continue)
        adln_navigation.appendChild(hide_previous)
        adln_navigation.appendChild(hide_exit)
        adln_navigation.appendChild(hide_exitAll)
        adln_navigation.appendChild(hide_suspendAll)
        adln_navigation.appendChild(hide_abandonAll)
        adln_presentation.appendChild(adln_navigation)

        # Append to domtree
        title_element = domtree.getElementsByTagName('title')[1]
        parent = title_element.parentNode
        adlnav = parent.insertBefore(adln_presentation, title_element)
        parent.removeChild(title_element)
        parent.insertBefore(title_element, adlnav)

        # title_element.parentNode.insertBefore(adln_presentation, title_element)
        return domtree

    # check scorm version
    def checkScormVersion(rootnode):
        schema_node = rootnode.getElementsByTagName('schemaversion')[0].firstChild.data
        return schema_node

    def createExcelReport(path, data):
        workbook = xlsxwriter.Workbook('hello.xlsx')
        worksheet = workbook.add_worksheet()

        worksheet.write('A1', 'Hello world')

        workbook.close()