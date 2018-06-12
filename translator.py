#!/etc/python
#Note:
#    +array of high dimension[ https://www.cnblogs.com/ye-ming/articles/7990986.html          ]
#    +stdcall                [ https://blog.csdn.net/citywanderer2005/article/details/1651312 ]
# PSEUDO HEADER
# =============
# class FileASTVisitor(NodeVisitor);
# class FuncDefVisitor(NodeVisitor);
# class InlineCompoundVisitor(NodeVisitor);
# class ReturnVisitor(NodeVisitor);
# class UnaryOpVisitor(NodeVisitor);
# class BinaryOpVisitor(NodeVisitor);
# class DeclVisitor(NodeVisitor);
# class AssignmentVisitor(NodeVisitor);
# class IfVisitor(NodeVisitor);
# class WhileVisitor(NodeVisitor);
# class ForVisitor(NodeVisitor);
# class FuncCallVisitor(NodeVisitor);
from pycparser import parse_file
from pycparser.c_ast import NodeVisitor, Return, BinaryOp, Decl, Assignment
from pycparser.c_ast import TypeDecl, ArrayDecl
from pycparser.c_ast import ArrayRef, ID
from pycparser.c_ast import PtrDecl, UnaryOp, Constant
from pycparser.c_ast import If
from pycparser.c_ast import While
from pycparser.c_ast import For
from pycparser.c_ast import Break, Continue
from pycparser.c_ast import Compound
from pycparser.c_ast import FuncCall, FuncDef
from pycparser.c_ast import FileAST
import sys


data=[]
_bss=[]
text=[]
# symbol table.
symbol_table_array        =[]
symbol_table_parent       ={}
symbol_table_child        ={}
symbol_table_current_index=[0]
class FileASTVisitor(NodeVisitor):
    def visit_FileAST(self, node):
        # initialize symbol table(single file).
        symbol_table_current  ={}
        symbol_table_array.append(symbol_table_current)
        for item in node.ext:
            if type(item)==Decl:
                DeclVisitor().visit(item)
            elif type(item)==FuncDef:
                FuncDefVisitor().visit(item)


class FuncDefVisitor(NodeVisitor):
    def visit_FuncDef(self, node):
        # how to handle function defs ?
        #BlockCompoundVisitor().visit(node.body)
        # symbol table.
        symbol_table_current  ={}
        symbol_table_array.append(symbol_table_current)
        symbol_table_parent[str(len(symbol_table_array)-1)]=symbol_table_current_index[0]
        # 'parent' may have multiple children
        if symbol_table_child.__contains__(str(symbol_table_current_index[0])):
            symbol_table_child[str(symbol_table_current_index[0])].append(len(symbol_table_array)-1)
        else:
            symbol_table_child[str(symbol_table_current_index[0])]=[len(symbol_table_array)-1]
        symbol_table_current_index[0]=len(symbol_table_array)-1
        
        node_decl=node.decl
        func_nym=node_decl.type.type.declname
        func_ret=node_decl.type.type.type.names[0]
        for param in node_decl.type.args.params:
            param_id=param.type.declname
            param_tp=param.type.type.names[0]
            if param_tp=='int':
                symbol_table_current[param_id]={'type':'int',   'offset':-1,'length':4}
            elif param_tp=='double':
                symbol_table_current[param_id]={'type':'double','offset':-1,'length':8}
            elif param_tp=='float':
                symbol_table_current[param_id]={'type':'float', 'offset':-1,'length':4}
            elif param_tp=='char':
                symbol_table_current[param_id]={'type':'char',  'offset':-1,'length':1}
        
        node_body=node.body
        if len(node_body.block_items)==0:
            return
        #preprocess_bss()
        start=0
        block_item_decl=node_body.block_items[start]
        while type(block_item_decl)==Decl:
            DeclVisitor().visit(block_item_decl)
            start+=1
            if start > len(node_body.block_items) - 1:
                return
            block_item_decl=node_body.block_items[start]
        #preprocess_text()
        #for block_item in node_body.block_items:    
        for i in range(start, len(node_body.block_items)):
            block_item=node_body.block_items[i]
            if type(block_item)==Return:
                ReturnVisitor().visit(block_item)
            elif type(block_item)==UnaryOp:
                UnaryOpVisitor().visit(block_item)
            elif type(block_item)==BinaryOp:
                BinaryOpVisitor().visit(block_item)
            elif type(block_item)==Assignment:
                AssignmentVisitor().visit(block_item)
            elif type(block_item)==If:
                IfVisitor().visit(block_item)
            elif type(block_item)==While:
                WhileVisitor().visit(block_item)
            elif type(block_item)==For:
                ForVisitor().visit(block_item)
            elif type(block_item)==FuncCall:
                FuncCallVisitor().visit(block_item)
            elif type(block_item)==Compound:
                InlineCompoundVisitor().visit(block_item)
        #ReturnVisitor().visit(node_body)


