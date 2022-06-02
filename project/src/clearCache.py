import pickle
from pathlib import Path
f = open(str(Path().resolve().parent.absolute()) + '/saveddata/cacheinfo.pkl', 'wb')
empt = {}
pickle.dump(empt, f)
f.close()
