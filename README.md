# Hyperbolic Poincare Disk Geometry
A simple graphing utility for creating geodesic segments in the Poincare Disk Model.

## Overview
This was a project I worked on for my Non-Euclidean Geometry class at the University of Missouri. The project was simply to draw Einstein in this particular model of Hyperbolic Geometry, so I wrote some python to give me a canvas to do so. It's fun to play with and can further one's understanding of geodesics in this geometric model. 

## Use
If you want to download and play with this, you'll just need to clone the repo and do the following in the directory:

    $ pip install matplotlib
    
or if you dont have pip and all that, here's a link to matplotlib's installation page: https://matplotlib.org/faq/installing_faq.html

## Tools used 
scikit-image (http://scikit-image.org/): I used their canny edge detection to outline Einstein's Face so I could actually draw him.

matplotlib (https://matplotlib.org/): This is the backbone of the actual graphing itself.


## Works Created

Example of drawing where all base circles are left on
---------------
<img src="https://github.com/trevorBajkowski/hyperbolicPoincareDiskGeometry/blob/master/pictures/hyperStein.png" width="200">


Example of drawing where all base circles are NOT left on
---------------
<img src="https://github.com/trevorBajkowski/hyperbolicPoincareDiskGeometry/blob/master/pictures/circleStein.png" width="200">


Quick snippet of drawing process!
---------------
<img src="https://github.com/trevorBajkowski/hyperbolicPoincareDiskGeometry/blob/master/pictures/drawnstein.gif" width="200">