class InlineCompoundVisitor(NodeVisitor):
    def visit_Compound(self, node):
        # symbol table.
        symbol_table_current  ={}
        symbol_table_array.append(symbol_table_current)
        symbol_table_parent[str(len(symbol_table_array)-1)]=symbol_table_current_index[0]
        # 'parent' may have multiple children
        if symbol_table_child.__contains__(str(symbol_table_current_index[0])):
            symbol_table_child[str(symbol_table_current_index[0])].append(len(symbol_table_array)-1)
        else:
            symbol_table_child[str(symbol_table_current_index[0])]=[len(symbol_table_array)-1]
        symbol_table_current_index[0]=len(symbol_table_array)-1
        if len(node.block_items)==0:
            return
        for block_item in node.block_items: 
            if type(block_item)==Decl:
                DeclVisitor().visit(block_item)
            elif type(block_item)==Return:
                ReturnVisitor().visit(block_item)
            elif type(block_item)==UnaryOp:
                UnaryOpVisitor().visit(block_item)
            elif type(block_item)==BinaryOp:
                BinaryOpVisitor().visit(block_item)
            elif type(block_item)==Assignment:
                AssignmentVisitor().visit(block_item)
            elif type(block_item)==If:
                IfVisitor().visit(block_item)
            elif type(block_item)==While:
                WhileVisitor().visit(block_item)
            elif type(block_item)==For:
                ForVisitor().visit(block_item)
            elif type(block_item)==Compound:
                InlineCompoundVisitor().visit(block_item)
        # symbol table.
        symbol_table_current_index[0]=symbol_table_parent[str(symbol_table_current_index[0])]


class ReturnVisitor(NodeVisitor):
    def visit_Return(self, node):
        #text.append('%s, %s'%(node.expr.type, node.expr.value))
        #text.append('section .text')
        #text.append('global _start')
        #text.append('_start:')
        
        text.append('mov eax, 1')# ..[NASM]<==>call exit[ASM,AT&T]
        text.append('mov ebx, %s' % (node.expr.value))
        text.append('int 80h')


class UnaryOpVisitor(NodeVisitor):
    def visit_UnaryOp(self, node):
        op=node.op
        if op=='&':
            addr=node.expr.name
            text.append('mov eax, %s' % (addr))# mov eax, addr
        elif op=='+':
            rvalue_type=node.expr.type
            rvalue_value=node.expr.value
            if rvalue_type=='int':
                text.append('mov eax, %s' % rvalue_value)
        elif op=='-':
            rvalue_type=node.expr.type
            rvalue_value=node.expr.value
            if rvalue_type=='int':
                text.append('mov eax, 0')
                text.append('sub eax, %s' % rvalue_value)
        elif op=='sizeof':
            identifier_type=node.expr.type.type.names[0]
            if identifier_type=='int':
                text.append('mov eax, 4')
            elif identifier_type=='double':
                text.append('mov eax, 8')
            elif identifier_type=='float':
                text.append('mov eax, 4')
            elif identifier_type=='char':
                text.append('mov eax, 1')


