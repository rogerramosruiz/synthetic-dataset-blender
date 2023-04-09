import bpy
import random
from math import radians
from mathutils import Euler
from objOps import select
from camera import cam_box
from data import scale_min, scale_max, min_rot, max_rot, prob_roate, prob_scale

def move(obj):
    """
    Move a blender mesh to a random place with in the bounds of the background image (Plane) and
    within the camera's view
    """
    # maximum value in y that the object can fit without loosin itself behind the plane
    max_y = bpy.context.scene.objects['Plane'].location[1] - obj.dimensions[1]
    rand_y = random.uniform(-1, max_y)
    # update object mesh y random location
    obj.location[1] = rand_y 
    # camera's render view width and height at the location of the object mesh
    width, height = cam_box(obj)
    # calculate the maximum bound in X, Z coordenates that the object can be fit with in the camera render view
    obj_width, _, obj_height = obj.dimensions    
    obj_width /= 2
    obj_height /= 2
    x = width - obj_width
    z = height - obj_height
    # random location with in the bound of the camera view
    rand_x = random.uniform(-x, x)
    rand_z = random.uniform(-z , z)
    obj.location = (rand_x, rand_y, rand_z)
        
def rotate(obj): 
    """
    Rotate a blender object mesh randomly defined by minrot and by maxrot
    """
    if random.random() < prob_roate:
        rx = radians(random.uniform(min_rot[0], max_rot[0]))
        ry = radians(random.uniform(min_rot[1], max_rot[1]))
        rz = radians(random.uniform(min_rot[2], max_rot[2])) 
        obj.rotation_euler = Euler((rx, ry, rz), 'XYZ')
    
def scale(obj):
    """
    Randomly scale a blender mesh object
    """
    if random.random() < prob_scale:
        scale = random.uniform(scale_min, scale_max)
        scl = [scale for _ in range(3)]
        obj.scale = scl

def transform(obj):
    """
    Transform a blender mesh object randomly by rotating, scaling and moving in that order
    """
    rotate(obj)
    scale(obj)
    select(obj)
    bpy.ops.object.transform_apply(rotation=True, scale=True)
    move(obj)
    select(obj)
    bpy.ops.object.transform_apply(location=True)