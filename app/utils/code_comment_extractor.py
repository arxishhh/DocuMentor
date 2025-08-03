import ast
import asttokens
import re

inline_comment = re.compile(r'^(?P<code>.*?\S)\s+#(?P<comment>.*)$')
above_line_comment = re.compile(r'^\s*#(?P<comment>.+)$')

def processing_file(file):
    with open(file, 'r') as f:
        files = f.read()
    atok = asttokens.ASTTokens(files, parse=True)
    tree = atok.tree
    return tree,atok


def finding_func(file):
    func_doc = []
    tree,atok = processing_file(file)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            code = atok.get_text(node)
            func_doc.append(code)
    return func_doc

def comment_extractor(file):
    tree, atok = processing_file(file)
    global inline_comment,above_line_comment
    com_cod = []
    for node in ast.walk(tree):
        text = atok.get_text(node)
        for i, line in enumerate(text.splitlines()):
            if match := inline_comment.match(line):
                code = match.group('code').strip()
                comment = match.group('comment').strip()
            elif match := above_line_comment.match(line):
                code = text.splitlines()[i + 1].strip() if i + 1 < len(text) else None
                comment = match.group('comment').strip()
            else:
                code = None
                comment = None
            if code == None or comment == None:
                continue
            else:
                com_cod.append({
                    'Code':code,
                    'Comment':comment,
                })
    return com_cod
if __name__ == '__main__':
    print(comment_extractor('sample.py'))