class BinaryOpVisitor(NodeVisitor):
    def visit_BinaryOp(self, node):
        op=node.op
        if type(node.left)==Constant:
            left_type=node.left.type
            left_value=node.left.value
        elif type(node.left)==ID:
            IDVisitor().visit(node.left)
            left_value='['+node.left.name+']'
        
        if type(node.right)==Constant:
            right_type=node.right.type
            right_value=node.right.value
        elif type(node.right)==ID:
            IDVisitor().visit(node.right)
            right_value='['+node.right.name+']'

        if node.op=='+':
            text.append('mov eax,%s' % (left_value))
            text.append('add eax,%s' % (right_value))
        elif node.op=='-':
            text.append('mov eax,%s' % (left_value))
            text.append('sub eax,%s' % (right_value))
        elif node.op=='*':
            text.append('mov eax,%s' % (left_value))
            text.append('mov ecx,%s' % (right_value))
            text.append('imul ecx,eax')
            text.append('mov eax, ecx')
        elif node.op=='/':
            text.append('mov ecx,%s' % (right_value))
            text.append('mov eax,%s' % (left_value))
            text.append('cdq')
            text.append('idiv ecx')
        elif node.op=='%':
            text.append('mov ecx,%s' % (right_value))
            text.append('mov eax,%s' % (left_value))
            text.append('cdq')
            text.append('idiv ecx')
            text.append('mov eax, edx')
        elif node.op=='==':
            text.append('mov eax, %s' % (left_value))# mov eax, left_value
            text.append('mov ecx, %s' % (right_value))# mov ecx, right_value
            text.append('cmp ecx, ecx')# cmp ecx, eax
            text.append('mov eax, 0')# mov eax, 0
            text.append('sete al')# sete al
        elif node.op=='!=':
            text.append('mov eax, %s' % (left_value))# mov eax, left_value
            text.append('mov ecx, %s' % (right_value))# mov ecx, right_value
            text.append('cmp ecx, ecx')# cmp ecx, eax
            text.append('mov eax, 0')# mov eax, 0
            text.append('setne al')# sete al
        elif node.op=='>':
            text.append('mov eax, %s' % (left_value))# mov eax, left_value
            text.append('mov ecx, %s' % (right_value))# mov ecx, right_value
            text.append('cmp ecx, ecx')# cmp ecx, eax
            text.append('mov eax, 0')# mov eax, 0
            text.append('setg al')# sete al
        elif node.op=='>=':
            text.append('mov eax, %s' % (left_value))# mov eax, left_value
            text.append('mov ecx, %s' % (right_value))# mov ecx, right_value
            text.append('cmp ecx, ecx')# cmp ecx, eax
            text.append('mov eax, 0')# mov eax, 0
            text.append('setge al')# sete al
        elif node.op=='<':
            text.append('mov eax, %s' % (left_value))# mov eax, left_value
            text.append('mov ecx, %s' % (right_value))# mov ecx, right_value
            text.append('cmp ecx, ecx')# cmp ecx, eax
            text.append('mov eax, 0')# mov eax, 0
            text.append('setl al')# sete al
        elif node.op=='<=':
            text.append('mov eax, %s' % (left_value))# mov eax, left_value
            text.append('mov ecx, %s' % (right_value))# mov ecx, right_value
            text.append('cmp ecx, ecx')# cmp ecx, eax
            text.append('mov eax, 0')# mov eax, 0
            text.append('setle al')# sete al


