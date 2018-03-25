from flask import Flask, url_for, request
from logging.config import thread
import entity_extractor
import json
import logging

application = Flask(__name__)


# to check service is up..
# url: get request => http://ip:port/

# url: post request => http://ip:port/
# include text content as raw data in the request body
# or url: get request => http://ip:port/?concept='text content'
@application.route('/', methods=['GET', 'POST'])
def index():
    try:
        if request.method == 'POST':
            return entity_extractor.get_names(request.get_data(as_text=True))
        else:
            if request.args.get('concept') is None:
                return json.dumps({"status": "ok"})
            else:
                return entity_extractor.get_names(request.args['concept'])

    except Exception as e:
        logging.error("error: " + str(e))


if __name__ == '__main__':
    application.run(threaded=True)
