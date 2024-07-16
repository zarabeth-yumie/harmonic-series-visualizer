# taylor-webapp

The most fascinating topic I encountered in my calculus journey this year was the remarkable Taylor Series. The concept of approximating complex functions with simpler polynomials left me in awe, although comprehending it was no easy feat. Driven by making this topic more accessible, I created a web application that provides a visualization for the Taylor Polynomial. I used Bokeh, an interactive visualization library in Python, and hosted the page using Glitch.

Feature List:
- Graphs any function and computes its nth-degree Taylor polynomials.
- The program is able to show the error between the approx. and function
- The program is able to show the radius of convergence for functions ln/log(x+1) and 1/(1-x) (I tried making it able to compute the ROC for any function, but it was really hard since doing the Ratio Test in python is kind of hard)
- The user can change the center value to any value (this is the traditional "a" value).

If anyone has any suggestions/issues, please DM me. I'm really interested in making this as helpful as possible! Also, this tech stack is super simple for anyone familiar with Python so feel free to branch off my code and try something out!

LinkedIn: https://www.linkedin.com/in/naren-manikandan/

### Made using Bokeh, Python, and Glitch (for hosting and free)!

## Developer Notes
### start.sh
```
find ./ -name '*.pyc' -delete
pip3 install -r requirements.txt
pip3 install bokeh
bokeh serve --port=3000 --address=0.0.0.0 --allow-websocket-origin=* --use-xheaders --disable-index taylor-webapp.py
```
In the run script, I had too use `--disable-index` to prevent Glitch from running Bokeh in the background (if it were two, Glitch won't actually open the website). Using this in the command forces Bokeh to run in the foreground instead. 
