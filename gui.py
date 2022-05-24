import tkinter as tk
from tkinter import filedialog, IntVar, Checkbutton, Tk


#customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
#customtkinter.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green

check_media_files = True


def clearLabels():
    label_scorm = tk.Label(root, textvariable=text_empty, anchor="c", bg='grey')
    label_scorm.place(x=20, y=20, width=460, height=30)
    label_namespace = tk.Label(root, textvariable=text_empty, anchor="c", bg='grey')
    label_namespace.place(x=20, y=50, width=460, height=30)
    label_item = tk.Label(root, textvariable=text_empty, anchor="c", bg='grey')
    label_item.place(x=20, y=80, width=460, height=30)
    label_characters = tk.Label(root, textvariable=text_empty, anchor="c", bg='grey')
    label_characters.place(x=20, y=110, width=460, height=30)
    label_ttkf = tk.Label(root, textvariable=text_empty, anchor="c", bg='grey')
    label_ttkf.place(x=20, y=140, width=460, height=30)
    label_status = tk.Label(root, textvariable=text_empty, anchor="c", bg='grey')
    label_status.place(x=20, y=170, width=460, height=30)

def setLabelStatus(text, color):
    text_status.set(text)
    label_status = tk.Label(root, textvariable=text_status, anchor="c", bg=color)
    label_status.place(x=20, y=170, width=460, height=30)

def setLabelTtkf(text, color):
    text_ttkf.set(text)
    label_ttkf = tk.Label(root, textvariable=text_ttkf, anchor="c", bg=color)
    label_ttkf.place(x=20, y=140, width=460, height=30)

def setNamespaceLabel(text, color):
    text_namespace.set(text)
    label_namespace = tk.Label(root, textvariable=text_namespace, anchor="c", bg=color)
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

root = Tk()  # create CTk window like you do with the Tk window

root.geometry("500x400")
root.configure(bg='grey')

text_scorm, text_namespace, text_item, text_characters, text_ttkf, text_status, text_empty = tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar()
text_empty.set("")
text_scorm.set("SCORM Version:")
text_namespace.set("Namespace check (adlnav):")
text_item.set("Only one Item check:")
text_characters.set("Special characters check:")
text_ttkf.set("TTKF Assessment check:")
text_status.set("Overall status:")
root.title('SIT | SCORM Tester v2.5 | 23.05.2022')

# Buttons

btn_quit = tk.Button(root, text="Quit", command=lambda: root.destroy(), bg='grey')
btn_quit.place(x=180, y=320, width=140, height=30)

checkbox_media_test = IntVar()
checkbox_media_test.set(True)
tk.Checkbutton(root, text="Create Media Files Report", command=toggleMediaCheck, variable=checkbox_media_test, bg='grey').place(x=40, y=215)

checkbox_runjs = IntVar()
checkbox_runjs.set(True)
tk.Checkbutton(root, text="Replace run.js (if TTKF Assessment)", variable=checkbox_runjs, bg='grey').place(x=250, y=215)

checkbox_svg = IntVar()
checkbox_svg.set(True)
tk.Checkbutton(root, text="exclude ttkf player directory", command=toggleSvgCheck, variable=checkbox_svg, bg='grey').place(x=40, y=240)

checkbox_lms = IntVar()
checkbox_lms.set(False)
tk.Checkbutton(root, text="LMS-Upload (beta)", variable=checkbox_lms, bg='grey').place(x=250, y=240)

# Labels
label_group = tk.Label(root, borderwidth=2, relief="groove", bg='grey')
label_group.place(x=10, y=10, width=480, height=200)
label_scorm = tk.Label(root, textvariable=text_scorm, anchor="c", bg='grey')
label_scorm.place(x=20, y=20, width=460, height=30)
label_namespace = tk.Label(root, textvariable=text_namespace, anchor="c", bg='grey')
label_namespace.place(x=20, y=50, width=460, height=30)
label_item = tk.Label(root, textvariable=text_item, anchor="c", bg='grey')
label_item.place(x=20, y=80, width=460, height=30)
label_characters = tk.Label(root, textvariable=text_characters, anchor="c", bg='grey')
label_characters.place(x=20, y=110, width=460, height=30)
label_ttkf = tk.Label(root, textvariable=text_ttkf, anchor="c", bg='grey')
label_ttkf.place(x=20, y=140, width=460, height=30)
label_status = tk.Label(root, textvariable=text_status, anchor="c", bg='grey')
label_status.place(x=20, y=170, width=460, height=30)