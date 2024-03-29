import openpyxl
import os
import subprocess
import zipfile
from pathlib import Path
from PIL import Image

# Variables
path = 'c:\\temp\\scorm\\'
unzip_path = 'c:\\temp\\scorm\\unzip\\'
unzipped_directories = []
#exif = 'c:\\temp\\exiftool.exe'
exif = './exiftool.exe'

# Methods
def checkAudioVideo(file_input):
    print("check audio/ video: " + str(file_input))
    metadata = []
    process = subprocess.Popen([exif, file_input], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, encoding='utf8', errors='ignore')
    for output in process.stdout:
        info = []
        line = output.strip().split(':')
        info.append(line[0].strip())
        info.append(line[1].strip())
        metadata.append(info)
    return metadata

def checkImage(file):
    print("check image: " + str(file))
    values = []
    # get image size
    size = int(os.path.getsize(file))
    size /= 1000
    values.append(['File Size', str(size)])

    # get image dimensions
    if file[-3:] != 'svg':
        img = Image.open(file)
        width, height = img.size
        values.append(['Image Width', str(width)])
        values.append(['Image Height', str(height)])
    if file[-3:] == 'peg':
        values.append(['File Type', 'JPEG'])
    else:
        values.append(['File Type', file[-3:].upper()])
    return values

def changeExcelColumnWidth(ws):
    cell = ['A','B','C','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T']
    for c in cell:
        ws.column_dimensions[c].width = 16
    ws.column_dimensions['A'].width = 110
    ws.column_dimensions['D'].width = 18
    ws.column_dimensions['T'].width = 20

def write_to_excel(media_data, unzip_dir):
    parent_path = Path(unzip_dir).parent
    #report_path = os.path.join(parent_path.parent, os.path.basename(os.path.dirname(unzip_dir)))
    report_path = Path(parent_path).parent
    restore_cwd = os.getcwd()
    os.chdir(report_path)
    wb = openpyxl.Workbook()
    ws = wb.active
    changeExcelColumnWidth(ws)
    ws.title = 'Info'
    for rows in media_data:
        ws.append(rows)
    report_filename = 'MEDIA-REPORT_' + os.path.basename(os.path.dirname(unzip_dir + "/imsmanifest.xml") + '.xlsx')
    print("Media-Report created: " + report_filename + "in directory " + str(report_path))

    # add filter
    ws.auto_filter.ref = "A1:Q2000"
    ws.auto_filter.add_filter_column(0, ['file path', 'file size KiB', 'file type', 'MIME Type', 'image width', 'image height', 'media duration', 'compressor name', 'frame rate', 'avg. bitrate', 'Encoder', 'Video Frame Rate', 'Major Brand', 'Duration', 'Compressor ID', 'Track Duration', 'Compatible Brands'])
    ws.auto_filter.add_sort_condition("B2:B2000")

    wb.save(report_filename)
    os.chdir(restore_cwd)

def filter_report(report, file_paths):
    print("Filtering media data for report.")
    data_final = [['file path', 'file size KiB', 'file type', 'MIME Type', 'image width', 'image height', 'media duration', 'compressor name', 'frame rate', 'avg. bitrate', 'Encoder', 'Video Frame Rate', 'Major Brand', 'Duration', 'Compressor ID', 'Track Duration', 'Compatible Brands']]
    # convert to dictionary
    file_counter = 0
    for media_file in report:
        row = []
        data_dict = {}
        for data in media_file:
            data_dict[data[0]] = data[1]
        try:
            row.append(file_paths[file_counter])
            file_counter += 1
        except:
            print("Warning: No more file paths to grab!")
        try:
            if "MiB" in data_dict.get('File Size'):
                row.append(float(data_dict.get('File Size').replace(' MiB', ''))*1000)
            elif "KiB" in data_dict.get('File Size'):
                row.append(float(data_dict.get('File Size').replace(' KiB', '')))
            elif "bytes" in data_dict.get('File Size'):
                row.append(float(data_dict.get('File Size').replace(' bytes', ''))/1000)
            else:
                row.append(float(data_dict.get('File Size')))
        except:
            row.append(data_dict.get('File Size')) if 'File Size' in data_dict else row.append("")
            print("Conversion of file size to float not possible:")
            print(data_dict.get('File Size')) if 'File Size' in data_dict else print("No File Size data present!")
        #row.append(data_dict.get('File Size')) if 'File Size' in data_dict else row.append("")
        row.append(data_dict.get('File Type')) if 'File Type' in data_dict else row.append("")
        row.append(data_dict.get('MIME Type')) if 'MIME Type' in data_dict else row.append(" ")
        row.append(data_dict.get('Image Width').replace("'", "")) if 'Image Width' in data_dict else row.append(" ")
        row.append(data_dict.get('Image Height').replace("'", "")) if 'Image Height' in data_dict else row.append(" ")
        #row.append(data_dict.get('Image Size')) if 'Image Size' in data_dict else row.append(" ")
        #row.append(data_dict.get('Megapixels')) if 'Megapixels' in data_dict else row.append(" ")
        row.append(data_dict.get('Media Duration')) if 'Media Duration' in data_dict else row.append(" ")
        row.append(data_dict.get('Compressor Name')) if 'Compressor Name' in data_dict else row.append(" ")
        row.append(data_dict.get('Video Frame Rate')) if 'Video Frame Rate' in data_dict else row.append(" ")
        row.append(data_dict.get('Avg Bitrate')) if 'Avg Bitrate' in data_dict else row.append(" ")
        row.append(data_dict.get('Encoder')) if 'Encoder' in data_dict else row.append(" ")
        row.append(data_dict.get('Video Frame Rate')) if 'Video Frame Rate' in data_dict else row.append(" ")
        row.append(data_dict.get('Major Brand')) if 'Major Brand' in data_dict else row.append(" ")
        row.append(data_dict.get('Duration')) if 'Duration' in data_dict else row.append(" ")
        row.append(data_dict.get('Compressor ID')) if 'Compressor ID' in data_dict else row.append(" ")
        row.append(data_dict.get('Track Duration')) if 'Track Duration' in data_dict else row.append(" ")
        row.append(data_dict.get('Compatible Brands')) if 'Compatible Brands' in data_dict else row.append(" ")
        #row.append(data_dict.get('Encoding Process')) if 'Encoding Process' in data_dict else row.append(" ")

        data_final.append(row)
        #print(row)
    return data_final

