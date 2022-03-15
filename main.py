import sys
import bpy
from pathlib import Path
import bpy_extras
import random
import os
import string

sys.path.append(r'C:/Users/Roger/Documents/synthetic_dataset')
from transformations import transform
from objOps import delete
from background import changeBackground

def convertYolo(x1,y1,x2,y2, shape):
    x = ((x1 + x2) / 2) / shape[1]
    y = ((y1 + y2) / 2) / shape[0]
    h = abs(y1 - y2) / shape[0]
    w = abs(x2 - x1) / shape[1]
    return x, y, w, h

def boundingBox(obj, yoloFormat = False):
    renderScale = scene.render.resolution_percentage / 100
    width  = int(scene.render.resolution_x * renderScale)
    height = int(scene.render.resolution_y * renderScale)
    mat   = obj.matrix_world
    x, y, _ = bpy_extras.object_utils.world_to_camera_view(scene, cam, obj.data.vertices[0].co)
    left = right = x
    top = bottom = y

    for i in obj.data.vertices:
        glob = mat @ i.co
        x, y, _  = bpy_extras.object_utils.world_to_camera_view(scene, cam, glob)
        left = min(left, x)
        right = max(right, x)
        top = max(top, y)
        bottom = min(bottom, y)

    p1 = (int(left * width), height - int(top *  height))
    p2 = (int(right * width), height - int(bottom * height))  
   # if coordenates exceed the frame then corop the boundingBox
    p1 = (max(p1[0], 0), max(p1[1], 0))
    p2 = (min(p2[0], width), min(p2[1], height))
    if yoloFormat:
        return convertYolo(p1[0], p1[1], p2[0], p2[1], (height, width))
    return p1, p2 

def randomFilename():
    name = ''.join(random.choice(letters) for _ in range(filenameSize))
    return f'{saveDir}/{name}'

    
def save(objs, colls):
    """
    Definitely change the names of this things
    """
    # filename = randomFilename()
    filename = f'{saveDir}/{imgIndex}'
    bpy.context.scene.render.filepath = f'{filename}.png'
    with open (f'{filename}.txt', 'w') as f:
        ln = len(objs)
        for i in range(len(objs)):
            x, y, w, h = boundingBox(objs[i], True)
            f.write(f'{revnames[colls[i]]} {x} {y} {w} {h}')
            if i != ln - 1 :
                f.write('\n')  
    bpy.ops.render.render(write_still = True)

def renderMany():
    directory = Path('C:/Users/Roger/Documents/Backgrounds')
    outputPath = Path('E:/images')
    i = 0
    for f in directory.iterdir():
        img = changeBackground(str(f))
        bpy.context.scene.render.filepath = str(outputPath / f'{str(i).zfill(6)}.png')
        bpy.ops.render.render(write_still = True)
        i += 1
        bpy.data.images.remove(img)

def intersersct(obj1,obj2):
    # Boundingbox the objects
    o1p1, o1p2 = boundingBox(obj1)
    o2p1, o2p2  = boundingBox(obj2)
    return o1p1[0] < o2p2[0] and o1p2[0] > o2p1[0] and o1p1[1] < o2p2[1] and o1p2[1] > o2p1[1] 

def init():
    revNames = {}
    ln = len(collections)
    with open('classes.txt', 'w') as f:
        for i in range(ln):
            collections[i].hide_render = True
            f.write(collections[i].name)
            revNames[collections[i].name] = i
            if i != ln -1:
                f.write('\n')
    return revNames
        
def chooseObjs(collection):
    colls = [collection.name]
    renderObjs = [random.choice(collection.all_objects).name]
    for i in collections:
        if random.random() > 0.6:
            renderObjs.append(random.choice(i.all_objects).name)
            colls.append(i.name)
    return renderObjs, colls

def useCollection(collection):
    renObjs, colls = chooseObjs(collection)
    objects = []
    global imgIndex
    img = changeBackground(imgs[imgIndex])
    imgIndex = (imgIndex + 1) % lnImg
    for i in renObjs:
        objc = bpy.context.scene.objects[i].copy()
        objc.data = bpy.context.scene.objects[i].data.copy()
        bpy.context.scene.collection.objects.link(objc)
        objc.hide_render = False
        transform(objc)
        b = True
        for _ in range(100):
            for o in objects:
                b = b and not intersersct(o, objc)            
            if b:
                objects.append(objc)
                break
            else:
                objc.data = bpy.context.scene.objects[i].data.copy()
                transform(objc)
                b = True
        if not b:
            delete(obj)
    save(objects, colls)
    for obj in objects:
        delete(obj)
    bpy.data.images.remove(img)
    

if __name__ == '__main__':
    letters = string.ascii_lowercase + string.ascii_uppercase
    filenameSize = 10
    saveDir = 'E:/Devs/Python/readyolo/dataset/'
    imgDir = 'C:/Users/Roger/Documents/Backgrounds'
    imgIndex = 0
    imgs = [os.path.join(imgDir, i) for i in os.listdir(imgDir)]
    lnImg = len(imgs)

    cam   = bpy.data.objects['Camera']
    scene = bpy.context.scene
    collectionname = 'Objects'
    collections = bpy.data.collections[collectionname].children
    revnames = init()

    if not os.path.exists(saveDir):
        os.mkdir(saveDir)
    n = 2
    for i in collections:
        for _ in range(n):
            useCollection(i)