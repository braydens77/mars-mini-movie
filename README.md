# Mars Mini Movie
An interactive Python script to create short 3D movies and 3D gifs from stereoscopic images obtained by the Mars Curiosity Rover's front hazard avoidance cameras. 

![Solar day 2008 gif example](https://github.com/braydens77/mars-mini-movie/blob/master/MarsSol2008.gif?raw=true)

Images for all Mars solar days can be found on [NASA's Mars Science Laboratory website](https://mars.nasa.gov/msl/multimedia/raw/)

## Set Up
In order to get the script working, the following must be installed on your system:

* requests
* html5lib
* bs4
* Pillow
* matplotlib
* ffmpeg

`pip install requests html5lib bs4 Pillow matplotlib`

FFmpeg can be downloaded [here](https://www.ffmpeg.org/). Make sure to add the path to your ffmpeg executable file in your system path.

## Running
Once installed, you can run the script in the terminal:

`python mars_movie.py`

You will be prompted to enter the number for a Mars solar day. All solar days can be found [here](https://mars.nasa.gov/msl/multimedia/raw/). If you enter a number for a day that doesn't exist, you will be prompted to enter a different number.

After this, the movie will be made. You will also be prompted about whether to make an additional .gif format for the movie. Both files will be available the same directory that you are running `mars_movie.py`in.

### Acknowledgments
This script was inspired by the course [Python: Programming Efficiently](https://www.linkedin.com/learning/python-programming-efficiently/).
