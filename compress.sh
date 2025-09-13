for ((i=2;i<84;i+=1))
do 
	ffmpeg -i video/video$i.MOV -c:v libx264 -crf 28 -preset veryslow -c:a aac -b:a 128k video_new/video$i.MOV
done
