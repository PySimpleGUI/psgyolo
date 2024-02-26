'''
Copyright 2019-2023 PySimpleSoft, Inc. and/or its licensors. All rights reserved.

Redistribution, modification, or any other use of PySimpleGUI or any portion thereof is subject
to the terms of the PySimpleGUI License Agreement available at https://eula.pysimplegui.com.

You may not redistribute, modify or otherwise use PySimpleGUI or its contents except pursuant
to the PySimpleGUI License Agreement.
'''

version = '5.0.0'
__version__ = version.split()[0]

"""
    Demo of YOLO object detection with a WebCam using PySimpleGUI
    The YOLO detection code was provided courtsey of Dr. Adrian Rosebrock of the pyimagesearch organization.
    https://www.pyimagesearch.com
    If you use this program, you agree to keep this header in place.
    It's OK to build on other people's works, it's not ok to remove their credits and claim the work as your own.
"""

import numpy as np
import time
import cv2
import os
import PySimpleGUI as sg
import urllib.request
import sys

URL_FILE = r'https://www.dropbox.com/s/uf00d4ov6fmw0he/yolov3.weights?dl=1'
UA_FOR_URLLIB = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'


'''
M""M                     dP            dP dP                   
M  M                     88            88 88                   
M  M 88d888b. .d8888b. d8888P .d8888b. 88 88 .d8888b. 88d888b. 
M  M 88'  `88 Y8ooooo.   88   88'  `88 88 88 88ooood8 88'  `88 
M  M 88    88       88   88   88.  .88 88 88 88.  ... 88       
M  M dP    dP `88888P'   dP   `88888P8 dP dP `88888P' dP       
MMMM
'''


def pip_install_thread(window, sp):
    window.write_event_value('-THREAD-', (sp, 'Install thread started'))
    for line in sp.stdout:
        oline = line.decode().rstrip()
        window.write_event_value('-THREAD-', (sp, oline))



def pip_install_latest():

    pip_command = '-m pip install --upgrade --no-cache-dir PySimpleGUI>=5'

    python_command = sys.executable  # always use the currently running interpreter to perform the pip!
    if 'pythonw' in python_command:
        python_command = python_command.replace('pythonw', 'python')

    layout = [[sg.Text('Installing PySimpleGUI', font='_ 14')],
              [sg.Multiline(s=(90, 15), k='-MLINE-', reroute_cprint=True, reroute_stdout=True, echo_stdout_stderr=True, write_only=True, expand_x=True, expand_y=True)],
              [sg.Push(), sg.Button('Downloading...', k='-EXIT-'), sg.Sizegrip()]]

    window = sg.Window('Pip Install PySimpleGUI Utilities', layout, finalize=True, keep_on_top=True, modal=True, disable_close=True, resizable=True)

    window.disable_debugger()

    sg.cprint('Installing with the Python interpreter =', python_command, c='white on purple')

    sp = sg.execute_command_subprocess(python_command, pip_command, pipe_output=True, wait=False)

    window.start_thread(lambda: pip_install_thread(window, sp), end_key='-THREAD DONE-')

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or (event == '-EXIT-' and window['-EXIT-'].ButtonText == 'Done'):
            break
        elif event == '-THREAD DONE-':
            sg.cprint('\n')
            show_package_version('PySimpleGUI')
            sg.cprint('Done Installing PySimpleGUI.  Click Done and the program will restart.', c='white on red', font='default 12 italic')
            window['-EXIT-'].update(text='Done', button_color='white on red')
        elif event == '-THREAD-':
            sg.cprint(values['-THREAD-'][1])

    window.close()

def suggest_upgrade_gui():
    layout = [[sg.Image(sg.EMOJI_BASE64_HAPPY_GASP), sg.Text(f'PySimpleGUI 5+ Required', font='_ 15 bold')],
              [sg.Text(f'PySimpleGUI 5+ required for this program to function correctly.')],
              [sg.Text(f'You are running PySimpleGUI {sg.version}')],
              [sg.Text('Would you like to upgrade to the latest version of PySimpleGUI now?')],
              [sg.Push(), sg.Button('Upgrade', size=8, k='-UPGRADE-'), sg.Button('Cancel', size=8)]]

    window = sg.Window(title=f'Newer version of PySimpleGUI required', layout=layout, font='_ 12')

    while True:
        event, values = window.read()

        if event in (sg.WIN_CLOSED, 'Cancel'):
            window.close()
            break
        elif event == '-UPGRADE-':
            window.close()
            pip_install_latest()
            sg.execute_command_subprocess(sys.executable, __file__, pipe_output=True, wait=False)
            break


def make_str_pre_38(package):
    return f"""
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
import pkg_resources
try:
    ver=pkg_resources.get_distribution("{package}").version.rstrip()
except:
    ver=' '
print(ver, end='')
"""

def make_str(package):
    return f"""
import importlib.metadata

try:
    ver = importlib.metadata.version("{package}")
except importlib.metadata.PackageNotFoundError:
    ver = ' '
print(ver, end='')
"""


