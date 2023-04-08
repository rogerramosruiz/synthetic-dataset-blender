# name of the collection to start
collection_start  = 'bag'
# name of the collection to end
collection_end    = 'straw'
# Number of images to generate per class or collection
# E.G if  there are three collections A, B, C and images_per_class=10 
# then there will be at least 10 images with collection A, 10 with B, and 10 with C
# in total there will be 30 images

images_per_class = 1
# name length of the files
file_name_size     = 10
# Location to save the dataset, must be full path
save_dir          = 'D:/dataset_shyntethic'
# Location of the images
img_dir           = 'D:/generadores/synthtetic_dataset/images/background'

# Probability of having more than one object per background image
# if the value is 0 then there will just one object per background image
# if the values is 1 then there will more than one obejct per background image

prob_many_objs   = 0.3

# Probabylity of one object image to be added
# When one more than object will be added per background image 
# prob_add_obj is the probabily of adding a type or class of an object
# e.g there are three classes of objects A,B,C and the values is 0.5
# there is a 50% of adding an object A, 50% of adding an object of B
# and 50% of adding an object of C

prob_add_obj     = 0.5

# transformations
# probabily of scaling a mesh
prob_scale       = 0.7
# minimum and maximum value to scale
scale_min        = 1
scale_max        = 1.5

# probabily of rotating a mesh
prob_roate       = 0.55
# rotation (x, y, z) between -360 and 360
# minimum and maximum rotationn value 
min_rot           = [-80, 0, 0]
max_rot           = [80, 360, 360]

# background
# Background location minimun and maximun in cooraenate Y  
background_min_y = 0
background_max_y = 6

# Object mesh aditional data
# format
"""
obj_data = {
   collection_name: {
        material_name: probability of changeing color,
        material_name 2: probability of changeing color,
        
        # Optional value 
        # Colors to use for this sepecific collection
        colors: [[R,G,B], [R,G,B], [R,G,B]]
 }
}

"""
 
obj_data = {
    'bag': {
        'garbagebags': 0.1,
        'transparent bag': 0.7
    },
    'bottle': {
        'Plastic_transparent': 0.3,
        'lid': 1,
        'label': 1,
        'inner label': 0,
        'no_label_prob': 0.1
    },
    'container': {
        'Plastic_transparent': 0.005,
    },
    'cup': {
        'Plastic_transparent': 0.005
    },
    'gloves': {
        'gloves': 0.8,
        # Color for gloves
        'colors' : [[0.238398, 0.341915, 0.904661], [0.208637, 0.558341, 0.930111], [0.027321, 0.114435, 0.327778], [0.871367, 0.83077, 0.708376]]
    },
    'spoon': {
        'spoon': 0.5,
    },
    'straw': {
        'straw': 1,
    }
}
