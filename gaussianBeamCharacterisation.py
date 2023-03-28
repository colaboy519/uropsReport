#%%
import matplotlib.pyplot as plt
import numpy as np
import glob
from PIL import Image
# Read me: 
# 1. naming the .pgm documents: 
    # background: 1.pgm -> so that background reading is first in the file 
    # others: z-position+unit.pgm -> eg: 15cm.pgm for reading at 15cm on z-axis
    # this is such that glob.glob works properly 
# 2. the following lines of code are instrument specific: -> do change parameters accordingly 
    # CCD camera: hBeamDiameter = (rBound - lBound)*3.75*10**(-6) (in microns)
    
###############################################################################################
# helper functions:

# Read the pgm file into a nparray; input .pgm file path, output the .pgm image as nparray
def read_pgmf(filePath):
    return plt.imread(open(filePath,'rb'))

# image nparray -> horizontal beam radius in mm
def getHorizontalBeamRadius(image_array, image_array_bg):
    column_image = image_array.sum(axis=0) # this sums up all rows of camData
    column_image_bg = image_array_bg.sum(axis=0) # this sums up all rows of background camData
    column_image_wtbg = column_image - column_image_bg # subtract background reading from camData
    column_image_normalised = [] #normalise
    for i in range(len(column_image_wtbg)):
        column_image_normalised.append(column_image_wtbg[i] / column_image_wtbg.max())
    threshold = 1/(np.e**2)
    aboveThreshold = []
    for i in range(len(column_image)):
        if column_image[i] >= threshold:
            aboveThreshold.append(i)
    aboveThreshold = np.array(aboveThreshold)

    #this givs a list of the elements in column_image above threshold)
    lBound = aboveThreshold.min()
    rBound = aboveThreshold.max()
    pixelSize = 3.75*10**(-6) #meter
    hBeamRadius = (rBound - lBound)*pixelSize/2
    #debug: 
    print("beam left bound is: "+ str(lBound))
    print("beam right bound is: "+ str(rBound))
    print('Horizontal beam radius',':', hBeamRadius*10**(3), 'mm')
    plt.plot(column_image_normalised)
    
    return hBeamRadius
    
def getVerticalBeamRadius(image_array, image_array_bg):
    row_image = image_array.sum(axis=1) # this sums up all columns in camData
    row_image_bg = image_array_bg.sum(axis=1) # this sums up all columns in backgroung
    row_image_wtbg = row_image - row_image_bg
    row_image_normalised = [] #normalise
    for i in range(len(row_image_wtbg)):
        row_image_normalised.append(row_image_wtbg[i] / row_image_wtbg.max())
    threshold = 1/(np.e**2)
    aboveThreshold = []
    for i in range(len(row_image)):
        if row_image[i] >= threshold:
            aboveThreshold.append(i)
    aboveThreshold = np.array(aboveThreshold)

    bBound = aboveThreshold.min()
    tBound = aboveThreshold.max()
    pixelSize = 3.75*10**(-6) #meter
    vBeamRadius = (tBound - bBound)*pixelSize/2
    #debug: 
    print("beam top bound is: "+ str(tBound))
    print("beam bottom bound is: "+ str(bBound))
    print('Vertical beam radius',':', vBeamRadius*10**(3), 'mm')
    plt.plot(row_image_normalised)
    
    return vBeamRadius


###############################################################################################
# the main code:

# Directory where .pgm files are stored
# directory = input("input data file directory")
# directory = "/Volumes/dzmitrylab/zhonglin/10MarCamera"
directory = "/Volumes/dzmitrylab/zhonglin/10MarCamera2"
pixelSize = 3.75*10**(-6) #meter

# Find all .pgm files in the directory
pgm_files = glob.glob(directory + '/*.pgm')
pgm_files.sort(key = lambda s: len(s))

# read background first, then delele background from the list of files 
image_array_bg = read_pgmf(pgm_files[0])
print("-> background array: ")
print(image_array_bg)
print("CCD has number of rows: " + str(len(image_array_bg)))
print("CCD has horizonal length: " + str(len(image_array_bg)*pixelSize))
print("CCD has number of columns " + str(len(image_array_bg[0])))
print("CCD has vertical length: " + str(len(image_array_bg[0])*pixelSize))
pgm_files=pgm_files[1:]

print("-> Finished reading files, here are all the files: ")
print(pgm_files)
print("-> Now import files: ")
# Define empty lists to hold the image arrays and z positions
image_arrays = [] # contain nparray
z_positions = []  # contain integer
# Read all .pgm files and process them one by one
for file_path in pgm_files:
    # Load the .pgm file using the Pillow library
    pgm_image = Image.open(file_path)

    # Convert the image to a numpy array and append it to the list
    image_array = np.array(pgm_image)
    image_arrays.append(image_array)
    
    zPosition = int(file_path[-8]+file_path[-7])
    z_positions.append(zPosition)

    # Close the image file to free up resources
    pgm_image.close()

print("-> Finished importing files, here are all the image data: ")
for image_array in image_arrays: 
    print(image_array)
print("-> now start processing image data: ")

horizontal_radius = [] 
vertical_radius = [] 
for i in range(len(image_arrays)):
    z_position = z_positions[i]
    print("data from " + str(z_position) +"cm :")
    # process each image_array to get horizontal and vertical beam radius
    hBeamRadius = getHorizontalBeamRadius(image_arrays[i], image_array_bg)
    horizontal_radius.append(hBeamRadius)
    vBeamRadius = getVerticalBeamRadius(image_arrays[i], image_array_bg)
    vertical_radius.append(vBeamRadius)
    print("-> image minused bg " + str(i) + " :")
    print(image_array)
print("-> Finished image processing, now plot graphs: ")

# Now plot the w(z) graph for horizontal and vertical directions
plt.plot(z_positions,horizontal_radius, 'o', label='horizontal radius(mm) - z(cm)')
plt.plot(z_positions,vertical_radius, 'o', label='vertical radius(mm) - z(cm)')
plt.legend()
plt.xlabel('detector position (cm)')
plt.ylabel('beam radius (mm)')


plt.show
print('-> all done')

#%%


