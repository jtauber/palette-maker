#!/usr/bin/env python3

from PIL import Image
import numpy as np
from sklearn.cluster import KMeans


NUM_CLUSTERS = 10

print("""<!DOCTYPE html>
<html>
  <head>
    <title>Color Palette</title>
    <link rel="stylesheet" href="style.css">
  </head>
  <body>
    <h1>Colours of ROP Demo</h1>
    <p>using K-means clustering of pixels in colour space</p>""")


def hsv_to_hsl(h, s, v):
    h = h
    l = v * (1 - s / 2)
    s_hsl = 0 if (l == 0 or l == 1) else (v - l) / min(l, 1 - l)
    
    return h, s_hsl, l

for i in range(1, 13):

    FILENAME = f"images/img{i:02d}.png"

    img = Image.open(FILENAME).convert("HSV").resize((400, 400))
    img_data = np.array(img).reshape((-1, 3))

    kmeans = KMeans(n_clusters=NUM_CLUSTERS)
    kmeans.fit(img_data)

    palette = kmeans.cluster_centers_.astype(int)

    print(f"""    <div class="frame">""")
    print(f"""      <img src="{FILENAME}">""")
    print(f"""      <div class="palette">""")

    for color in sorted(palette, key = lambda x: x[0]):
        h = 360 * color[0] / 256
        s = 1 * color[1] / 256
        v = 1 * color[2] / 256

        H, S, L = hsv_to_hsl(h, s, v)

        H = int(H)
        S = int(100 * S)
        L = int(100 * L)

        print(f"""        <div class="swatch" style="background-color: hsl({H}, {S}%, {L}%);"></div>""")

    print("""      </div>
    </div>""")

print("""  </body>
</html>""")
