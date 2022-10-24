#with help from:
#https://auth0.com/blog/image-processing-in-python-with-pillow/#:~:text=format%20this%20way.-,Resizing%20Images,Image%20with%20the%20new%20dimensions.


from PIL import Image
import os
from os import walk

from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True


DIM1 = 400
DIM2 = 600


starting_directory = "/Users/sairah/Desktop/resize/images"
target_directory = "/Users/sairah/Desktop/resize/images/small"

counter = 0


f = []
for (dirpath, dirnames, filenames) in walk(starting_directory):
    f.extend(filenames)
    break

#print(filenames)

for file in filenames:
    if file[-4:] == '.jpg':
        image = Image.open(file)
        image = image.convert('RGB')
        #print(image.size)
        new_image = image.resize((DIM1, DIM2)) #This could be changed to image.crop or image.thumbnail
        os.chdir(target_directory)

        new_image.save(file)
        counter = counter + 1
        print(counter)
        os.chdir(starting_directory)

print("done")