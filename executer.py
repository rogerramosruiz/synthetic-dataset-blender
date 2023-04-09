import os
import time
import platform
import subprocess

# total images to render per class
images_per_classs = 1

# images to render per execution
max_imgs = 3

blender_file = "start_1.blend"


n = images_per_classs // max_imgs
rest = images_per_classs % max_imgs


def blender_location():
    if platform.system() == 'Windows':
        # find the location of instalation of blender
        # where command donse't work for the space in the path
        default_path = 'C:\Program Files\Blender Foundation'
        latest = os.listdir(default_path)[-1]
        return os.path.join(default_path, latest, 'blender')

    return subprocess.check_output(['which', 'blender']).decode('utf-8').strip()


blender_command = blender_location()

def render():
    subprocess.run([blender_command, blender_file, "--background", "--python", "main.py"])

def edit(n, i):
    """
    Edit data.py for updates in images_per_class 
    """
    file = 'data.py'
    with open(file, 'r') as f:
        lines = f.readlines()
    with open(file, 'w') as f:
        for line in lines:
            if 'images_per_class' in line:
                img_class = max_imgs if i != n else rest
                f.write(f"images_per_class = {img_class}\n")
            else:
                f.write(line)

def main():
    total = 0
    starttime = time.time()
    for i in range(n + 1):
        edit(n, i)
        render()
        total += max_imgs if i != n else rest
    totaltime = time.time() - starttime
    print(f"Executer time", totaltime)

if __name__ == '__main__':
    main()