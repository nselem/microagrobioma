import pandas as pd
import os

def GetFilesForDownload(path):
    fileList = os.listdir(path)
    fileListSizes = [ (filePath, os.stat(os.path.join(path, filePath)).st_size/1000000) for filePath in fileList ]
    df = pd.DataFrame(fileListSizes,columns=['File Name','Size (MB)']).round({'Size':2})
    return df
