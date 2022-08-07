import re, os

# Übermittlung von Lernzeit u. Score ans LMS ausschalten

# txt = r',f(u.LESSON_STATUS,h),f(u.SESSION_TIME,l),f(u.EXIT,a.getValue(o.EXIT)||""),f(u.SUSPEND_DATA,s)}catch(e){t.error(e)}'
# txt2 = r',A(l.SUCCESS_STATUS,a.getValue(o.SUCCESS_STATUS)),A(l.SESSION_TIME,u),A(l.EXIT,a.getValue(o.EXIT)||""),A(l.SUSPEND_DATA,r.create(i))'
# # x = re.sub(r',(.\(.\.SESSION_TIME,.\),)(.\(.\.EXIT)', r',/\*$1*/$2', txt)
# x = re.sub(r',(.\(.\.SESSION_TIME,.\),)(.\(.\.EXIT)', r',/*\1*/\2', txt)
# y = re.sub(r',(.\(.\.SESSION_TIME,.\),)(.\(.\.EXIT)', r',/*\1*/\2', txt2)

# new_script = []
new_script = ''

def change_articulate_scormdriver(path):
    try:
        # with open(path, 'r') as f:
        #     scormdriver_lines = f.readlines()
        #     for line in scormdriver_lines:
        #         # SCORM 2004
        #         line = re.sub(r'function SCORM2004_SaveTime\(intMilliSeconds\){(.*?)}', r'function SCORM2004_SaveTime(intMilliSeconds){return 0;}', line)
        #         line = re.sub(r'function SCORM2004_SetScore\(intScore,intMaxScore,intMinScore\){(.*?)}', r'function SCORM2004_SetScore(intScore,intMaxScore,intMinScore){return 0;}', line)
        #         # SCORM 1.2
        #         line = re.sub(r'function SCORM_SaveTime\(intMilliSeconds\){(.*?)}', r'function SCORM_SaveTime(intMilliSeconds){return 0;}', line)
        #         line = re.sub(r'function SCORM_SetScore\(intScore,intMaxScore,intMinScore\){(.*?)}', r'function SCORM_SetScore(intScore,intMaxScore,intMinScore){return 0;}', line)
        #         new_script.append(line)
        #
        # with open(path, 'w') as f:
        #     f.writelines(new_script)

        with open(path, 'r') as f:
            scormdriver_lines = f.readlines()
            for line in scormdriver_lines:
                global new_script
                new_script = new_script + line
        # SCORM 2004
        new_script = re.sub(r'function SCORM2004_SaveTime\(intMilliSeconds\){(.*[\s\S]*?)}',
                            r'function SCORM2004_SaveTime(intMilliSeconds){return 0;}', new_script)
        new_script = re.sub(r'function SCORM2004_SetScore\(intScore,\s*intMaxScore,\s*intMinScore\){(.*[\s\S]*?)}',
                            r'function SCORM2004_SetScore(intScore,intMaxScore,intMinScore){return 0;}', new_script)
        # SCORM 1.2
        new_script = re.sub(r'function SCORM_SaveTime\(intMilliSeconds\){(.*[\s\S]*?)}',
                            r'function SCORM_SaveTime(intMilliSeconds){return 0;}', new_script)
        new_script = re.sub(r'function SCORM_SetScore\(intScore,\s*intMaxScore,\s*intMinScore\){(.*[\s\S]*?)}',
                            r'function SCORM_SetScore(intScore,intMaxScore,intMinScore){return 0;}', new_script)

        with open(path, 'w') as f:
            f.writelines(new_script)
        return "Scormdriver has been modified!"
    except:
        print("Error modifying Scormdriver!")
        return "Error modifying Scormdriver"

def change_runjs(path):
    try:
        with open(path, 'r') as f:
            runjs_lines = f.readlines()
            for line in runjs_lines:
                line = re.sub(r',(.\(.\.SESSION_TIME,.\),)(.\(.\.EXIT)', r',/*\1*/\2', line)
                line = re.sub(r',.\.setValue\(.\.SCORE_SCALED[^1]*100\)', r' ', line)
                line = re.sub(r',.\.setValue\(.\.SCORE_RAW.*?SCORE_MAX\)\)', r' ', line)
                new_script.append(line)

        with open(path, 'w') as f:
            f.writelines(new_script)
        print("run.js has been modified")
        return "run.js has been modified"
    except:
        print("Error modifying run.js!")
        return "Error modifying run.js!"

def disable_time_score(path):
    if os.path.isfile(os.path.join(path, r'scormdriver\scormdriver.js')):
        print("Articulate Rise Content detected!")
        rise_path = os.path.join(path, r'scormdriver/scormdriver.js')
        result = change_articulate_scormdriver(rise_path)
        return result
    elif os.path.isfile(os.path.join(path, r'lms\scormdriver.js')):
        print("Articulate Storyline Content detected!")
        storyline_path = os.path.join(path, r'lms\scormdriver.js')
        result = change_articulate_scormdriver(storyline_path)
        return result
    elif os.path.isfile(os.path.join(path, r'com.tts.player\src\run.js')):
        print("TTKF Content detected!")
        ttkf_path = os.path.join(path, r'com.tts.player\src\run.js')
        result = change_runjs(ttkf_path)
        return result
    elif os.path.isfile(os.path.join(path, r'lms\SCORM2004Functions.js')):
        print("Articulate Storyline Content detected!")
        os.path.join(path, r'lms\SCORM2004Functions.js')
        storyline_path = os.path.join(path, r'lms\SCORMFunctions.js')
        result = change_articulate_scormdriver(storyline_path)
        return result
    else:
        print("No Articulate or TTKF Content found!")
        return "No Articulate or TTKF Content!"

