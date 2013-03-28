import os
import sys
import time
import omero
from omero.gateway import BlitzGateway


count = long(sys.argv[1]) if len(sys.argv) > 1 else 10
timeout = 30

conn = BlitzGateway('root', 'omero')
conn.connect()

def get_repository(klass, name=None):
    klass = '%sPrx' % klass
    klass = getattr(omero.grid, klass)
    sr = conn.getSharedResources()
    repositories = sr.repositories()
    for index, proxy in enumerate(repositories.proxies):
        repository = klass.checkedCast(proxy)
        if repository is not None:
            description = repositories.descriptions[index]
            if name is None or name == description.name.val:
                return (repository, description)
    raise AttributeError(
        'Repository of type %s with optional name %s unavailable' %
        (klass, name))


def getDirectory(dirpath):
    user = conn.getUser()
    return os.path.join('%s_%s' % (user.getName(), user.getId()), dirpath)


repository, description = get_repository('ManagedRepository')

name = 'delete_test_%s' % time.time()
directory = getDirectory(name)
repository.makeDir(directory, True)
for i in range(count):
    name = os.path.join(directory, 'file%s.txt' % i)
    print "Creating", name
    targetfile = repository.file(name, 'rw')
    targetfile.truncate(0)
    targetfile.write('ABC123', 0, 6)
    targetfile.close()


handle = repository.deletePaths([directory], True, True)
try:
    conn._waitOnCmd(handle, loops=timeout * 2)  # loops are 500ms
finally:
    handle.close()
