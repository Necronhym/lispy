import sys

def standard_env():
	env = Env()
	env

def tekenize(code):
	return code.replace('(', ' ( ' ).replace(')', ' ) ').split()

def parse(code):
	return read_from_tokens(tekenize(code))

def read_from_tokens(tokens):
	if len(tokens) == 0:
		print("Error unexpected EOF")

	token = tokens.pop(0)

	if token == '(':
		L = []
		while tokens[0] != ')':
			L.append(read_from_tokens(tokens))
		tokens.pop(0)
		return L
	elif token == ')':
		print("Unexpected )")
	else:
		return atom(token)

def atom(token):
	try:
		return int(token)
	except ValueError:
		try:
			return float(token)
		except ValueError:
			return str(token)

lispy_env = {
#Basic Math:
'+': lambda x,y: x+y,
'-': lambda x,y: x-y,
'/': lambda x,y: x/y,
'*': lambda x,y: x*y,
#Comparators:
'<': lambda x,y: x<y,
'>': lambda x,y: x>y,
'>=': lambda x,y: x>=y,
'<=': lambda x,y: x<=y,
'=': lambda x,y: x==y,

'begin': lambda *x: x[-1],

'print': lambda x: print(x)
}

def eval(x, env):
	#Var Ref:
	if isinstance(x, str):
		return env[x]
	#Atomic number:
	elif isinstance(x, (int, float)):
		return x
	#Define:
	elif x[0] == 'define':
		(_, symbol, exp) = x
		env[symbol] = eval(exp, env)
	#Function call:
	else:
		proc = eval(x[0], lispy_env)
		args = [eval(arg, lispy_env) for arg in x[1:]]
		return proc(*args)

program = ''
f = open(sys.argv[1], "r")
for l in f:
  program = program + l
program = program.replace('\n', '')
print(program)

eval(parse(program), lispy_env)