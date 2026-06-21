"""
NMS Non-Uniform Scale Scanner v45
================================

Purpose:
    Static helper for reviewing generated NMS Python scripts.
    Flags obvious non-uniform scale patterns that may stretch real NMS parts
    into unsupported in-game geometry.

Usage:
    python NMS_NONUNIFORM_SCALE_SCANNER.py path/to/script.py
"""

import ast
import sys
from pathlib import Path

SCALE_KEYS = {"sx", "sy", "sz"}

class ScaleVisitor(ast.NodeVisitor):
    def __init__(self):
        self.findings = []

    def visit_Call(self, node):
        kws = {kw.arg: kw.value for kw in node.keywords if kw.arg}
        if SCALE_KEYS.issubset(kws):
            vals = []
            static = True
            for k in ("sx", "sy", "sz"):
                try:
                    vals.append(ast.literal_eval(kws[k]))
                except Exception:
                    static = False
                    vals.append(ast.unparse(kws[k]) if hasattr(ast, "unparse") else "<expr>")
            if not static or len(set(vals)) > 1:
                self.findings.append((node.lineno, "call_keywords", vals))
        self.generic_visit(node)

    def visit_Assign(self, node):
        # Detect obj.scale = (a,b,c)
        for target in node.targets:
            if isinstance(target, ast.Attribute) and target.attr == "scale":
                if isinstance(node.value, (ast.Tuple, ast.List)) and len(node.value.elts) == 3:
                    vals = []
                    static = True
                    for elt in node.value.elts:
                        try:
                            vals.append(ast.literal_eval(elt))
                        except Exception:
                            static = False
                            vals.append(ast.unparse(elt) if hasattr(ast, "unparse") else "<expr>")
                    if not static or len(set(vals)) > 1:
                        self.findings.append((node.lineno, "scale_assignment", vals))
        self.generic_visit(node)

def main(path):
    text = Path(path).read_text(encoding="utf-8")
    tree = ast.parse(text)
    visitor = ScaleVisitor()
    visitor.visit(tree)
    if visitor.findings:
        print("NON_UNIFORM_SCALE_FINDINGS")
        for lineno, kind, vals in visitor.findings:
            print(f"line {lineno}: {kind}: {vals}")
        print("Review required. Rewrite as repeated uniformly-scaled segments or document approved exception.")
        return 1
    print("NON_UNIFORM_SCALE_SCAN_PASS")
    return 0

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python NMS_NONUNIFORM_SCALE_SCANNER.py path/to/script.py")
        raise SystemExit(2)
    raise SystemExit(main(sys.argv[1]))
