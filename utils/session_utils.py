import pickle
from flask import session

def save_params_to_session(params_dict):
    for key, value in params_dict.items():
        session[key] = pickle.dumps(value)

def load_param_from_session(key, default=None):
    return pickle.loads(session.get(key, pickle.dumps(default)))

def get_session_param(key, default=None):
    return pickle.loads(session.get(key, pickle.dumps(default)))
