import importlib
import os
import pkgutil


#build a list of available plugins from the plugin folder. Default search value is power meter
def discover_plugins(folder="plugins", plugin_type="power_meter"):
    plugins = []
    for _, module_name, _ in pkgutil.iter_modules([folder]):
        mod = importlib.import_module(f"{folder}.{module_name}")
        if hasattr(mod, "plugin_info") and mod.plugin_info.get("type") == plugin_type:
            cls_name = mod.plugin_info["class"]
            cls = getattr(mod,cls_name)
            plugins.append((module_name,cls))
    return plugins

#method for automaticlly connecting devices. User can sepcify number of a type of device to detect
def autodetect_devices(count=1,type="power_meter"):
    plugins = discover_plugins("plugins",type)
    found = []
    for module_name, cls in plugins:
        while True:
            conn = cls.can_connect()
            if conn:
                found.append(cls(conn))
                print(f"Detected {cls.__name__} from {module_name}")
                if len(found) == count:
                    return found
            else:
                break
    raise RuntimeError(f"Only found {len(found)} "+type+" , expected {count}")