class DeclVisitor(NodeVisitor):
    def visit_Decl(self, node):
        name=node.name
        if type(node.type)==TypeDecl:
            decl_type=node.type.type.names[0]
            # symbol table.
            symbol_table_current      =symbol_table_array[symbol_table_current_index[0]]
            if decl_type=='int':
                _bss.append('%s resb %s' % (name, 4))
                symbol_table_current[name]={'type':'int',   'offset':-1,'length':4}
            elif decl_type=='double':
                _bss.append('%s resb %s' % (name, 8))
                symbol_table_current[name]={'type':'double','offset':-1,'length':8}
            elif decl_type=='float':
                _bss.append('%s resb %s' % (name, 4))
                symbol_table_current[name]={'type':'float', 'offset':-1,'length':4}
            elif decl_type=='char':
                _bss.append('%s resb %s' % (name, 1))
                symbol_table_current[name]={'type':'char',  'offset':-1,'length':1}
        elif type(node.type)==ArrayDecl:
            decl_type=node.type.type.type.names[0]
            array_length=int(node.type.dim.value)
            if decl_type=='int':
                _bss.append('%s resb %s' % (name, 4*array_length))
            elif decl_type=='double':
                _bss.append('%s resb %s' % (name, 8*array_length))
            elif decl_type=='float':
                _bss.append('%s resb %s' % (name, 4*array_length))
            elif decl_type=='char':
                _bss.append('%s resb %s' % (name, 1*array_length))
        elif type(node.type)==PtrDecl:
            # ptr <==> int.
            _bss.append('%s resb %s' % (name, 4))
            # ptr_type=node.type.type.type.names[0]


class AssignmentVisitor(NodeVisitor):
    def visit_Assignment(self, node):
        op=node.op # assume op->'+'.
        lvalue=node.lvalue
        if type(lvalue)==ID:
            IDVisitor().visit(lvalue)
            lvalue_name=lvalue.name
            rvalue=node.rvalue
            if type(rvalue)==Constant:
                rvalue_type=rvalue.type
                rvalue_value=rvalue.value
                
                if rvalue_type=='int':
                    text.append('mov eax,%s' % (rvalue_value))
                    text.append('mov [%s],eax' % (lvalue_name))
                elif rvalue_type=='double':
                    pass
                elif rvalue_type=='float':
                    pass
                elif rvalue_type=='char':
                    text.append('mov eax,%s' % (ord(rvalue_value.strip('"').strip("'"))))
                    text.append('mov [%s],al' % (lvalue_name))
            elif type(rvalue)==UnaryOp:
                UnaryOpVisitor().visit(rvalue)
                text.append('mov [%s], eax' % (lvalue_name))
            elif type(rvalue)==BinaryOp:
                BinaryOpVisitor().visit(rvalue)
                text.append('mov [%s], eax' % (lvalue_name))
        elif type(lvalue)==ArrayRef:
            array_name=lvalue.name.name
            array_subscript=lvalue.subscript.value

            rvalue_type=node.rvalue.type
            rvalue_value=node.rvalue.value

            if rvalue_type=='int':
                text.append('mov eax,%s' % (rvalue_value))
                text.append('mov [%s+4*%s],eax' % (array_name, array_subscript))
            elif rvalue_type=='double':
                pass
            elif rvalue_type=='float':
                pass
            elif rvalue_type=='char':
                text.append('mov eax,%s' % (ord(rvalue_value.strip('"').strip("'"))))
                text.append('mov [%s+4*%s],al' % (array_name, array_subscript))