def show_package_version(package):
    """
    Function that shows all versions of a package
    """
    interpreter = sg.execute_py_get_interpreter()
    sg.cprint(f'{package} upgraded to ', end='', c='red')
    # print(f'{interpreter}')
    if sys.version_info.major == 3 and sys.version_info.minor in (6, 7):  # if running Python version 3.6 or 3.7
        pstr = make_str_pre_38(package)
    else:
        pstr = make_str(package)
    temp_file = os.path.join(os.path.dirname(__file__), 'temp_py.py')
    with open(temp_file, 'w') as file:
        file.write(pstr)
    sg.execute_py_file(temp_file, interpreter_command=interpreter, pipe_output=True, wait=True)
    os.remove(temp_file)



def upgrade_check():
    if not sg.version.startswith('5'):
        suggest_upgrade_gui()
        exit()


# M""MMMM""M MMP"""""YMM M""MMMMMMMM MMP"""""YMM
# M. `MM' .M M' .mmm. `M M  MMMMMMMM M' .mmm. `M
# MM.    .MM M  MMMMM  M M  MMMMMMMM M  MMMMM  M
# MMMb  dMMM M  MMMMM  M M  MMMMMMMM M  MMMMM  M
# MMMM  MMMM M. `MMM' .M M  MMMMMMMM M. `MMM' .M
# MMMM  MMMM MMb     dMM M         M MMb     dMM
# MMMMMMMMMM MMMMMMMMMMM MMMMMMMMMMM MMMMMMMMMMM
#
# MM'""""'YMM                dP
# M' .mmm. `M                88
# M  MMMMMooM .d8888b. .d888b88 .d8888b.
# M  MMMMMMMM 88'  `88 88'  `88 88ooood8
# M. `MMM' .M 88.  .88 88.  .88 88.  ...
# MM.     .dM `88888P' `88888P8 `88888P'
# MMMMMMMMMMM


def download_weights_file(save_to_filename):
    '''
    Download the weights file from the internet and save
    :param save_to_filename:    the filename to save
    '''
    try:
        req = urllib.request.Request(URL_FILE, headers={'User-Agent': UA_FOR_URLLIB})
        res = urllib.request.urlopen(req)
        data = res.read()
        with open(save_to_filename, 'wb') as f:
            f.write(data)
    except Exception as e:
        print(f'Error Occurred {e}')


