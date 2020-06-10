from flask import Flask, render_template, json, request
import numpy as np
import os
import time
import matplotlib
import json
import random

matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.ioff()

from threading import Lock
lock = Lock()
import datetime
import mpld3
from mpld3 import plugins
s = json.load(open("./static/bmh_matplotlibrc.json"))


def plot(h) :
      
      labels = 'work', ''
      sizes = [8, 8-h]
      colors = ['yellowgreen', 'gold']
      explode = (0, 0)
      
      plt.pie(sizes, explode=explode, labels=labels, colors=colors, 
              autopct='%1.1f%%', shadow=True, startangle=90)
      
      plt.axis('equal')
      plotfile = os.path.join('static', str(time.time()) + '.png')
      plt.savefig(plotfile)
      return plotfile
if __name__ == '__main__':
    plot(8)
    

      