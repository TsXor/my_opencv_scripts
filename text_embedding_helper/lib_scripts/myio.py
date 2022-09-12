import pickle, base64

def obj2str(obj):
    obj_pkl = pickle.dumps(obj)
    obj_pkl_b64byte = base64.b64encode(obj_pkl)
    obj_pkl_b64str = obj_pkl_b64byte.decode()
    return obj_pkl_b64str
def str2obj(obj_pkl_b64str):
    obj_pkl_b64byte = obj_pkl_b64str.encode()
    obj_pkl = base64.b64decode(obj_pkl_b64byte)
    obj = pickle.loads(obj_pkl)
    return obj 