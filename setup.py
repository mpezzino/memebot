
from setuptools import setup

setup(name='memebot',
      version='0.1',
      description='memebot',
      url='https://github.com/softwareengineerprogrammer/memebot',
      author='Breaux Gramm',
      author_email='breaux@breauxgramm.in',
      license='MIT',
      packages=['memebot'],
      install_requires=[
          'praw',
          'simplejson',
          'cherrypy'
      ],
      zip_safe=False)

print "Setup complete, now run\npython memebot_config.py"


