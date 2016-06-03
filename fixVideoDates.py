#!/usr/bin/python3
import os
import datetime
import logging


def main():
    """ Fix up video file dates in folder
    """
    src_dir = '/media/MEDIA1/VideosToProcess'
    cleanse_filenames(src_dir)
    fix_movie_metadata(src_dir)


def fix_movie_metadata(src_dir):
    """ Loop through movie files and fix up metadata
    """
    filePath = os.path.abspath(src_dir)
    os.chdir(filePath)
    for i, file in enumerate(os.listdir(filePath)):
        oldfName, fExt = os.path.splitext(file)
        # Check the file is a relevant file type
        if fExt in ['.mp4','.MOV','.AVI','.mts']:
            fileDate = get_date_from_filename(oldfName)
            if fileDate != None:
                fullFilePath = src_dir+'/'+file
                fix_metadata(fullFilePath, fileDate)


def fix_metadata(fPath, createDate):
    """ If no metadata exists, specifically for mp4
        Then use the filename to set the creation date
        using exiftool, for example:
        exiftool -v2 -quicktime:createdate="2010:03:07 11:08:19" input.mp4
    """
    ds = datetime.datetime.strftime(createDate, "%Y:%m:%d %H:%M:%S")
    output = 'exiftool -v2 -quicktime:createdate="'+ds+'" '+fPath
    os.system(output)


def cleanse_filenames(src_dir):
    """ Remove unneeded words from filename
        This will hopefully make it a date
        Then convert that date to ISO format
        Then rename the file
    """
    filePath = os.path.abspath(src_dir)
    os.chdir(filePath)
    for file in os.listdir(filePath):
        oldfName, fExt = os.path.splitext(file)
        # Check the file is a relevant file type
        if fExt in ['.mp4','.MOV','.AVI']:
            newfName = clean_filename(oldfName)
            #dateString = newfName[0:8]
            #newfName = convert_datestring_to_iso(dateString,"%d%m%Y")[0:8]
            #newfName = newfName + '_' + oldfName[9:]
            rename_file(src_dir, oldfName, newfName, fExt, False)

def get_date_from_filename(fName):
    """ See if we can extract a date from the filename
        Will have to try a few different date formats
    """

    fileDate = fName
    try:
        fileDate = datetime.datetime.strptime(fName,'%Y%m%d_%H%M%S')
    except ValueError:
        try:
            testString = fName[0:14]
            fileDate = datetime.datetime.strptime(testString,'%Y%m%d_%H%M%S')
        except ValueError:
            try:
                fileDate = datetime.datetime.strptime(testString,'%Y%m%d%H%M%S')
            except ValueError:
                try:
                    testString = fName[0:8]
                    fileDate = datetime.datetime.strptime(testString,'%Y%m%d')
                except ValueError:
                    fileDate = None
    
    return fileDate


def clean_filename(fileName):
    """ Remove unwanted text from the filename
        This is to hopefully get it down to just a date
    """
    newFileName = fileName
    unwantedText = ['VID_','VID','IMG_','.mts']
    for searchField in unwantedText:
        newFileName = newFileName.replace(searchField,'')
    newFileName = newFileName.replace(' ','_')
    newFileName = newFileName.replace('-','')
    newFileName = newFileName.replace('.','')
    newFileName = newFileName.strip()

    return newFileName

def convert_datestring_to_iso(dString,dFormat):
    """ Convert date string to ISO format
    """
    dt = datetime.datetime.strptime(dString, dFormat)
    ds = datetime.datetime.strftime(dt, "%Y%m%d_%H%M%S")

    return ds

def rename_file(fPath, oldfName, newfName, fExt, tryRename=False, append=0):
    """ Renames file, checking to make sure it does not already exist
        Adds a incrementing number if it does exist
    """
    if oldfName == newfName:
        return newfName
    if append == 0:
        pass
    else:
        newfName = newfName + '_' + str(append)

    oldPath = os.path.join(fPath, oldfName+fExt)
    newPath = os.path.join(fPath, newfName+fExt)
    if os.path.isfile(newPath):
         if tryRename:
             rename_file(fPath, oldfName, newfName, fExt, append+1)       
    else:
        os.rename(oldPath, newPath)
        logging.info('Renamed '+str(oldPath),' to '+str(newPath))
    return newPath

            
if __name__ == '__main__':
    main()
