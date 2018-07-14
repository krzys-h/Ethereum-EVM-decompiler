import sys

assert sys.version_info[0] == 3

DEBUG = False

# https://github.com/ethereum/pyethereum/blob/develop/ethereum/opcodes.py

# schema: [opcode, ins, outs, gas]
opcodes = {
    0x00: ['STOP', 0, 0, 0],
    0x01: ['ADD', 2, 1, 3],
    0x02: ['MUL', 2, 1, 5],
    0x03: ['SUB', 2, 1, 3],
    0x04: ['DIV', 2, 1, 5],
    0x05: ['SDIV', 2, 1, 5],
    0x06: ['MOD', 2, 1, 5],
    0x07: ['SMOD', 2, 1, 5],
    0x08: ['ADDMOD', 3, 1, 8],
    0x09: ['MULMOD', 3, 1, 8],
    0x0a: ['EXP', 2, 1, 10],
    0x0b: ['SIGNEXTEND', 2, 1, 5],
    0x10: ['LT', 2, 1, 3],
    0x11: ['GT', 2, 1, 3],
    0x12: ['SLT', 2, 1, 3],
    0x13: ['SGT', 2, 1, 3],
    0x14: ['EQ', 2, 1, 3],
    0x15: ['ISZERO', 1, 1, 3],
    0x16: ['AND', 2, 1, 3],
    0x17: ['OR', 2, 1, 3],
    0x18: ['XOR', 2, 1, 3],
    0x19: ['NOT', 1, 1, 3],
    0x1a: ['BYTE', 2, 1, 3],
    0x20: ['SHA3', 2, 1, 30],
    0x30: ['ADDRESS', 0, 1, 2],
    0x31: ['BALANCE', 1, 1, 20],  # now 400
    0x32: ['ORIGIN', 0, 1, 2],
    0x33: ['CALLER', 0, 1, 2],
    0x34: ['CALLVALUE', 0, 1, 2],
    0x35: ['CALLDATALOAD', 1, 1, 3],
    0x36: ['CALLDATASIZE', 0, 1, 2],
    0x37: ['CALLDATACOPY', 3, 0, 3],
    0x38: ['CODESIZE', 0, 1, 2],
    0x39: ['CODECOPY', 3, 0, 3],
    0x3a: ['GASPRICE', 0, 1, 2],
    0x3b: ['EXTCODESIZE', 1, 1, 20], # now 700
    0x3c: ['EXTCODECOPY', 4, 0, 20], # now 700
    0x3d: ['RETURNDATASIZE', 0, 1, 2],
    0x3e: ['RETURNDATACOPY', 3, 0, 3],
    0x40: ['BLOCKHASH', 1, 1, 20],
    0x41: ['COINBASE', 0, 1, 2],
    0x42: ['TIMESTAMP', 0, 1, 2],
    0x43: ['NUMBER', 0, 1, 2],
    0x44: ['DIFFICULTY', 0, 1, 2],
    0x45: ['GASLIMIT', 0, 1, 2],
    0x50: ['POP', 1, 0, 2],
    0x51: ['MLOAD', 1, 1, 3],
    0x52: ['MSTORE', 2, 0, 3],
    0x53: ['MSTORE8', 2, 0, 3],
    0x54: ['SLOAD', 1, 1, 50],  # 200 now
    # actual cost 5000-20000 depending on circumstance
    0x55: ['SSTORE', 2, 0, 0],
    0x56: ['JUMP', 1, 0, 8],
    0x57: ['JUMPI', 2, 0, 10],
    0x58: ['PC', 0, 1, 2],
    0x59: ['MSIZE', 0, 1, 2],
    0x5a: ['GAS', 0, 1, 2],
    0x5b: ['JUMPDEST', 0, 0, 1],
    0xa0: ['LOG0', 2, 0, 375],
    0xa1: ['LOG1', 3, 0, 750],
    0xa2: ['LOG2', 4, 0, 1125],
    0xa3: ['LOG3', 5, 0, 1500],
    0xa4: ['LOG4', 6, 0, 1875],
    # 0xe1: ['SLOADBYTES', 3, 0, 50], # to be discontinued
    # 0xe2: ['SSTOREBYTES', 3, 0, 0], # to be discontinued
    # 0xe3: ['SSIZE', 1, 1, 50], # to be discontinued
    0xf0: ['CREATE', 3, 1, 32000],
    0xf1: ['CALL', 7, 1, 40],  # 700 now
    0xf2: ['CALLCODE', 7, 1, 40],  # 700 now
    0xf3: ['RETURN', 2, 0, 0],
    0xf4: ['DELEGATECALL', 6, 1, 40],  # 700 now
    0xf5: ['CALLBLACKBOX', 7, 1, 40],
    0xfa: ['STATICCALL', 6, 1, 40],
    0xfd: ['REVERT', 2, 0, 0],
    0xff: ['SUICIDE', 1, 0, 0],  # 5000 now
}

