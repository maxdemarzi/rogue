import ast

class SecureASTValidator(ast.NodeVisitor):
    """
    Abstract Syntax Tree (AST) validator enforcing allow-lists for modules
    and preventing arbitrary code execution vectors inside the sandbox.
    """
    def __init__(self):
        # Allowed imports list
        self.allowed_imports = {
            'pandas', 'numpy', 'openpyxl', 'pyrel_duckdb', 'json', 'math', 'datetime', 'scipy',
            'merton_simulator', 'path_reasoner', 'gnn_model', 'optimizer', 'gnn_explainers',
            'merger_solver', 'path_tracer', 'macro_optimizer', 'live_modeler', 'citation_engine'
        }
        # Prohibited built-in functions
        self.prohibited_calls = {'eval', 'exec', 'open', 'compile', 'getattr', 'setattr', 'delattr'}

    def visit_Import(self, node):
        for alias in node.names:
            base_module = alias.name.split('.')[0]
            if base_module not in self.allowed_imports:
                raise PermissionError(f"AST Error: Import of '{alias.name}' is prohibited in the sandbox.")
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        if node.module:
            base_module = node.module.split('.')[0]
            if base_module not in self.allowed_imports:
                raise PermissionError(f"AST Error: Import from '{node.module}' is prohibited in the sandbox.")
        self.generic_visit(node)

    def visit_Call(self, node):
        # Prevent calls to prohibited functions
        if isinstance(node.func, ast.Name):
            if node.func.id in self.prohibited_calls:
                raise PermissionError(f"AST Error: Call to built-in function '{node.func.id}' is prohibited.")
        self.generic_visit(node)

def exec_in_sandbox(code_str, globals_dict=None, locals_dict=None):
    """
    Validates the code AST and runs it inside a restricted globals/locals environment.
    """
    if globals_dict is None:
        globals_dict = {}
    if locals_dict is None:
        locals_dict = {}

    # 1. Parse and validate AST
    try:
        tree = ast.parse(code_str)
    except SyntaxError as e:
        raise SyntaxError(f"AST Error: Syntax error in generated code: {e}")

    validator = SecureASTValidator()
    validator.visit(tree)

    # 2. Compile and execute in restricted scope
    # Restrict builtins to prevent malicious access
    safe_builtins = __builtins__.copy() if isinstance(__builtins__, dict) else __builtins__.__dict__.copy()
    
    # Remove dangerous functions from builtins
    for name in validator.prohibited_calls:
        safe_builtins.pop(name, None)
        
    globals_dict['__builtins__'] = safe_builtins

    compiled_code = compile(tree, filename="<sandbox>", mode="exec")
    exec(compiled_code, globals_dict, locals_dict)
    return locals_dict
