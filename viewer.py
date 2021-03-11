import napari
import argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
# %matplotlib qt 
from scipy import ndimage as ndi
from skimage.filters import threshold_li
from skimage.measure import label, regionprops
from skimage.color import label2rgb
from skimage.morphology import disk, opening, remove_small_objects
from skimage.segmentation import watershed
from skimage.feature import peak_local_max

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
    dense = args.dense

    img = plt.imread(args.image)  #clear: Boyden Chamber/CD345_LN229_Ctrl/8.tif
    r = img[:,:,0].astype(np.int32)
    g = img[:,:,1].astype(np.int32)
    b = img[:,:,2].astype(np.int32)
    print('Image size: ', b.shape)
    
    # subtract b from g channel
    sub_rgb = (g-b)/(r+g+b)
    thresh = threshold_li(sub_rgb)
    binary_rgb = sub_rgb < thresh
    
    # opening
    selem = disk(7)
    eroded = opening(binary_rgb,selem)
    eroded = remove_small_objects(eroded.astype(bool), 1000).astype(np.int64)
    #plt.imshow(eroded)

    #plot
    final = label(eroded)
    area = []
    for region in regionprops(final):
        area.append(region.area)
    mid = np.median(np.array(area))
    
    # only use watershed algorithm when the input image is not quite dense
    if dense==True:
        print('Use watershed algorithm for dense images')
        distance = ndi.distance_transform_edt(eroded)
        local_max_coords = peak_local_max(distance, min_distance=40,exclude_border=0)
        local_max_mask = np.zeros(distance.shape, dtype=bool)
        local_max_mask[tuple(local_max_coords.T)] = True
        markers = label(local_max_mask)
        labels = watershed(-distance, markers, mask=eroded,watershed_line=True)

        #only do watershed on large size cells
        large = remove_small_objects(eroded.astype(bool), 2*mid).astype(np.int64)
        final[large>0] = labels[large>0]
        final = remove_small_objects(label(final), 1000).astype(np.int64)


    points = [] 
    colors = []
    bboxes = []
    i=0
    for region in regionprops(final):
        y,x = region.centroid
        if region.area >= 2*mid:       
            #bound
            minr, minc, maxr, maxc = region.bbox
            bbox_rect = np.array([[minr, minc], [maxr, minc], [maxr, maxc], [minr, maxc]])
            colors.append('green') #0.1)
            bboxes.append(bbox_rect)
        
        elif region.area < mid/2:
            colors.append('red') #0.5)
        else:
            colors.append('green') #0.1)

        points.append([y,x]) #or [x,y]?

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