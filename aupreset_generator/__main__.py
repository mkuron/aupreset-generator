import importlib
import sys

m = importlib.import_module(__package__)

if len(sys.argv) > 1:
    print(sys.argv)
    for f in sys.argv[1:]:
        if f not in m.__all__:
            raise NameError(f'{f} not found, available options: ' + ", ".join(sorted(m.__all__)))
        getattr(m, f)()
else:
    for f in m.__all__:
        getattr(m, f)()
