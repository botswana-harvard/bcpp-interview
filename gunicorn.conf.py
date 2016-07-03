# http://cheng.logdown.com/posts/2015/01/29/deploy-django-nginx-gunicorn-on-mac-osx-part-2
# cd /Users/erikvw/source/bcpp-interview/
# gunicorn -c gunicorn.conf.py bcpp_interview.wsgi --pid /Users/erikvw/source/bcpp-interview/logs/gunicorn.pid --daemon
#

bind = "127.0.0.1:9000"  # Don't use port 80 becaue nginx occupied it already. 
errorlog = '/Users/erikvw/source/bcpp-interview/logs/gunicorn-error.log'  # Make sure you have the log folder create
accesslog = '/Users/erikvw/source/bcpp-interview/logs/gunicorn-access.log'
loglevel = 'debug'
workers = 1  # the number of recommended workers is '2 * number of CPUs + 1'
