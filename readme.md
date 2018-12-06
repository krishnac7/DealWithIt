Packages required:

`pip3 install moviepy dlib pillow imutils numpy`

Download Shape predictor file at : 
http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2

Arguments : -image <path_to_image>

Fixing ffmpeg installation on macos for MoviePy:
 * manually download the built (this is where the SSL error occurs): https://github.com/imageio/imageio-binaries/raw/master/ffmpeg/ffmpeg-osx-v3.2.4

* paste the file to the path: /Users/yourusername/Library/Application\ Support/imageio/ffmpeg/

* re-run your code


Sample Output:<br/>

![](deal.gif)