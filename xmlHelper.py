import os, re
import xlsxwriter
import writeExcel as we
import shutil
import gui
from xml.dom import minidom

class xmlHelper:

    # Check if only one Item present
    def checkOneItemOnly(rootnode):
        return True if len(rootnode.getElementsByTagName('item')) == 1 else False

    # check filenames for special characters
    def checkSpecialCharsInFileNames(rootnode, path):

        #print(path)
        #parent_path = Path(path).parent
        #report_path = os.path.join(parent_path.parent, os.path.basename(os.path.dirname(path + "/imsmanifest.xml")))
        print(path)
        print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')

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
            we.createItemsReport(path, report_data)
        else:
            we.createItemsReport(path, ['nothing found!'])

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

    # check TTKF Mode (Training or Assessment)
    def checkAssessment(domtree, path):
        global assessment_mode
        global gui_message
        assessment_mode = False
        try:
            titles = domtree.getElementsByTagName('title')
            for title in titles:
                if 'Assessment' in title.firstChild.data and not assessment_mode:
                    assessment_mode = True
                    #find TTKF Version
                    global runjs_source
                    global runjs_version
                    try:
                        meta_inf = minidom.parse(os.path.join(path, 'meta-inf.xml')).documentElement.getElementsByTagName('Metadata')
                        for i in meta_inf:
                            product_version = i.getAttribute('ProductVersion')
                            if product_version[0:2] == '20':
                                runjs_version = '20'
                                runjs_source = os.path.join(os.getcwd(), 'run_20.js')
                            elif product_version[0:2] == '21':
                                runjs_version = '21'
                                runjs_source = os.path.join(os.getcwd(), 'run_21.js')
                            else:
                                runjs_version = 'unknown'
                    except:
                        print('error parsing meta-inf.xml')
                    try:
                        print('TTKF ASSESSMENT mode detected, copying run.js version ' + runjs_version)
                        runjs_destination = os.path.join(path, 'com.tts.player', 'src', 'run.js')
                        shutil.copyfile(runjs_source, runjs_destination)
                        message = 'TTKF Assessment - run.js v.' + runjs_version + ' replaced'
                        gui_message = [message, '#ffff00']
                    except:
                        print('error copying run.js version ' + runjs_version)
                        gui_message = ['TTKF Assessment - ERROR - run.js was NOT copied', '#ff0000']
                else:
                    gui_message = ['No TTKF Assessment', '#00ff00']
            return gui_message
        except:
            gui_message = ['Error checking TTKF assessment mode']
            print("Error checking TTKF assessment mode")
            return gui_message

    # check scorm version
    def checkScormVersion(rootnode):
        schema_node = rootnode.getElementsByTagName('schemaversion')[0].firstChild.data
        return schema_node


    def writeInfoToReport(rootnode):
        print("****** new report elements ******")
        add_data = []

        #print(rootnode.getAttribute('identifier'))
        add_data.append(str(rootnode.getAttribute('identifier')))

        #print(rootnode.getElementsByTagName('organizations')[0].getAttribute('default'))
        add_data.append(str(rootnode.getElementsByTagName('organizations')[0].getAttribute('default')))

        #print(rootnode.getElementsByTagName('organization')[0].getAttribute('identifier'))
        add_data.append(str(rootnode.getElementsByTagName('organization')[0].getAttribute('identifier')))

        metadata = rootnode.getElementsByTagName('metadata')
        #print(metadata[0].getElementsByTagName('imsmd:title')[0].toxml())
        add_data.append(str(metadata[0].getElementsByTagName('imsmd:title')[0].toxml()))

        for node in rootnode.getElementsByTagName('identifier'):
            #print('identifier=' + node.toxml())
            add_data.append(str())
        for node in rootnode.getElementsByTagName('identifierref'):
            #print('identifierref=' + node.toxml())
            add_data.append(str('identifier=' + node.toxml()))

        for node in rootnode.getElementsByTagName('title'):
            #print(node.toxml())
            add_data.append(str(node.toxml()))
        #print(rootnode.getElementsByTagName('resource')[0].getAttribute('identifier'))
        add_data.append(str(rootnode.getElementsByTagName('resource')[0].getAttribute('identifier')))
        return add_data

    def createExcelReport(path, data):
        workbook = xlsxwriter.Workbook('hello.xlsx')
        worksheet = workbook.add_worksheet()

        worksheet.write('A1', 'Hello world')

        workbook.close()


    def writeInfoToReport(rootnode):
        print("****** new report elements ******")
        add_data = []

        # print(rootnode.getAttribute('identifier'))
        add_data.append(str(rootnode.getAttribute('identifier')))

        # print(rootnode.getElementsByTagName('organizations')[0].getAttribute('default'))
        add_data.append(str(rootnode.getElementsByTagName('organizations')[0].getAttribute('default')))

        # print(rootnode.getElementsByTagName('organization')[0].getAttribute('identifier'))
        add_data.append(str(rootnode.getElementsByTagName('organization')[0].getAttribute('identifier')))

        metadata = rootnode.getElementsByTagName('metadata')
        # print(metadata[0].getElementsByTagName('imsmd:title')[0].toxml())
        add_data.append(str(metadata[0].getElementsByTagName('imsmd:title')[0].toxml()))

        for node in rootnode.getElementsByTagName('identifier'):
            # print('identifier=' + node.toxml())
            add_data.append(str())
        for node in rootnode.getElementsByTagName('identifierref'):
            # print('identifierref=' + node.toxml())
            add_data.append(str('identifier=' + node.toxml()))

        for node in rootnode.getElementsByTagName('title'):
            # print(node.toxml())
            add_data.append(str(node.toxml()))
        # print(rootnode.getElementsByTagName('resource')[0].getAttribute('identifier'))
        add_data.append(str(rootnode.getElementsByTagName('resource')[0].getAttribute('identifier')))
        return add_data