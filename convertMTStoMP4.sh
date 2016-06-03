for f in *.mts
do 
    avconv -i $f -qscale 1 -strict experimental $f.mp4 
done