# Unzip all zip-files in unzip directory
def unzipScormFiles(scorm_path):
    for file in os.listdir(scorm_path):
        if file.endswith('.zip'):
            # print("Unzipping " + file)
            with zipfile.ZipFile(path + file, 'r') as zip_ref:
                new_directory = unzip_path + file[:-4]
                zip_ref.extractall(new_directory)
                unzipped_directories.append(new_directory)

# find all images and videos of unzipped content
def checkMediaFiles(directories, svg_exclude):
    print("Checking media files...")
    for unzip_dir in directories:
        report = []
        # list of all media file paths (to put into report)
        file_paths = []
        exclude = set(['com.tts.player'])
        for folder, subfolders, filenames in os.walk(unzip_dir, topdown=True):
            if svg_exclude:
                subfolders[:] = [d for d in subfolders if d not in exclude]
            for file in filenames:
                # search for images, videos, audios (checkbox svg due to massive .svg files in ttkf projects!)
                if file.endswith('.svg'):
                    #print(os.path.join(folder, file).replace('/', '\\'))
                    report.append(checkImage(os.path.join(folder, file).replace('/', '\\')))
                    file_paths.append(os.path.join(folder, file).replace('/', '\\'))
                elif file.endswith('.png') or file.endswith('.jpg') or file.endswith('.gif') or file.endswith('.jpeg') or file.endswith('.bmp') or file.endswith('.tiff') or file.endswith('.tif') or file.endswith('.avif') or file.endswith('.webp'):
                    report.append(checkImage(os.path.join(folder, file).replace('/', '\\')))
                    file_paths.append(os.path.join(folder, file).replace('/', '\\'))
                elif file.endswith('.mpeg') or file.endswith('.mp4') or file.endswith('.mov') or file.endswith('.ogg') or file.endswith('.avi') or file.endswith('.wmv') or file.endswith('.mkv') or file.endswith('.flv') or file.endswith('.swf') or file.endswith('pdf'):
                    #print(os.path.join(folder, file).replace('/', '\\'))
                    file_paths.append(os.path.join(folder, file).replace('/', '\\'))
                    report.append(checkAudioVideo(os.path.join(folder, file).replace('/', '\\')))
                elif file.endswith('.mp3') or file.endswith('.ogv') or file.endswith('.aac') or file.endswith('.wav') or file.endswith('.mpg') or file.endswith('.mpeg') or file.endswith('.m2v'):
                    #print(os.path.join(folder, file).replace('/', '\\'))
                    file_paths.append(os.path.join(folder, file).replace('/', '\\'))
                    report.append(checkAudioVideo(os.path.join(folder, file).replace('/', '\\')))
    # create report for each unzipped SCORM package
    report_filtered = filter_report(report, file_paths)
    restore_cwd = os.getcwd()
    os.chdir(unzip_dir)
    write_to_excel(report_filtered, unzip_dir)
    os.chdir(restore_cwd)