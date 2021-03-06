from collections import OrderedDict

from node_visitor import NodeVisitor


class Symbol(object):
    def __init__(self, name, type=None):
        self.name = name
        self.type = type

    def __str__(self):
        return '<{name}:{type}>'.format(name=self.name, type=self.type)

    __repr__ = __str__


class BuiltinTypeSymbol(Symbol):
    def __init__(self, name):
        super(BuiltinTypeSymbol, self).__init__(name)

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<{class_name}(name='{name}')>".format(
            class_name=self.__class__.__name__,
            name=self.name,
        )


class VarSymbol(Symbol):
    def __init__(self, name, type):
        super(VarSymbol, self).__init__(name, type)

    def __str__(self):
        return "<{class_name}(name='{name}', type='{type}')>".format(
            class_name=self.__class__.__name__,
            name=self.name,
            type=self.type,
        )


class SymbolTable(object):
    """Table of symbols.
    """
    def __init__(self):
        self._symbols = OrderedDict()
        self._init_builtins()

    def _init_builtins(self):
        BUILTINS = ('INTEGER', 'REAL', 'STRING', 'BOOLEAN')
        for builtin in BUILTINS:
            self.define(BuiltinTypeSymbol(builtin))

    def define(self, symbol):
        """Procedure that defines symbol in table.

        :param symbol: string
        """
        self._symbols[symbol.name] = symbol

    def lookup(self, name):
        """Return symbol with given name.

        :param name: string symbol name
        """
        symbol = self._symbols.get(name)
        return symbol

    def __str__(self):
        return 'Symbols: {symbols}'.format(
            symbols=[val for val in self._symbols.values()]
        )


class SymbolTableBuilder(NodeVisitor):
    """Table builder working as node visitor.
    While visiting each node created needed symbols
    """
    def __init__(self):
        self.symtab = SymbolTable()

    def build(self, tree):
        """Build symbol table."""
        self.visit(tree)

    def visit_Program(self, node):
        self.visit(node.block)

    def visit_Block(self, node):
        for declaration in node.declarations:
            self.visit(declaration)
        self.visit(node.compound_statement)

    def visit_ProcedureDeclaration(self, node):
        pass

    def visit_Compound(self, node):
        for child in node.children:
            self.visit(child)

    def visit_Condition(self, node):
        self.visit(node.condition)
        self.visit(node.statement)
        self.visit(node.otherwise)

    def visit_ForLoop(self, node):
        self.visit(node.identifier)
        self.visit(node.boundary)
        self.visit(node.statement)

    def visit_Writeln(self, node):
        pass

    def visit_Assign(self, node):
        var_name = node.left.value
        var_symbol = self.symtab.lookup(var_name)
        if var_symbol is None:
            raise NameError(repr(var_name))

        self.visit(node.right)

    def visit_VarDecl(self, node):
        type_name = node.type.value
        type_symbol = self.symtab.lookup(type_name)
        var_name = node.var.value
        var_symbol = VarSymbol(var_name, type_symbol)

        if self.symtab.lookup(var_name) is None:
            # TODO: improve verbosity of exceptions
            raise NameError(
                "{} declared more than once!".format(repr(var_name))
            )

        self.symtab.define(var_symbol)

    def visit_Type(self, node):
        pass

    def visit_Var(self, node):
        var_name = node.value
        var_symbol = self.symtab.lookup(var_name)

        if var_symbol is None:
            raise NameError(repr(var_name))

    def visit_RelOp(self, node):
        self.visit(node.left)
        self.visit(node.right)

    def visit_BinOp(self, node):
        self.visit(node.left)
        self.visit(node.right)

    def visit_UnaryOp(self, node):
        self.visit(node.expr)

    def visit_NoOp(self, node):
        pass

    def visit_Num(self, node):
        pass

    def visit_String(self, node):
        pass

    def visit_Boolean(self, node):
        pass
