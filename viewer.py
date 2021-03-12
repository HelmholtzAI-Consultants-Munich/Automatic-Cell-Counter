import napari
import argparse
import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import regionprops,label
from CellCounter import get_binary_map,apply_opening,find_median_cell_size,apply_watershed

def str_to_bool(value):
    if isinstance(value, bool):
        return value
    if value.lower() in {'false', 'f', '0', 'no', 'n'}:
        return False
    elif value.lower() in {'true', 't', '1', 'yes', 'y'}:
        return True
    raise ValueError(f'{value} is not a valid boolean value')

def get_args():
    parser = argparse.ArgumentParser(description='Automatic cell counter')
    parser.add_argument('--image', default=False)
    parser.add_argument('--dense', type=str_to_bool,default=True)
    return parser.parse_args()

if __name__ == '__main__':
    args = get_args()
    
    # image process
    img = plt.imread(args.image)  
    
    binary_img = get_binary_map(img)
    final = label(apply_opening(binary_img))
    median_size = find_median_cell_size(final)
    if args.dense==True:
        final = apply_watershed(final,median_size) 
    
    # viewer
    points = [] 
    colors = []
    bboxes = []
    i=0
    for region in regionprops(final):
        y,x = region.centroid
        if region.area >= 2*median_size:       
            #bound
            minr, minc, maxr, maxc = region.bbox
            bbox_rect = np.array([[minr, minc], [maxr, minc], [maxr, maxc], [minr, maxc]])
            colors.append('green') #0.1)
            bboxes.append(bbox_rect)
        
        elif region.area < median_size/2:
            colors.append('red')
        else:
            colors.append('green')

        points.append([y,x])

    points=np.array(points)
    point_properties={
        'point_colors': np.array(colors)
    }
    bboxes = np.array(bboxes)
    print('Number of cells detected with automatic method: ', len(points))

    with napari.gui_qt():
        viewer = napari.view_image(img, name='image')
        shapes_layer = viewer.add_shapes(bboxes,
                                face_color='transparent',
                                edge_color='magenta',
                                name='bounding box',
                                edge_width=5) # properties=properties, text=text_parameters,
        points_layer = viewer.add_points(points,
                                properties=point_properties,
                                face_color='point_colors',
                                size=20,
                                name='points') # face_colormap='plasma', can add good point anf confidence 

        @viewer.bind_key('c')
        def print_names(viewer):
            num_cells = viewer.layers['points'].data.shape[0]
            print('Number of cells after manual correction: ', num_cells)