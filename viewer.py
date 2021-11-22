import os
import napari
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from skimage.measure import regionprops,label
from CellCounter import get_binary_map,apply_opening,find_median_cell_size,apply_watershed

# def str_to_bool(value):
#     if isinstance(value, bool):
#         return value
#     if value.lower() in {'false', 'f', '0', 'no', 'n'}:
#         return False
#     elif value.lower() in {'true', 't', '1', 'yes', 'y'}:
#         return True
#     raise ValueError(f'{value} is not a valid boolean value')

def get_args():
    parser = argparse.ArgumentParser(description='Automatic cell counter')
    parser.add_argument('--image', default=False)
    return parser.parse_args()

if __name__ == '__main__':
    args = get_args()
    
    if os.path.isdir(args.image):
        listOfFiles = list()
        for (dirpath, dirnames, filenames) in os.walk(args.image):
            filenames = [f for f in filenames if not f[0] == '.']
            dirnames[:] = [d for d in dirnames if not d[0] == '.']
            print(dirpath)
            filenames.sort()#key=lambda x: int(x.split(".")[0]))
            listOfFiles += [os.path.join(dirpath, file) for file in filenames]
    else:
        listOfFiles = [args.image]
    
    result = []
    # image process
    for image in listOfFiles:
        img = plt.imread(image)  

        binary_img = get_binary_map(img)
        final = label(apply_opening(binary_img))
        median_size = find_median_cell_size(final)
        cell_number = len(np.unique(final))-1
        # only apply watershed when the detected cell number is larger than 150
        if cell_number > 150: 
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
        print('Image name: ',image)
        print('Number of cells detected with automatic method: ', len(points))
        result.append([image,len(points)])

        #with napari.gui_qt():
        viewer = napari.view_image(img, name='image')
        if len(bboxes)>0:
            shapes_layer = viewer.add_shapes(bboxes,
                                    face_color='transparent',
                                    edge_color='magenta',
                                    name='bounding box',
                                    edge_width=5)
        if len(points)>0:
            points_layer = viewer.add_points(points,
                                    properties=point_properties,
                                    face_color='point_colors',
                                    size=20,
                                    name='points')

        @viewer.bind_key('d') # denote done
        def update_cell_numbers(viewer):
            num_cells = viewer.layers['points'].data.shape[0]
            print('Number of cells after manual correction: ', num_cells)
            result[-1].append(num_cells)
            viewer.close()
        
        napari.run()
    
        if len(result[-1]) == 2:
            result[-1].append(None)
            
    df = pd.DataFrame(result, columns =['Name', 'Automatic Cell Number','Corrected Cell Number']) 
    df.to_excel('result.xlsx')
    print('Done! All results are saved in result.xlsx!')
