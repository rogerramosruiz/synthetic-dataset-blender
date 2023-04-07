import bpy
import random
from math import atan, tan
import bpy_extras

from utils import convert_yolo, distance

cam =  bpy.data.objects['Camera']

def get_angles(camera):
    scene = scene = bpy.context.scene    
    frame = camera.data.view_frame(scene = scene)
    x = abs(frame[0][0])
    y = abs(frame[0][1])
    z = abs(frame[0][2])
    angleX = atan(x/z)
    angleY = atan(y/z)
    return angleX, angleY

def cam_box(obj):
    angleX, angleY = get_angles(cam)
    distanceY = distance(obj, cam)[1]
    width  = tan(angleX) * distanceY
    height = tan(angleY) * distanceY
    return width, height

def adjust_resolution(img):
    width, height = img.size
    bpy.context.scene.render.resolution_x = width
    bpy.context.scene.render.resolution_y = height
    bpy.context.scene.render.resolution_percentage = random.randint(30, 60) if width > 3000 or height > 3000 else 100

def change_focal_length(val= None):
    if val:
        cam.data.lens = val
    else:
        cam.data.lens = random.randint(20,65)

def bounding_box(obj, yoloFormat = False):
    scene = bpy.context.scene
    render_scale = scene.render.resolution_percentage / 100
    width  = int(scene.render.resolution_x * render_scale)
    height = int(scene.render.resolution_y * render_scale)
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
        return convert_yolo(p1[0], p1[1], p2[0], p2[1], (height, width))
    return p1, p2