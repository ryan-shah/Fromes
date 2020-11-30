# Fromes
This project was inspired by the [Fromes](https://www.frome.co/) website/service.

However, since I didn't want to pay $200+ on their prints, I figured I'd see if I could do it myself and print the resulting image for much cheaper.

## From their website
- [How it works](https://www.frome.co/pages/how-it-works)

The canvases you see are movies condensed into chronological color strips that represent each frame - 
meaning the colors you see can roughly represent the main color of that scene. 
The movie begins with a single color strip at the start of canvas (left) and ends with the last 
strip (right). You can see how beautiful movies are in terms of colors!


## How this works
1. Use ffmpeg to split a video into it's frames
2. Using the sklearn python library to determine the most common color in each image.
3. Using numpy to gather said images and display them in order

### Packages necessary
- ffmpeg
- python2.7
	- opencv-python: `pip install opencv-python==4.2.0.32`
	- scikit-learn: `pip install scikit-learn`
	- watchdog: `pip install watchdog`
## Examples
- [glip_glops.mp4](example-videos/glip_glops.mp4): `./frome.py -i example-videos/glip_glops.mp4 -d tmp -o example-images/glip_glops.png -q 8000 -t 10`
![](example-images/glip_glops.png)

- [glip_glops.mp4 - 1 fps](example-videos/glip_glops.mp4): `./frome.py -i example-videos/glip_glops.mp4 -d tmp -o example-images/glip_glops_1fps.png -q 8000 -t 10 -r 1`
![](example-images/glip_glops_1fps.png)

- [Man or Muppet music video](https://www.youtube.com/watch?v=cRTjksM3YAs)
![](example-images/muppet.png)

- [Monty Python & the Holy Grail - 1fps](https://www.youtube.com/watch?v=PxagJ8fpsv8)
![](example-images/holy_grail_1fps.png)
