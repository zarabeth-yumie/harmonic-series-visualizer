find ./ -name '*.pyc' -delete
pip3 install -r requirements.txt
pip3 install bokeh
bokeh serve --port=3000 --address=0.0.0.0 --allow-websocket-origin=* --use-xheaders --disable-index taylor-webapp.py