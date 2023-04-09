import os 

prog = {}

def convert_yolo(x1,y1,x2,y2, shape):
    x = ((x1 + x2) / 2) / shape[1]
    y = ((y1 + y2) / 2) / shape[0]
    h = abs(y1 - y2) / shape[0]
    w = abs(x2 - x1) / shape[1]
    return x, y, w, h

def distance(a, b):
    """
    Returns the distance between two blender meshes
    """
    d = a.location - b.location
    for i in range(len(d)):
        d[i] = abs(d[i])        
    return d

def init(collections, path):
    """
    Initialization
    Creates a directory to renderthe images and saves 
    the classes.txt with all the collections names
    """
    if not os.path.exists(path):
        os.mkdir(path)
    names = {}
    ln = len(collections)
    with open(os.path.join(path, 'classes.txt'), 'w') as f:
        for i in range(ln):
            collections[i].hide_render = True
            f.write(collections[i].name)
            names[collections[i].name] = i
            if i != ln -1:
                f.write('\n')
    return names

def save():
    with open('progress.txt', 'w') as f:
        for i, v in prog.items():
            f.write(f'{i}:{v}\n')

def read():
    if not os.path.exists('progress.txt'):
        return
    with open('progress.txt', 'r') as f:
        for i in f.read().splitlines():
            vals  = i.split(':')
            prog[vals[0]] = int(vals[1])


def progress(colname):
    """
    Save in a txt file the progress made
    """
    if len(prog) == 0:
        read()
    prog[colname] = prog[colname] + 1 if colname in prog else 1
    save()