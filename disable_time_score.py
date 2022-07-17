import re, os

# Übermittlung von Lernzeit u. Score ans LMS ausschalten

# txt = r',f(u.LESSON_STATUS,h),f(u.SESSION_TIME,l),f(u.EXIT,a.getValue(o.EXIT)||""),f(u.SUSPEND_DATA,s)}catch(e){t.error(e)}'
# txt2 = r',A(l.SUCCESS_STATUS,a.getValue(o.SUCCESS_STATUS)),A(l.SESSION_TIME,u),A(l.EXIT,a.getValue(o.EXIT)||""),A(l.SUSPEND_DATA,r.create(i))'
# # x = re.sub(r',(.\(.\.SESSION_TIME,.\),)(.\(.\.EXIT)', r',/\*$1*/$2', txt)
# x = re.sub(r',(.\(.\.SESSION_TIME,.\),)(.\(.\.EXIT)', r',/*\1*/\2', txt)
# y = re.sub(r',(.\(.\.SESSION_TIME,.\),)(.\(.\.EXIT)', r',/*\1*/\2', txt2)

new_script = []

def change_articulate_scormdriver(path):
    try:
        with open(path, 'r') as f:
            scormdriver_lines = f.readlines()
            for line in scormdriver_lines:
                # SCORM 2004
                line = re.sub(r'function SCORM2004_SaveTime\(intMilliSeconds\){(.*?)}', r'function SCORM2004_SaveTime(intMilliSeconds){return 0;}', line)
                line = re.sub(r'function SCORM2004_SetScore\(intScore,intMaxScore,intMinScore\){(.*?)}', r'function SCORM2004_SetScore(intScore,intMaxScore,intMinScore){return 0;}', line)
                # SCORM 1.2
                line = re.sub(r'function SCORM_SaveTime\(intMilliSeconds\){(.*?)}', r'function SCORM_SaveTime(intMilliSeconds){return 0;}', line)
                line = re.sub(r'function SCORM_SetScore\(intScore,intMaxScore,intMinScore\){(.*?)}', r'function SCORM_SetScore(intScore,intMaxScore,intMinScore){return 0;}', line)
                new_script.append(line)

        with open(path, 'w') as f:
            f.writelines(new_script)
        return "Scormdriver.js has been modified!"
    except:
        print("Error scormdriver.js")
        return "Error modifying scormdriver.js, nothing changed!"

def change_runjs(path):
    try:
        with open(path, 'r') as f:
            runjs_lines = f.readlines()
            for line in runjs_lines:
                line = re.sub(r',(.\(.\.SESSION_TIME,.\),)(.\(.\.EXIT)', r',/*\1*/\2', line)
                print(line)
                new_script.append(line)

        with open(path, 'w') as f:
            f.writelines(new_script)
        return "run.js has been modified!"
    except:
        print("Error changing run.js")
        return "Error modifying run.js, nothing changed!"

def disable_time_score(path):
    if os.path.isfile(os.path.join(path, r'scormdriver\scormdriver.js')):
        print("Articulate Rise Content detected!")
        rise_path = os.path.join(path, r'scormdriver/scormdriver.js')
        change_articulate_scormdriver(rise_path)
    elif os.path.isfile(os.path.join(path, r'lms\scormdriver.js')):
        print("Articulate Storyline Content detected!")
        storyline_path = os.path.join(path, r'lms\scormdriver.js')
        change_articulate_scormdriver(storyline_path)
    elif os.path.isfile(os.path.join(path, r'com.tts.player\src\run.js')):
        print("TTKF Content detected!")
        ttkf_path = os.path.join(path, r'com.tts.player\src\run.js')
        change_runjs(ttkf_path, r'com.tts.player\src\run.js')
    else:
        print("No Articulate or TTKF Content found!")
        return "-"

