#
# To be run in OMERO CLI shell as follows:
#
#     # Download script to current working directory
#     omero shell --login
#     ...
#     %run -i rename-plate-images.py plate_id name
#
import sys

from omero.gateway import omero_type

try:
    plate_id, name = sys.argv[1:]
except ValueError:
    print "Usage: %s <plate_id> <name>"
    sys.exit(1)
plate_id = long(plate_id)

session = client.getSession()
iquery = session.getQueryService()
iupdate = session.getUpdateService()

params = omero.sys.Parameters()
params.map = {"pid": omero_type(plate_id)}

query = """select image from Image image
join image.wellSamples as samples
join samples.well as well
join well.plate as plate
where plate.id=:pid"""

images = iquery.findAllByQuery(query, params)

for image in images:
    image.setName(omero_type(name))
    iupdate.saveObject(image)

print 'Successfully set name of %d images in Plate:%d to %r' % (
    len(images), plate_id, name)
