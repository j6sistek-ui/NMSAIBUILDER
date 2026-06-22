import json
def main():
    BUILDER = globals().get("BUILDER")
    if BUILDER is None:
        open("preview.json", "w").write("{}")
