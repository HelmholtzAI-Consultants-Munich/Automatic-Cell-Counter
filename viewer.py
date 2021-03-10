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

def get_args():
    parser = argparse.ArgumentParser(description='Bone Cement Planning Pipeline')
    parser.add_argument('--image', default=False)
    parser.add_argument('--save', default=False)
    return parser.parse_args()

if __name__ == '__main__':
    args = get_args()

    img = plt.imread(args.image)  #clear: Boyden Chamber/CD345_LN229_Ctrl/8.tif
    r = img[:,:,0].astype(np.int32)
    g = img[:,:,1].astype(np.int32)
    b = img[:,:,2].astype(np.int32)
    print('Image size: ', b.shape)
    
    # subtract b from g channel
    sub_rgb = (g-b)/(r+g+b)
    # sub_rgb = (sub_rgb-np.min(sub_rgb))/(np.max(sub_rgb)-np.min(sub_rgb))
    thresh = threshold_li(sub_rgb)
    # print(thresh)
    binary_rgb = sub_rgb < thresh
    binary_rgb = remove_small_objects(binary_rgb, 1000).astype(np.int64)
    
    # opening
    selem = disk(7)
    eroded = opening(binary_rgb,selem)
    eroded = remove_small_objects(eroded.astype(bool), 1000).astype(np.int64)
    #plt.imshow(eroded)

    #plot
    labels = label(eroded)
    area = []
    for region in regionprops(labels):
        area.append(region.area)
    mid = np.median(np.array(area))


    points = [] 
    colors = []
    bboxes = []
    i=0
    for region in regionprops(labels):
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
    print('Automatic number of cells detected with automatic method: ',len(points) )
    with napari.gui_qt():

        viewer = napari.view_image(img, name='image')
        points_layer = viewer.add_points(points,
                                properties=point_properties,
                                face_color='point_colors',
                                size=20,
                                name='points') # face_colormap='plasma', can add good point anf confidence 
        shapes_layer = viewer.add_shapes(bboxes,
                                        face_color='transparent',
                                        edge_color='magenta',
                                        name='bounding box',
                                        edge_width=5)
        
        # properties=properties, text=text_parameters,
        print('Number of cells after manual correction: ',len(points))