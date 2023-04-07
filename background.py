import bpy
import random
from transformations import cam_box
from camera import adjust_resolution, cam_box
from data import background_max_y, background_min_y

plane = bpy.context.scene.objects['Plane']
def move_plane():
    plane.location = (0, random.randint(background_min_y, background_max_y), 0)

def adjust_background(img):
    img = bpy.data.images[img.name]
    adjust_resolution(img)
    width, height = cam_box(plane)    
    width  = width  * 2
    height = height * 2
    plane.dimensions = (width, 0, height)


def change_background(path):
    move_plane()
    image = bpy.data.images.load(path)
    bpy.data.materials['Background'].node_tree.nodes['Image Texture'].image = image
    adjust_background(image)
    return image