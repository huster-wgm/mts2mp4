# MTS to MP4

The video files from my camera are saved as MTS files. MTS is a file extension for an AVCHD (Advanced Video Coding High Definition) video clip format for high-definition video. 

There isn't much support for it in video editting software, so this script converts them to MP4. This doesn't bring across the date metadata properly, so run a python script to fix it up.


To convert all MTS files in the folder to MP4:

```
./convertMTStoMP4.sh
```

To fix the date metadata:

```
python3 fixVideoDates.py
```


