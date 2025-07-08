import importlib
import os
import pkgutil

#build a list of available plugins from the plugin folder. Default search value is power meter
def discover_plugins(package="plugin_system.plugins", plugin_type="power_meter"):
    plugins = []

    package_module = importlib.import_module(f"{package}.plugins")
    package_path = package_module.__path__

    print(package_path)

    for _, module_name, _ in pkgutil.iter_modules(package_path):
        print(f"Checking: {package}.{module_name}")
        mod = importlib.import_module(f"{package}.{module_name}")
        if hasattr(mod, "plugin_info") and mod.plugin_info.get("type") == plugin_type:
            cls_name = mod.plugin_info["class"]
            print(f"Found plugin of type {plugin_type} : name {cls_name}")
            cls = getattr(mod,cls_name)
            plugins.append((module_name,cls))
    if len(plugins) == 0:
        print(f"ERROR Could not find any plugins of type: {plugin_type} in {package}")
    return plugins

#method for automaticlly connecting devices. User can sepcify number of a type of device to detect
def autodetect_devices(count=1,package="opm_plugin",type="power_meter"):
    found = []
    connected_resources = set()

    plugins = discover_plugins(package,type)

    if len(plugins) == 0:
        print(f"ERROR! No plugins of type: {type} found. Please contact engineering")
    else:
        for module_name, cls in plugins:
            while True:
                print(f"Looking into {cls} from {module_name}")
                result = cls.can_connect()
                if result is None:
                    break

                res_string, conn = result

                if res_string in connected_resources:
                    print(f"Skipping duplicate resource: {res_string}")
                    break
            
                connected_resources.add(res_string)
                print(f"Connected {cls.__name__} to {res_string}")
                found.append(cls(conn))

                if len(found) == count:
                    return found if count > 1 else found[0]
    
    return None

             