opcodesMetropolis = { 0x3d, 0x3e, 0xfa, 0xfd }

for i in range(1, 33):
    opcodes[0x5f + i] = ['PUSH' + str(i), 0, 1, 3]

for i in range(1, 17):
    opcodes[0x7f + i] = ['DUP' + str(i), i, i + 1, 3]
    opcodes[0x8f + i] = ['SWAP' + str(i), i + 1, i + 1, 3]

class Expression:
	pass

class Constant(Expression):
	def __init__(self, val):
		self.value = val

	def __repr__(self):
		if isinstance(self.value, int):
			return hex(self.value)
		else:
			return str(self.value)

class TwoOp(Expression):
	def __init__(self, arg1, op, arg2):
		self.arg1 = arg1
		self.op = op
		self.arg2 = arg2

	@staticmethod
	def create(arg1, op, arg2):
		if isinstance(arg1, Constant) and isinstance(arg1.value, int) and isinstance(arg2, Constant) and isinstance(arg2.value, int):
			return Constant(eval(str(arg1.value) + op + str(arg2.value)))
		else:
			return TwoOp(arg1, op, arg2)

	def __repr__(self):
		return "("+str(self.arg1)+" "+self.op+" "+str(self.arg2)+")"

class OneOp(Expression):
	def __init__(self, op, arg):
		self.op = op
		self.arg = arg

	@staticmethod
	def create(op, arg):
		if isinstance(arg, Constant) and isinstance(arg.value, int):
			return Constant(eval("(" + op + str(arg.value) + ")&0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"))
		else:
			return OneOp(op, arg)

	def __repr__(self):
		return self.op+"("+str(self.arg)+")"

class FuncCall(Expression):
	def __init__(self, name, args):
		self.name = name
		self.args = args

	def __repr__(self):
		return self.name+"("+(", ".join(map(str, self.args)))+")"

class ArrayIndex(Expression):
	def __init__(self, array, index):
		self.array = array
		self.index = index

	def __repr__(self):
		return str(self.array)+"["+str(self.index)+"]"

class ArrayIndexRange(Expression):
	def __init__(self, array, index_start, index_end):
		self.array = array
		self.index_start = index_start
		self.index_end = index_end

	def __repr__(self):
		return str(self.array)+"["+str(self.index_start)+":"+str(self.index_end)+"]"

class ArrayIndexRangeCount(Expression):
	def __init__(self, array, index_start, index_count):
		self.array = array
		self.index_start = index_start
		self.index_count = index_count

	def __repr__(self):
		return str(self.array)+"["+str(self.index_start)+":+"+str(self.index_count)+"]"

class ObjectIndex(Expression):
	def __init__(self, array, index):
		self.array = array
		self.index = index

	def __repr__(self):
		return str(self.array)+"."+self.index

class Goto(Expression):
	def __init__(self, target):
		self.target = target

	def __repr__(self):
		return "goto loc_"+str(self.target)

class GotoIf(Expression):
	def __init__(self, target, condition):
		self.target = target
		self.condition = condition

	def __repr__(self):
		return "if("+str(self.condition)+") goto loc_"+str(self.target)

stack = []
pc = 0

prog_data = open(sys.argv[1], "rb").read()

