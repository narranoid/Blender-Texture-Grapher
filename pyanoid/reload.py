import sys, os
import importlib
import pyanoid
import types
import inspect

def reload_recursive(path, packages):
    if isinstance(packages, str):
        packages = [packages]

    path = os.path.normpath(path)
    modules_and_packages = []
    reload_packages = []

    for package in packages:
        for root, dirs, files in os.walk(os.path.join(path, package)):
            for file in files:
                # check if the file is a python file and not an __init__
                if file.endswith(".py"):
                    #if file != "__init__.py":
                    # get the name of the module, without extension,
                    local_module_name = os.path.splitext(file)[0]
                    module_path = os.path.join(root, local_module_name)[len(path):]

                    if module_path.startswith(os.path.sep):
                        module_path = module_path[len(os.path.sep):]
                    elif module_path.startswith(os.path.altsep):
                        module_path = module_path[len(os.path.altsep):]

                    full_module_name = module_path.replace(os.path.sep, ".").replace(os.path.altsep, ".")
                    if full_module_name.endswith(".__init__"):
                        full_module_name = full_module_name[:-len(".__init__")]
                        reload_packages.append(full_module_name)
                    #else:
                    print("reloading " + full_module_name)
                    module = importlib.import_module(full_module_name)
                    importlib.reload(module)
                    modules_and_packages.append(full_module_name)
                    #rreload_by_name(full_module_name, path)
                    del (sys.modules[full_module_name])

                    # reimport module
                    #importlib.__import__(full_module_name)
                    #__import__(full_module_name, globals(), locals(), [], 0)

    for mp in modules_and_packages:
        importlib.import_module(mp)
        del (sys.modules[mp])
        #rreload_by_name(mp, path)
        #print("reimporting " + mp)
        #__import__(mp, globals(), locals(), [], 0)

    for pkg in reload_packages:
        pass
        #print("reloading package __init__ "+pkg)
        #module = importlib.import_module(pkg)
        #importlib.reload(module)
        # reimport module
        # importlib.__import__(full_module_name)
        #__import__(pkg, globals(), locals(), [], 0)


def reload_recursive_by_name(modules_and_packages, root_path):
    if isinstance(modules_and_packages, str):
        modules_and_packages = [modules_and_packages]
    for mod_or_pkg_name in modules_and_packages:
        mp = importlib.import_module(mod_or_pkg_name)
        if inspect.ismodule(mp):
            rreload(mp, root_path)



def rreload_by_name(module_name, root_path):
    module = importlib.import_module(module_name)
    rreload(module, root_path, [])


def rreload(module, root_path, reloaded):
    """Recursively reload modules."""
    root_path = os.path.normpath(root_path)
    print("reloading "+module.__name__)
    importlib.reload(module)
    for attribute_name in dir(module):
        attribute = getattr(module, attribute_name)
        if inspect.ismodule(attribute) and hasattr(attribute, "__file__") and os.path.normpath(attribute.__file__).startswith(root_path) and attribute not in reloaded:
            reloaded.append(attribute)
            rreload(attribute, root_path, reloaded)

if __name__ == "__main__":
    importlib.reload(pyanoid)
    # the_file_path = r""
    #reload_recursive_by_name("stringfiddle", the_file_path)
    #reload_recursive(the_file_path, "stringfiddle")
    #rreload_by_name("stringfiddle", the_file_path)
    #reload_recursive(the_file_path, "pyanoid")
    #reload_recursive(the_file_path, "texture")
    #reload_recursive(the_file_path, "textureblender")