class IfVisitor(NodeVisitor):
    def visit_If(self, node):
        cond   =node.cond
        iftrue =node.iftrue
        iffalse=node.iffalse
        
        line   =node.coord.line
        column =node.coord.column
        label  ='_'+str(line)+'_'+str(column)
        label_start =label+'_start'
        label_branch=label+'_branch'
        label_end   =label+'_end'
        text.append(label_start+':') # label_start:
        # (cond)
        if type(cond)==UnaryOp:
            UnaryOpVisitor().visit(cond)
        elif type(cond)==BinaryOp:
            BinaryOpVisitor().visit(cond)
        text.append('cmp eax, 1') # cmp eax, 1
        text.append('jne %s' % (label_branch))# jne label_branch
        # (iftrue)
        if type(iftrue)==Compound:
            InlineCompoundVisitor().visit(iftrue)
        elif type(iftrue)==Return:
            ReturnVisitor().visit(iftrue)
        elif type(iftrue)==UnaryOp:
            UnaryOpVisitor().visit(iftrue)
        elif type(iftrue)==BinaryOp:
            BinaryOpVisitor().visit(iftrue)
        elif type(iftrue)==Assignment:
            AssignmentVisitor().visit(iftrue)
        elif type(iftrue)==If:
            IfVisitor().visit(iftrue)
        elif type(iftrue)==Break:
            text.append('jmp %s' % (label_end)) # jmp label_end
        text.append('jmp %s' % (label_end)) # jmp label_end
        text.append(label_branch+':') # label_branch:
        # (iffalse)
        if type(iffalse)==Compound:
            InlineCompoundVisitor().visit(iffalse)
        elif type(iffalse)==Return:
            ReturnVisitor().visit(iffalse)
        elif type(iffalse)==UnaryOp:
            UnaryOpVisitor().visit(iffalse)
        elif type(iffalse)==BinaryOp:
            BinaryOpVisitor().visit(iffalse)
        elif type(iffalse)==Assignment:
            AssignmentVisitor().visit(iffalse)
        elif type(iffalse)==If:
            IfVisitor().visit(iffalse)
        elif type(iffalse)==Break:
            text.append('jmp %s' % (label_end)) # jmp label_end
        text.append(label_end+':')# label_end


class WhileVisitor(NodeVisitor):
    def visit_While(self, node):
        cond=node.cond
        stmt=node.stmt
        line=node.coord.line
        column=node.coord.column

        label  ='_'+str(line)+'_'+str(column)
        label_start =label+'_start'
        label_branch=label+'_branch'
        label_end   =label+'_end'
        # (cond)
        if type(cond)==UnaryOp:
            UnaryOpVisitor().visit(cond)
        elif type(cond)==BinaryOp:
            BinaryOpVisitor().visit(cond)
        text.append('cmp eax, 0') # cmp eax, 0
        text.append('je %s' % (label_end)) # je _while_end
        text.append('jmp %s' % (label_start)) # jmp _while_start
        text.append(label_start+':')# _while_start:
        # (stmt)
        if type(stmt)==Compound:
            InlineCompoundVisitor().visit(stmt)
        elif type(stmt)==Return:
            ReturnVisitor().visit(stmt)
        elif type(stmt)==UnaryOp:
            UnaryOpVisitor().visit(stmt)
        elif type(stmt)==BinaryOp:
            BinaryOpVisitor().visit(stmt)
        elif type(stmt)==Assignment:
            AssignmentVisitor().visit(stmt)
        elif type(stmt)==If:
            IfVisitor().visit(stmt)
        elif type(stmt)==While:
            WhileVisitor().visit(stmt)
        elif type(stmt)==Break:
            text.append('jmp %s' % (label_end))
        elif type(stmt)==Continue:
            text.append('jmp %s' % (label_branch))
        text.append(label_branch+':') # _while_branch:
        # (cond)
        if type(cond)==UnaryOp:
            UnaryOpVisitor().visit(cond)
        elif type(cond)==BinaryOp:
            BinaryOpVisitor().visit(cond)
        text.append('cmp eax, 0') # cmp eax, 0
        text.append('je %s' % (label_end)) # je _while_end
        text.append('jmp %s' % (label_start)) # jmp _while_start
        text.append(label_end+':') # _while_end:


