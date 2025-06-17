
import os



def testkey(basedir, key):
    counter = 0
    folderlist = os.listdir(basedir)
    for folders in folderlist:
        fullpath = os.path.join(basedir, folders)
        if os.path.isdir(fullpath):
            for img in os.scandir(fullpath):
                if f'{key}' in img.name:
                    counter+=1
    print(f'sum of {key} is {counter}')
    return counter

def testfull(basedir):
    counter = 0
    folderlist = os.listdir(basedir)
    for folders in folderlist:
        fullpath = os.path.join(basedir, folders)
        if os.path.isdir(fullpath):
            for img in os.scandir(fullpath):
                if img.is_file():
                    counter += 1
    print (counter)
    return counter

def renamer(filepath, newname, key):
    filename = os.path.basename(filepath)
    if key in filename and os.path.isfile(filepath):
        name, ext = os.path.splitext(filepath)
        newpath = os.path.join(os.path.dirname(filepath), f"{newname}{ext}")
        counter = 1

        while os.path.exists(newpath):
            newpath = os.path.join(os.path.dirname(filepath), f"{newname}_{counter}{ext}")
            counter += 1

        os.rename(filepath, newpath)
        print(f"Переименован: {filepath} → {newpath}")


def renamer_with_counter(directory, newname, key):
    counter = 0
    for files in os.scandir(directory):
        if key in files.name:
            oldpath = files.path
            newpath = os.path.join(directory, f'{newname}{counter}.jpeg')
            os.rename(oldpath, newpath)
            counter += 1
    print('successful')


