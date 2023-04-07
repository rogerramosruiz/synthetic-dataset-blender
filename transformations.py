import bpy
import random
from math import radians
from mathutils import Euler
from objOps import select
from camera import cam_box
from data import scale_min, scale_max, minrot, maxrot, prob_roate, prob_scale

def move(obj):
    max_y = bpy.context.scene.objects['Plane'].location[1] - obj.dimensions[1]
    rand_y = random.uniform(-1, max_y)
    obj.location[1] = rand_y 
    width, height = cam_box(obj)
    obj_width, _, obj_height = obj.dimensions    
    obj_width /= 2
    obj_height /= 2
    x = width - obj_width
    z = height - obj_height
    rand_x = random.uniform(-x, x)
    rand_z = random.uniform(-z , z)
    obj.location = (rand_x, rand_y, rand_z)
        
def rotate(obj): 
    if random.random() < prob_roate:
        rx = radians(random.uniform(minrot[0], maxrot[0]))
        ry = radians(random.uniform(minrot[1], maxrot[1]))
        rz = radians(random.uniform(minrot[2], maxrot[2])) 
        obj.rotation_euler = Euler((rx, ry, rz), 'XYZ')
    
def scale(obj):
    if random.random() < prob_scale:
        scale = random.uniform(scale_min, scale_max)
        scl = [scale for _ in range(3)]
        obj.scale = scl

def transform(obj):
    rotate(obj)
    scale(obj)
    select(obj)
    bpy.ops.object.transform_apply(rotation=True, scale=True)
    move(obj)
    select(obj)
    bpy.ops.object.transform_apply(location=True)