class ForVisitor(NodeVisitor):
    def visit_For(self, node):
        init=node.init
        cond=node.cond
        next=node.next
        stmt=node.stmt
        line=node.coord.line
        column=node.coord.column

        label  ='_'+str(line)+'_'+str(column)
        label_start =label+'_start'
        label_branch=label+'_branch'
        label_end   =label+'_end'

        # (init)
        if type(init)==Assignment:
            AssignmentVisitor().visit(init)
        # (cond)
        if type(cond)==UnaryOp:
            UnaryOpVisitor().visit(cond)
        elif type(cond)==BinaryOp:
            BinaryOpVisitor().visit(cond)
        text.append('cmp eax, 0') # cmp eax, 0
        text.append('je %s' % (label_end)) # je _for_end
        text.append('jmp %s' % (label_start)) # jmp _for_start
        # for_start:
        text.append(label_start+':')
        # (stmt)
        if type(stmt)==Compound:
            InlineCompoundVisitor().visit(stmt)
        elif type(stmt)==Return:
            ReturnVisitor().visit(stmt)
        elif type(stmt)==UnaryOp:
            UnaryOpVisitor().visit(stmt)
        elif type(stmt)==BinaryOp:
            BinaryOpVisitor().visit(stmt)
        elif type(stmt)==Assignment:
            AssignmentVisitor().visit(stmt)
        elif type(stmt)==If:
            IfVisitor().visit(stmt)
        elif type(stmt)==While:
            WhileVisitor().visit(stmt)
        elif type(stmt)==Break:
            text.append('jmp %s' % (label_end))
        elif type(stmt)==Continue:
            text.append('jmp %s' % (label_branch))
        text.append(label_branch+':') # for_branch:
        # (next)
        if type(next)==Assignment:
            AssignmentVisitor().visit(next)
        # (cond)
        if type(cond)==UnaryOp:
            UnaryOpVisitor().visit(cond)
        elif type(cond)==BinaryOp:
            BinaryOpVisitor().visit(cond)
        text.append('cmp eax, 0') # cmp eax, 0
        text.append('je %s' % (label_end)) # je _for_end
        text.append('jmp %s' % (label_start)) # jmp _for_start
        text.append(label_end+':') # for_end:


class FuncCallVisitor(NodeVisitor):
    def visit_FuncCall(self, node):
        func_name=node.name.name
        func_args=node.args.exprs
        tag      ='_'+str(node.coord.line)+'_'+str(node.coord.column)
        if func_name=='printf':
            data.append('%s: db %s,0xa,0' % (tag, func_args[0].value))
            if len(func_args)==1:
                text.append('push dword %s' % (tag))
                text.append('extern printf')
                text.append('call printf')
                text.append('add esp,byte 4')
            else:
                for i in range(len(func_args), 1, -1):
                    text.append('push dword [%s]' % (func_args[i-1].name))
                text.append('push dword %s' % (tag))
                text.append('extern printf')
                text.append('call printf')
                text.append('add esp,byte %s' % (str(4*len(func_args))))


class IDVisitor(NodeVisitor):
    def visit_ID(self, node):
        var_name =node.name
        var_coord=node.coord
        symbol_table_current_index_copy=symbol_table_current_index[0]
        symbol_table_current           =symbol_table_array[symbol_table_current_index_copy]
        while not symbol_table_current.__contains__(var_name):
            if symbol_table_parent.__contains__(str(symbol_table_current_index_copy)):
                symbol_table_current_index_copy=symbol_table_parent[str(symbol_table_current_index_copy)]
            else:
                break
            symbol_table_current           =symbol_table_array[symbol_table_current_index_copy]
        if not symbol_table_current.__contains__(var_name):
            print(str(var_coord.line)+':'
                 +str(var_coord.column)+':'
                 +'Error: variable '+"'"+var_name+"'"+' refered to before assignment.')
            sys.exit()


def generate_asm():
    print('section data')
    for item in data:
        print(item)
    print('section .bss')
    for item in _bss:
        print(item)
    print('section .text')
    print('global main')
    print('main:')
    for item in text:
        print(item)


def generate_symbol_table():
    print(symbol_table_array)
    print(symbol_table_parent)
    print(symbol_table_child)


# pseudo entry.
ast = parse_file('/home/dell/Desktop/Compiler/2-function_call.c',use_cpp=False)
FileASTVisitor().visit(ast)
generate_asm()
generate_symbol_table()

