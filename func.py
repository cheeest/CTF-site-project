import os

def task1_flag(flag_task1, id):
    os.system('exiftool -all= static/imgs/task1.jpg')
    if not os.path.exists('/tmp/task1'):
        os.mkdir('/tmp/task1')
    os.system(f'cp static/imgs/task1.jpg /tmp/task1/{id}.jpg')
    os.system(f"exiftool -Comment='{flag_task1}' /tmp/task1/{id}.jpg")

