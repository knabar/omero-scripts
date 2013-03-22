#
# To be run in OMERO CLI shell as follows:
#
#     # Download script to current working directory
#     omero shell --login
#     ...
#     %run -i rename-image.py image_id name
#
import sys

from omero.gateway import omero_type

try:
    image_id, name = sys.argv[1:]
except ValueError:
    print "Usage: %s <image_id> <name>"
    sys.exit(1)
image_id = long(image_id)

session = client.getSession()
iquery = session.getQueryService()
iupdate = session.getUpdateService()

image = iquery.find('Image', image_id)
image.setName(omero_type(name))
iupdate.saveObject(image)
print 'Successfully set name of Image:%d to %r' % (image_id, name)
