from collections import Counter
class Metrics:
    def __init__(self): self.counters=Counter(); self.latencies=[]
    def increment(self,name,value=1): self.counters[name]+=value
    def observe(self,name,value): self.latencies.append((name,value))
    def snapshot(self): return {"counters":dict(self.counters),"latencies":self.latencies[-100:]}
