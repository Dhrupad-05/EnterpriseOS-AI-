class PluginRegistry:
    def __init__(self): self._plugins={}
    def register(self,name,plugin): self._plugins[name]=plugin
    def get(self,name): return self._plugins[name]
    def names(self): return tuple(self._plugins)
