##################################
# Program formatujący dane: z formatu Data Extractor do formatu przyjmowanego przez PyTorch
# Sposób użycia: umieść program w tym samym folderze co dane z Extractor i uruchom
##################################

import os
import shutil


iter = 1

for dirname in os.listdir():
    if os.path.isdir(dirname):

        print("Formatting: " + dirname)

        for imgfolder in os.listdir(dirname):
            joined_path = os.path.join(dirname, imgfolder)

            if os.path.isdir(joined_path) and joined_path.endswith("imageframes"):
                shutil.move(joined_path, f"{iter:04d}")
                shutil.rmtree(dirname)
                iter += 1