import os
import json


class PyStore:

    @classmethod
    def store(cls, objs, filename='store.json'):
        root_dir = os.path.dirname(os.path.abspath(__file__))
        with open('{0}/{1}'.format(root_dir, filename), 'w', encoding='utf-8') as outfile:
            json.dump(objs, outfile, indent=4, ensure_ascii=False, sort_keys=True, default=str)

    @classmethod
    def read(cls, filename='store.json'):
        root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        objs = []
        if os.path.exists('{0}/{1}'.format(root_dir, filename)) and os.path.getsize(
                '{0}/{1}'.format(root_dir, filename)) > 0:
            with open('{0}/{1}'.format(root_dir, filename), 'r') as outfile:
                objs = json.load(outfile)
        return objs

    @classmethod
    def last_obj(cls, filename='store.json'):
        old_objs = PyStore.read(filename)
        if old_objs is not None and len(old_objs) >= 1:
            return old_objs[-1]
        return None

    @classmethod
    def add_obj(cls, new_obj, filename='store.json'):
        objs = PyStore.read(filename)
        objs.append(new_obj)
        PyStore.store(objs)
