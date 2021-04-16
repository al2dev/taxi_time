from os import listdir
from os.path import isfile, join


path = 'data'

files = [f for f in listdir(path) if isfile(join(path, f))]

print(files)

#os.path.dirname(sys.argv[0])
