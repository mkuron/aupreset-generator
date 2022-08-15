import importlib

m = importlib.import_module(__package__)

for f in m.__all__:
    getattr(m, f)()