def main():
    sg.user_settings_filename(filename='psgyolo.json')
    upgrade_check()
    folder = os.path.dirname(__file__)
    y_path = r'yolo-coco'

    sg.theme('LightGreen')
    DEFAULT_FONT = '_ 14'
    sg.set_options(font=DEFAULT_FONT)

    gui_confidence = .5     # initial settings
    gui_threshold = .3      # initial settings
    camera_number = 0       # if you have more than 1 camera, change this variable to choose which is used

    cap = cv2.VideoCapture(camera_number)  # initialize the capture device
    grabbed, frame = cap.read()
    if not grabbed:
        sg.popup('Exiting program without detecting a video feed.' ,'Maybe the camera is disconnected?')
        return

    # load the COCO class labels our YOLO model was trained on
    labelsPath = os.path.sep.join([folder, y_path, "coco.names"])
    LABELS = open(labelsPath).read().strip().split("\n")

    # initialize a list of colors to represent each possible class label
    np.random.seed(42)
    COLORS = np.random.randint(0, 255, size=(len(LABELS), 3), dtype="uint8")

    # derive the paths to the YOLO weights and model configuration
    weightsPath = os.path.sep.join([folder, y_path, "yolov3.weights"])
    configPath = os.path.sep.join([folder, y_path, "yolov3.cfg"])
    yolov3_weights_filename = os.path.abspath(os.path.sep.join((folder, y_path, 'yolov3.weights')))
    if not os.path.exists(yolov3_weights_filename):
        if sg.popup_yes_no('Yolo V3 Weights file not found.  Would you like to download this 240 MB file?') != 'Yes':
            sg.popup('In order to run this application, you must:',
                     '* Download the weights file',
                     '* Name it "yolov3.weights"',
                     f'* Place the file in the folder {os.path.dirname(yolov3_weights_filename)}',
                     'Click OK to exit program', title='Weights Required')
            exit()
        sg.popup_quick_message('Downloading the YOLO weights file.', 'It may take some time depending on your internet connection.')

        download_weights_file(yolov3_weights_filename)

    # load our YOLO object detector trained on COCO dataset (80 classes)
    # and determine only the *output* layer names that we need from YOLO
    sg.popup_quick_message('Loading YOLO weights from disk.... one moment...')

    net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)
    ln = net.getLayerNames()
    # ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]        # old code changed on Feb-4-2022
    ln = [ln[i - 1] for i in net.getUnconnectedOutLayers()]

    # initialize the video stream, pointer to output video file, and
    # frame dimensions
    W, H = None, None
    win_started = False
    while True:
        # read the next frame from the file or webcam
        grabbed, frame = cap.read()

        # if the frame was not grabbed, then we stream has stopped so break out
        if not grabbed:
            break

        # if the frame dimensions are empty, grab them
        if not W or not H:
            (H, W) = frame.shape[:2]

        # construct a blob from the input frame and then perform a forward
        # pass of the YOLO object detector, giving us our bounding boxes
        # and associated probabilities
        blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416),
                                     swapRB=True, crop=False)
        net.setInput(blob)
        start = time.time()
        layerOutputs = net.forward(ln)
        end = time.time()

        # initialize our lists of detected bounding boxes, confidences,
        # and class IDs, respectively
        boxes = []
        confidences = []
        classIDs = []

        # loop over each of the layer outputs
        for output in layerOutputs:
            # loop over each of the detections
            for detection in output:
                # extract the class ID and confidence (i.e., probability)
                # of the current object detection
                scores = detection[5:]
                classID = np.argmax(scores)
                confidence = scores[classID]

                # filter out weak predictions by ensuring the detected
                # probability is greater than the minimum probability
                if confidence > gui_confidence:
                    # scale the bounding box coordinates back relative to
                    # the size of the image, keeping in mind that YOLO
                    # actually returns the center (x, y)-coordinates of
                    # the bounding box followed by the boxes' width and
                    # height
                    box = detection[0:4] * np.array([W, H, W, H])
                    (centerX, centerY, width, height) = box.astype("int")

                    # use the center (x, y)-coordinates to derive the top
                    # and and left corner of the bounding box
                    x = int(centerX - (width / 2))
                    y = int(centerY - (height / 2))

                    # update our list of bounding box coordinates,
                    # confidences, and class IDs
                    boxes.append([x, y, int(width), int(height)])
                    confidences.append(float(confidence))
                    classIDs.append(classID)

        # apply non-maxima suppression to suppress weak, overlapping bounding boxes
        idxs = cv2.dnn.NMSBoxes(boxes, confidences, gui_confidence, gui_threshold)

        # ensure at least one detection exists
        if len(idxs) > 0:
            # loop over the indexes we are keeping
            for i in idxs.flatten():
                # extract the bounding box coordinates
                (x, y) = (boxes[i][0], boxes[i][1])
                (w, h) = (boxes[i][2], boxes[i][3])
                # draw a bounding box rectangle and label on the frame
                color = [int(c) for c in COLORS[classIDs[i]]]
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                text = "{}: {:.4f}".format(LABELS[classIDs[i]],
                                           confidences[i])
                cv2.putText(frame, text, (x, y - 5),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        imgbytes = cv2.imencode('.ppm', frame)[1].tobytes()
        #-----------------------------
        # MM'"""""`MM M""MMMMM""M M""M
        # M' .mmm. `M M  MMMMM  M M  M
        # M  MMMMMMMM M  MMMMM  M M  M
        # M  MMM   `M M  MMMMM  M M  M
        # M. `MMM' .M M  `MMM'  M M  M
        # MM.     .MM Mb       dM M  M
        # MMMMMMMMMMM MMMMMMMMMMM MMMM
        #
        #                         dP
        #                         88
        # .d8888b. .d8888b. .d888b88 .d8888b.
        # 88'  `"" 88'  `88 88'  `88 88ooood8
        # 88.  ... 88.  .88 88.  .88 88.  ...
        # `88888P' `88888P' `88888P8 `88888P'
        #------------------------------------
        if not win_started:
            win_started = True
            layout = [[sg.Image(size=(W,H), key='-IMAGE-')],
                      [sg.Text('Confidence', s=20, justification='r'), sg.Slider(range=(0, 10), orientation='h', resolution=1, default_value=5, size=(15, 15), key='-CONFIDENCE-')],
                      [sg.Text('Threshold', s=20, justification='r'), sg.Slider(range=(0, 10), orientation='h', resolution=1, default_value=3, size=(15, 15), key='-THRESHOLD-')],
                      [sg.Exit()]]
            window = sg.Window('YOLO Webcam Demo', layout, right_click_menu=sg.MENU_RIGHT_CLICK_EDITME_VER_EXPLORER_EXIT, auto_save_location=True, finalize=True)
            image_elem = window['-IMAGE-']     # type: sg.Image
        else:
            image_elem.update(imgbytes)
        event, values = window.read(timeout=0)      # use a timeout of 0 on the read... assume reading frames will set the pace

        if event is None or event == 'Exit':
            break
        elif event == 'Edit Me':
            sg.execute_editor(__file__)
        elif event == 'Version':
            sg.popup_scrolled( f'This Program: {__file__} version {version}', sg.get_versions(), keep_on_top=True, location=window.current_location(), no_buttons=True, no_sizegrip=True)
        elif event == 'Show in Explorer':
            sg.execute_file_explorer(os.path.dirname(__file__))

        gui_confidence = int(values['-CONFIDENCE-']) / 10
        gui_threshold = int(values['-THRESHOLD-']) / 10

    if win_started:
        window.close()
    else:
        sg.popup('Exiting program without detecting a video feed.' ,'Maybe the camera is disconnected?')


if __name__ == '__main__':
    main()
