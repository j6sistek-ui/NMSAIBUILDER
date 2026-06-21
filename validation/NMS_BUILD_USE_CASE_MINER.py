"""NMS Build Use-Case Miner.

Parse NMS base JSON exports and print object counts and review prompts for
creative use-case cataloging. This is a signal tool, not automatic promotion.
"""
import json, sys, collections
from pathlib import Path

def load_objects(path):
    data=json.loads(Path(path).read_text(encoding='utf-8',errors='ignore'))
    if isinstance(data,dict): return data.get('Objects',[])
    if isinstance(data,list): return data
    return []

def norm(x): return str(x or '').replace('^','')

def analyze(path):
    objs=load_objects(path)
    counts=collections.Counter(norm(o.get('ObjectID')) for o in objs if isinstance(o,dict))
    print('='*80)
    print('BUILD DATA REVIEW', path)
    print('Objects:',len(objs),'Unique ObjectIDs:',len(counts))
    for oid,c in counts.most_common(25): print(f'{oid}: {c}')
    print('Review prompts:')
    print('- Which parts are used nonliterally?')
    print('- Which repeated patterns imply shell, rib, furniture, foliage, facade, or hidden emitter roles?')
    print('- Which candidates need screenshot validation before catalog promotion?')

if __name__=='__main__':
    for arg in sys.argv[1:]: analyze(arg)
