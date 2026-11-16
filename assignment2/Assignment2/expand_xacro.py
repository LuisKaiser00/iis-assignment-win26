"""Standalone expander for this exercise's Xacro subset (no ROS required).
Only used for optional local demonstration. Use `xacro robot.xacro > robot.urdf` with ROS/Xacro.
"""
from pathlib import Path
from copy import deepcopy
import ast, math, re, sys, xml.etree.ElementTree as ET
NS='{http://www.ros.org/wiki/xacro}'
DEFAULTS={'base_radius':0.18, 'base_height':0.72, 'link1_length':0.48, 'link2_length':0.42, 'gripper_span':0.14}

class SafeEval(ast.NodeVisitor):
    def __init__(self, values):self.values=values
    def visit_Expression(self,node):return self.visit(node.body)
    def visit_Name(self,node):return self.values[node.id]
    def visit_Constant(self,node):
        if isinstance(node.value,(int,float)):return node.value
        raise ValueError('unsupported literal')
    def visit_BinOp(self,node):
        a,b=self.visit(node.left),self.visit(node.right)
        if isinstance(node.op,ast.Add):return a+b
        if isinstance(node.op,ast.Sub):return a-b
        if isinstance(node.op,ast.Mult):return a*b
        if isinstance(node.op,ast.Div):return a/b
        if isinstance(node.op,ast.Pow):return a**b
        raise ValueError('Unsupported operation')
    def visit_UnaryOp(self,node):
        x=self.visit(node.operand)
        return -x if isinstance(node.op,ast.USub) else x if isinstance(node.op,ast.UAdd) else None
    def generic_visit(self,node):raise ValueError(f'Unsafe expression: {type(node).__name__}')

def value(s,env):
    if s.startswith('$(arg ') and s.endswith(')'):return env[s[6:-1]]
    s=re.sub(r'\$\{([^{}]+)\}',lambda m:str(SafeEval(env).visit(ast.parse(m.group(1),mode='eval'))),str(s))
    return s

def expand(path, **params):
    path=Path(path);args=dict(DEFAULTS,**params)
    root=ET.parse(path).getroot();macros={}
    for inc in root.findall(NS+'include'):
        sub=ET.parse(path.parent/inc.get('filename')).getroot()
        for m in sub.findall(NS+'macro'):macros[m.get('name')]=m
    for m in root.findall(NS+'macro'):macros[m.get('name')]=m
    result=ET.Element('robot',{'name':root.get('name')})
    def place(node,parent,env):
        if node.tag==NS+'property':
            env[node.get('name')]=float(value(node.get('value'),env));return
        if node.tag==NS+'arg' or node.tag==NS+'include' or node.tag==NS+'macro':return
        if node.tag.startswith(NS):
            macro=macros[node.tag[len(NS):]]
            locals=dict(env)
            for name in macro.get('params').split():
                v=value(node.get(name),locals)
                try:locals[name]=float(v)
                except (ValueError,TypeError):locals[name]=v
            for child in macro:place(child,parent,locals)
            return
        elem=ET.SubElement(parent,node.tag,{k:str(value(v,env)) for k,v in node.attrib.items()})
        for child in node:place(child,elem,env)
    for c in root:place(c,result,args)
    ET.indent(result,space='  ')
    return result

if __name__=='__main__':
    base=Path(__file__).parent
    config={}
    for arg in sys.argv[1:]:
        k,v=arg.split(':=');config[k]=float(v)
    tree=ET.ElementTree(expand(base/'robot.xacro',**config))
    tree.write(base/'robot.urdf',encoding='unicode',xml_declaration=True)
    print('Wrote',base/'robot.urdf')
