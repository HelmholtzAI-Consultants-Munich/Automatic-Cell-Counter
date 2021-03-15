import numpy as np
from scipy import ndimage as ndi
from skimage.filters import threshold_li
from skimage.measure import label, regionprops
from skimage.color import label2rgb
from skimage.morphology import disk, opening, remove_small_objects
from skimage.segmentation import watershed
from skimage.feature import peak_local_max

def get_binary_map(img):
    '''
    This function returns the binary map of crystal violet cells from the input RGB images.
    
    Input
    ----------
        img: ndarray
            input image with RGB three channels
    
    Returns
    -------
        binary_map: ndarray
            output binary map, where foreground denotes detected violet cells
    '''
    r = img[:,:,0].astype(np.int32)
    g = img[:,:,1].astype(np.int32)
    b = img[:,:,2].astype(np.int32)
    
    # subtract b from g channel
    sub_rgb = (g-b)/(r+g+b)
    thresh = threshold_li(sub_rgb)
    binary_map = sub_rgb < thresh
    
    return binary_map
    
    
    
def apply_opening(binary_img,selem_parameter=7,remove_objects=1000):
    '''
    This function applies opening algorithm to the input binary map and remove small objects afterwards. Opening can remove small bright spots (i.e. “salt”) and connect small dark cracks. This tends to “open” up (dark) gaps between (bright) features.
    
    Input
    ----------
        binary_img: ndarray
            input binary image, where foreground denotes detected violet cells
        selem_parameter: int, default 7
            parameter affects the neighborhood structure in opening algorithm
        remove_objects: int, default 1000
            the smallest allowable object size.
    
    Returns
    -------
        opened_image: ndarray
            the binary image after opening algorithm and removing small objects
    
    '''
    selem = disk(selem_parameter)
    opened_image = opening(binary_img,selem)
    opened_image = remove_small_objects(opened_image.astype(bool), remove_objects).astype(np.int64)
    
    return opened_image

def find_median_cell_size(labeled_img):
    '''
    The function calculates the median region size given a instance labeled image.
    
    Input
    ----------
        labeled_img: ndarray
            input labeled image, where different values denote different region 
    
    Returns
    -------
        mid: float
            the median region size
    '''
    area = []
    for region in regionprops(labeled_img):
        area.append(region.area)
    median = np.median(np.array(area))
    return median
    
def apply_watershed(labeled_img,median_size,min_distance=40,remove_objects=1000):
    '''
    This function applies watershed algorithm on large-size regions (> 2*median size) to separate possible merged cells. 
    
    Input
    ----------
        labeled_img: ndarray
            input labeled image, where different values denote different regions
        median_size: float
            the median region size
        min_distance: int, default 40
            parameter in watershed algorithm, the minimal allowed distance separating peaks
        remove_objects: int, default 1000
            the smallest allowable object size.
            
    Returns
    -------
        final: ndarray
            the labeled image after watershed algorithm and removing small objects, where different values denote different detected cells
    '''
    # watershed algorithm
    distance = ndi.distance_transform_edt(labeled_img)
    local_max_coords = peak_local_max(distance, min_distance=min_distance,exclude_border=0)
    local_max_mask = np.zeros(distance.shape, dtype=bool)
    local_max_mask[tuple(local_max_coords.T)] = True
    markers = label(local_max_mask)
    labels = watershed(-distance, markers, mask=labeled_img,watershed_line=True)

    # only apply watershed on large size cells
    large_cells = remove_small_objects(labeled_img.astype(bool), 2*median_size).astype(np.int64)
    final = labeled_img
    final[large_cells>0] = labels[large_cells>0]
    final = remove_small_objects(label(final), remove_objects).astype(np.int64)

    return final
        
        
        
    
    