while pc < len(prog_data):
	c = prog_data[pc]
	stack_start = len(stack)
	if DEBUG:
		if c in opcodes:
			print("\033[1;30m"+("%04x:" % pc)+"    ", opcodes[c][0]+"\033[0m")
		else:
			print("\033[1;30m"+("%04x:" % pc)+"    \033[1;31mBAD OPCODE "+hex(c)+"\033[0m")
	if c == 0x00:  # STOP
		print("exit()")
	elif c == 0x01:  # ADD
		stack.append(TwoOp.create(stack.pop(), "+", stack.pop()))
	elif c == 0x02:  # MUL
		p1 = stack.pop()
		p2 = stack.pop()
		if isinstance(p2, Constant) and p2.value == 0:
			stack.append(Constant(0))
		elif isinstance(p2, Constant) and p2.value == 1:
			stack.append(p1)
		else:
			stack.append(TwoOp.create(p1, "*", p2))
	elif c == 0x03:  # SUB
		stack.append(TwoOp.create(stack.pop(), "-", stack.pop()))
	elif c == 0x04:  # DIV
		p1 = stack.pop()
		p2 = stack.pop()
		if isinstance(p2, Constant) and p2.value == 0:
			stack.append(Constant(0))
		elif isinstance(p2, Constant) and p2.value == 1:
			stack.append(p1)
		else:
			stack.append(TwoOp.create(p1, "/", p2))
	elif c == 0x05:  # SDIV
		p1 = stack.pop()
		p2 = stack.pop()
		if isinstance(p2, Constant) and p2.value == 0:
			stack.append(Constant(0))
		elif isinstance(p2, Constant) and p2.value == 1:
			stack.append(p1)
		else:
			stack.append(TwoOp.create(p1, "signed/", p2))
	elif c == 0x06:  # MOD
		p1 = stack.pop()
		p2 = stack.pop()
		if isinstance(p2, Constant) and p2.value == 0:
			stack.append(Constant(0))
		else:
			stack.append(TwoOp.create(p1, "%", p2))
	elif c == 0x07:  # SMOD
		p1 = stack.pop()
		p2 = stack.pop()
		if isinstance(p2, Constant) and p2.value == 0:
			stack.append(Constant(0))
		else:
			stack.append(TwoOp.create(p1, "signed%", p2))
	elif c == 0x08:  # ADDMOD
		stack.append(TwoOp.create(TwoOp.create(stack.pop(), "+", stack.pop())), stack.pop())
	elif c == 0x09:  # MULMOD
		stack.append(TwoOp.create(TwoOp.create(stack.pop(), "*", stack.pop())), stack.pop())
	elif c == 0x0a:  # EXP
		p1 = stack.pop()
		p2 = stack.pop()
		if isinstance(p2, Constant) and p2.value == 0:
			stack.append(Constant(1))
		elif isinstance(p2, Constant) and p2.value == 1:
			stack.append(p1)
		else:
			stack.append(TwoOp.create(p1, "**", p2))
	elif c == 0x0b:  # SIGNEXTEND
		stack.append(FuncCall("SignExtend", [stack.pop(), stack.pop()]))
	elif c == 0x10:  # LT
		stack.append(TwoOp.create(stack.pop(), "<", stack.pop()))
	elif c == 0x11:  # GT
		stack.append(TwoOp.create(stack.pop(), ">", stack.pop()))
	elif c == 0x12:  # SLT
		stack.append(TwoOp.create(stack.pop(), "signed<", stack.pop()))
	elif c == 0x13:  # SGT
		stack.append(TwoOp.create(stack.pop(), "signed>", stack.pop()))	
	elif c == 0x14:  # EQ
		stack.append(TwoOp.create(stack.pop(), "==", stack.pop()))
	elif c == 0x15:  # ISZERO
		stack.append(OneOp.create("!", stack.pop()))
	elif c == 0x16:  # AND
		stack.append(TwoOp.create(stack.pop(), "&", stack.pop()))
	elif c == 0x17:  # OR
		stack.append(TwoOp.create(stack.pop(), "|", stack.pop()))
	elif c == 0x18:  # XOR
		stack.append(TwoOp.create(stack.pop(), "^", stack.pop()))
	elif c == 0x19:  # NOT
		stack.append(OneOp.create("~", stack.pop()))
	elif c == 0x1a:  # BYTE
		n = stack.pop()
		v = stack.pop()
		stack.append(ArrayIndex(v, n))
	elif c == 0x20:  # SHA3
		stack.append(FuncCall("keccak256", [stack.pop(), stack.pop()]))  # TODO: check arguments
	elif c == 0x30:  # ADDRESS
		stack.append(Constant("this"))
	elif c == 0x31:  # BALANCE
		stack.append(FuncCall("balance", [stack.pop()]))
	elif c == 0x32:  # ORIGIN
		stack.append(Constant("tx.origin"))
	elif c == 0x33:  # CALLER
		stack.append(Constant("msg.address"))
	elif c == 0x34:  # CALLVALUE
		stack.append(Constant("msg.value"))
	elif c == 0x35:  # CALLDATALOAD
		i = stack.pop()
		stack.append(ArrayIndexRangeCount("msg.data", i, 32))
	elif c == 0x36:  # CALLDATASIZE
		stack.append(FuncCall("sizeof", ["msg.data"]))
	elif c == 0x37:  # CALLDATACOPY
		memaddr = stack.pop()
		msgaddr = stack.pop()
		num = stack.pop()
		print(TwoOp.create(ArrayIndexRangeCount("memory", memaddr, num), "=", ArrayIndexRangeCount("msg.data", msgaddr, num)))
	elif c == 0x38:  # CODESIZE
		stack.append(FuncCall("sizeof", ["this.code"]))
	elif c == 0x39:  # CODECOPY
		memaddr = stack.pop()
		msgaddr = stack.pop()
		num = stack.pop()
		print(TwoOp.create(ArrayIndexRangeCount("memory", memaddr, num), "=", ArrayIndexRangeCount("this.code", msgaddr, num)))
	elif c == 0x3a:  # GASPRICE
		stack.append(FuncCall("gas_price", []))
	elif c == 0x3b:  # EXTCODESIZE
		stack.append(FuncCall("sizeof", [ObjectIndex(stack.pop(), "code")]))
	elif c == 0x39:  # EXTCODECOPY
		address = stack.pop()
		memaddr = stack.pop()
		msgaddr = stack.pop()
		num = stack.pop()
		print(TwoOp.create(ArrayIndexRangeCount("memory", memaddr, num), "=", ArrayIndexRangeCount(ObjectIndex(address, "code"), msgaddr, num)))
	elif c == 0x40:  # BLOCKHASH
		stack.append(FuncCall("blockhash", [TwoOp.create("block.index", "-", stack.pop())]))
	elif c == 0x41:  # COINBASE
		stack.append(ObjectIndex(stack.pop(), "beneficiary_address"))
	elif c == 0x42:  # TIMESTAMP
		stack.append(ObjectIndex(stack.pop(), "timestamp"))
	elif c == 0x43:  # NUMBER
		stack.append(ObjectIndex(stack.pop(), "number"))
	elif c == 0x44:  # DIFFICULTY
		stack.append(ObjectIndex(stack.pop(), "difficulty"))
	elif c == 0x45:  # GASLIMIT
		stack.append(ObjectIndex(stack.pop(), "gaslimit"))
	elif c == 0x50:  # POP
		stack.pop()
	elif c == 0x51:  # MLOAD
		i = stack.pop()
		stack.append(ArrayIndexRangeCount("memory", i, 32))
	elif c == 0x52:  # MSTORE
		i = stack.pop()
		v = stack.pop()
		print(TwoOp.create(ArrayIndexRangeCount("memory", i, 32), "=", v))
	elif c == 0x53:  # MSTORE8
		i = stack.pop()
		v = stack.pop()
		print(TwoOp.create(ArrayIndex("memory", i), "=", v))
	elif c == 0x54:  # SLOAD
		stack.append(ArrayIndex("storage", stack.pop()))
	elif c == 0x55:  # SSTORE
		print(TwoOp.create(ArrayIndex("storage", stack.pop()), "=", stack.pop()))
	elif c == 0x56:  # JUMP
		print(Goto(stack.pop()))
	elif c == 0x57:  # JUMPI
		print(GotoIf(stack.pop(), stack.pop()))
	elif c == 0x58:  # PC
		stack.append(pc)
	elif c == 0x59:  # MSIZE
		stack.append(FuncCall("sizeof", ["memory"]))
	elif c == 0x5a:  # GAS
		stack.append(FuncCall("gas_available", []))
	elif c == 0x5b:  # JUMPDEST
		print("loc_"+hex(pc)+":")
	elif c >= 0x60 and c <= 0x7f:  # PUSHn
		n = c - 0x60 + 1
		data = [0] * (32 - n) + list(prog_data[pc+1:pc+1+n])
		data = sum([c << 8*i for i,c in enumerate(reversed(data))])
		pc += n
		stack.append(Constant(data))
	elif c >= 0x80 and c <= 0x8f:  # DUPn
		n = c - 0x80 + 1
		stack.append(stack[-n])
	elif c >= 0x90 and c <= 0x9f:  # SWAPn
		n = c - 0x90 + 2
		stack[-1], stack[-n] = stack[-n], stack[-1]
	elif c >= 0xa0 and c <= 0xa4:  # LOGn
		n = c - 0xa0
		print("TODO: LOG "+(", ".join(map(str, [stack.pop() for _ in range(n+2)]))))
	elif c == 0xf0:  # CREATE
		value = stack.pop()
		input_offset = stack.pop()
		input_size = stack.pop()
		stack.append(FuncCall("create", [value, ArrayIndexRangeCount("memory", input_offset, input_size)]))
	elif c == 0xf1:  # CALL
		gas = stack.pop()
		to = stack.pop()
		value = stack.pop()
		in_off = stack.pop()
		in_size = stack.pop()
		out_off = stack.pop()
		out_size = stack.pop()
		stack.append(FuncCall("call", [
			gas, to, value,
			ArrayIndexRangeCount("memory", in_off, in_size),
			ArrayIndexRangeCount("memory", out_off, out_size),
		]))
	elif c == 0xf2:  # CALLCODE
		gas = stack.pop()
		to = stack.pop()
		value = stack.pop()
		in_off = stack.pop()
		in_size = stack.pop()
		out_off = stack.pop()
		out_size = stack.pop()
		stack.append(FuncCall("callcode", [
			gas, to, value,
			ArrayIndexRangeCount("memory", in_off, in_size),
			ArrayIndexRangeCount("memory", out_off, out_size),
		]))
	elif c == 0xf3:  # RETURN
		inp = stack.pop()
		siz = stack.pop()
		print(FuncCall("return", [
			ArrayIndexRangeCount("memory", inp, siz)
		]))
	elif c == 0xf4:  # DELEGATECALL
		gas = stack.pop()
		to = stack.pop()
		in_off = stack.pop()
		in_size = stack.pop()
		out_off = stack.pop()
		out_size = stack.pop()
		stack.append(FuncCall("delegatecall", [
			gas, value,
			ArrayIndexRangeCount("memory", in_off, in_size),
			ArrayIndexRangeCount("memory", out_off, out_size),
		]))
	elif c == 0xf5:  # CALLBACKBOX TODO
		gas = stack.pop()
		to = stack.pop()
		value = stack.pop()
		in_off = stack.pop()
		in_size = stack.pop()
		out_off = stack.pop()
		out_size = stack.pop()
		stack.append(FuncCall("callblackbox", [
			gas, to, value,
			ArrayIndexRangeCount("memory", in_off, in_size),
			ArrayIndexRangeCount("memory", out_off, out_size),
		]))
	elif c == 0xf6:  # STATICCALL TODO
		gas = stack.pop()
		value = stack.pop()
		in_off = stack.pop()
		in_size = stack.pop()
		out_off = stack.pop()
		out_size = stack.pop()
		stack.append(FuncCall("staticcall", [
			gas, value,
			ArrayIndexRangeCount("memory", in_off, in_size),
			ArrayIndexRangeCount("memory", out_off, out_size),
		]))
	elif c == 0xfd:  # REVERT TODO
		print(FuncCall("revert", [
			stack.pop(), stack.pop()
		]))
	elif c == 0xff:  # SUICIDE
		newacct = stack.pop()
		print(FuncCall("suicide", [newacct]))
	else:
		print("TODO: "+hex(c))
	if DEBUG:
		print("\033[0;30m"+"        ", stack, "\033[0m")
	stack_end = len(stack)
	if c in opcodes:
		assert stack_end - stack_start == opcodes[c][2] - opcodes[c][1]
	pc += 1

print(stack)
