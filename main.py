import sys
import time
import bpy
import random
import os
import string

sys.path.append('.')
from transformations import transform
from objOps import delete
from background import change_background
from camera import bounding_box, change_focal_length
from utils import init, progress
from data import filenameSize, saveDir, imgDir, images_per_class, prob_many_objs, prob_add_obj, collection_start, collection_end
from color import shift_color

def save(objs, colls):
    file_name = random_filename()
    while os.path.exists(f'{file_name}.jpg'):
        file_name = random_filename()
    bpy.context.scene.render.filepath = f'{file_name}'
    with open (f'{file_name}.txt', 'w') as f:
        ln = len(objs)
        for i in range(len(objs)):
            x, y, w, h = bounding_box(objs[i], True)
            f.write(f'{names[colls[i]]} {x} {y} {w} {h}')
            if i != ln - 1 :
                f.write('\n')  
    bpy.ops.render.render(write_still = True)

def intersersct(obj1, obj2):
    # Boundingbox the objects
    o1p1, o1p2 = bounding_box(obj1)
    o2p1, o2p2  = bounding_box(obj2)
    return o1p1[0] < o2p2[0] and o1p2[0] > o2p1[0] and o1p1[1] < o2p2[1] and o1p2[1] > o2p1[1] 

def random_filename():
    letters = string.ascii_lowercase + string.ascii_uppercase
    name = ''.join(random.choice(letters) for _ in range(filenameSize))
    return f'{saveDir}/{name}'
        
def choose_objs(collection):
    collections_names = [collection.name]
    render_objs = [random.choice(collection.all_objects).name]
    if random.random() < prob_many_objs:
        for i in collections:
            if random.random() < prob_add_obj:
                render_objs.append(random.choice(i.all_objects).name)
                collections_names.append(i.name)
    return render_objs, collections_names

def use_collection(collection):
    change_focal_length()
    ren_objs, colls = choose_objs(collection)
    objects = []
    materials = []
    img = change_background(random.choice(imgs))
    for i in ren_objs:
        obj_copy = bpy.context.scene.objects[i].copy()
        obj_copy.data = bpy.context.scene.objects[i].data.copy()
        bpy.context.scene.collection.objects.link(obj_copy)
        obj_copy.hide_render = False
        transform(obj_copy)
        materials += shift_color(obj_copy, bpy.context.scene.objects[i].users_collection[0].name) 
        b = True
        for j in range(100):
            for o in objects:
                b = b and not intersersct(o, obj_copy)            
            if b:
                objects.append(obj_copy)
                break
            elif j != 99:
                obj_copy.data = bpy.context.scene.objects[i].data.copy()
                transform(obj_copy)
                b = True
        if not b:
            delete(obj_copy)
    save(objects, colls)
    for obj in objects:
        delete(obj)
    bpy.data.images.remove(img)
    for material in materials:
        bpy.data.materials.remove(material)

def main(n):
    b = False
    for i in collections:
        if i.name == collection_start:
            b = True
        if b:
            for j in range(n):
                use_collection(i)
                progress(i.name, j+1, n)
            progress(i.name)
        if i.name == collection_end:
            break

if __name__ == '__main__':
    start_time = time.time()
    imgs           = [os.path.join(imgDir, i) for i in os.listdir(imgDir)]
    collections    = bpy.data.collections['Objects'].children
    names          = init(collections, saveDir)
    main(images_per_class)
    total_time =  time.time() - start_time    
    print('Total time:', total_time)