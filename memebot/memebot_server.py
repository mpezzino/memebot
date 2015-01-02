import cherrypy
from utils import jsonp
import pickle
from memebot_config import CLASSIFIER_FILE_PATH
import memebot_classifier


print "Loading classifier..."
classifier_file = open(CLASSIFIER_FILE_PATH,'rb')
classifier = pickle.load( classifier_file )
classifier_file.close()

class MemebotServer(object):
    @cherrypy.expose
    @jsonp
    def index(self,t):
        return memebot_classifier.karma_classify(classifier, t)

cherrypy.quickstart(MemebotServer())#,'/','memebot_server.conf')
