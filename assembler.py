from sys import stdin
"""code = []
for i in range(5) :
    l = input()
    code.append(l)"""

instructions=[]

#create a list of flags
flags=[False]*4

#create a dictionary of opcodes

opcodes={
    "add" : "10000",
    "sub" : "10001",
    "movI": "10010",
    "movR": "10011",
    "ld"  : "10100",
    "st"  : "10101",
    "mul" : "10110",
    "div" : "10111",
    "rs"  : "11000",
    "ls"  : "11001",
    "xor" : "11010",
    "or"  : "11011",
    "and" : "11100",
    "not" : "11101",
    "cmp" : "11110",
    "jmp" : "11111",
    "jlt" : "01100",
    "jgt" : "01101",
    "je"  : "01111",
    "hlt" : "01010",
}

#create a dictionary of registers
register={
    "R0": "000",
    "R1": "001",
    "R2": "010",
    "R3": "011",
    "R4": "100",
    "R5": "101",
    "R6": "110",
    "FLAGS": "111",
}

#create a dictionary for stored registers

StoredRegisters = {
    "R0": 0,
    "R1": 0,
    "R2": 0,
    "R3": 0,
    "R4": 0,
    "R5": 0,
    "R6": 0,
    "FLAGS": 0,
}

#create a dictionary for variables

VAR={}

#create a dictionary for stored variables
StoredVars={}

# create a dictionary for label
labels={}

def convertToDecimal(Bstr):
    num=list(Bstr)
    ans=0
    n=len(num)
    i=0
    while(i!=n):
        if num[n-i-1]=='1':
            ans+=2**i
            i+=1
        else:
            i+=1
            continue
    return ans

def convertToBin(num, bits):
    if num==0:
        return "0" * bits
    else:
        ans=""
        while(num>1):
            solpart=str(num%2)
            ans+=solpart
            num=int(num/2)
    ans="1"+ans

    leftBits= bits - len(ans)
    if (leftBits>0):
        padd="0"* leftBits
        ans=padd+ans
    return ans

def decToBinary(n):
    x=bin(n)
    x=x.replace("0b", "")

    ans=int(x)
    return x

def ErrorA(inst, line):

    if len(inst) != 4:
        raise Exception(f"TypeA instruction requires 3 operands! Error in line {line + 1}")

    op = inst[0]
    Reg1 = inst[1]
    Reg2 = inst[2]
    resultReg = inst[3]

    if (Reg1 not in StoredRegisters.keys()) or (Reg2 not in StoredRegisters.keys()) or (resultReg not in StoredRegisters.keys()):
        raise Exception(f"Invalid register! Error in line {line + 1}.")

    if "FLAGS" in inst :
        raise Exception(f"FLAG register can not be used to store bits in typeA instruction! Error in line {line + 1}.")

    return True

def ErrorB(inst, line):

    if len(inst) != 3:
        raise Exception(f"TypeB instruction requires 2 commands! Error in line {line + 1}")

    op = inst[0]
    reg1 = inst[1]
    value = inst[2]

    if (reg1 not in StoredRegisters.keys()):
        raise Exception(f"Invalid register! Error in line {line + 1}.")

    if value[0] == "$":
        imm = int(value[1:])
        if ((imm > 255) or (imm < 0)) :
            raise Exception (f"Memory Overload! Error in line {line + 1}")

    else :
        raise Exception(f"Syntax Error! Error in line {line + 1}")
    
    return True

def ErrorC(inst, line) :

    if len(inst) != 3:
        raise Exception(f"TypeC instruction requires 2 commands! Error in line {line + 1}")

    op = inst[0]
    reg1 = inst[1]
    reg2 = inst[2]

    if (reg1 not in StoredRegisters.keys()) or (reg2 not in StoredRegisters.keys()):
        raise Exception(f"Invalid register! Error in line {line + 1}.")

    return True

def errorD(inst, line) :

    if len(inst) != 3:
        raise Exception(f"TypeD instruction requires 2 commands! Error in line {line + 1}")

    op = inst[0]
    reg1 = inst[1]
    mem = inst[2]

    if reg1 not in StoredRegisters.keys() :
        raise Exception(f"Invalid Register! Error in line {line + 1}")

    if mem not in StoredVars.keys() :
        raise Exception(f"Undeclared variable used! Error in line {line + 1}")

    if mem in labels.keys() :
        raise Exception(f"Label used in place of variable! Error in line {line + 1}")

    return True

def errorE(inst, line) :

    if len(inst) != 2:
        raise Exception(f"TypeD instruction requires 1 command! Error in line {line + 1}")

    op = inst[0]
    mem = inst[1]

    if mem not in labels.keys() :
        raise Exception(f"Label not declared! Error in line {line + 1}")

    if mem in StoredVars.keys() :
        raise Exception(f"Cannot use Variables in this instruction! Error in line {line + 1}")

    return True


def typeA (inst, line):

    result = ""

    if len(inst) != 4:
        raise Exception(f"TypeA instruction requires 3 operands! Error in line {line}")

    op = inst[0]
    Reg1 = inst[1]
    Reg2 = inst[2]
    resultReg = inst[3]

    result += opcodes[op] + "00"

    if (Reg1 not in StoredRegisters.keys()) or (Reg2 not in StoredRegisters.keys()) or (resultReg not in StoredRegisters.keys()):
        raise Exception(f"Invalid register! Error in line {line}.")

    if "FLAGS" in inst :
        raise Exception(f"FLAG register can not be used to store bits in typeA instruction! Error in line {line}.")

    result = result + register[Reg1] + register[Reg2] + register[resultReg]

    return result


def typeB(inst, line):

    result = ""

    if len(inst) != 3:
        raise Exception(f"TypeB instruction requires 2 commands! Error in line {line}")

    op = inst[0]
    reg1 = inst[1]
    value = inst[2]

    if (reg1 not in StoredRegisters.keys()):
        raise Exception(f"Invalid register! Error in line {line}.")

    result += opcodes[op] + register[reg1]

    if value[0] == "$":
        imm = int(value[1:])
        if ((imm > 255) or (imm < 0)) :
            raise Exception (f"Memory Overload! Error in line {line}")

        else :
            imm = convertToBin(imm, 8)
            result += imm
            return result

    else :
        raise Exception(f"Syntax Error! Error in line {line}")


def typeC (inst, line) :

    result = ""

    if len(inst) != 3:
        raise Exception(f"TypeC instruction requires 2 commands! Error in line {line}")

    op = inst[0]
    reg1 = inst[1]
    reg2 = inst[2]

    if (reg1 not in StoredRegisters.keys()) or (reg2 not in StoredRegisters.keys()):
        raise Exception(f"Invalid register! Error in line {line}.")

    result += opcodes[op]
    result += "00000"
    result += register[reg1] + register[reg2]

    return result

def typeD (inst, line) :

    result = ""

    if len(inst) != 3:
        raise Exception(f"TypeD instruction requires 2 commands! Error in line {line}")

    op = inst[0]
    reg1 = inst[1]
    mem = inst[2]

    if reg1 not in StoredRegisters.keys() :
        raise Exception(f"Invalid Register! Error in line {line}")

    if mem not in StoredVars.keys() :
        raise Exception(f"Undeclared variable used! Error in line {line}")

    if mem in labels.keys() :
        raise Exception(f"Label used in place of variable! Error in line {line}")

    result += opcodes[op] + register[reg1] + StoredVars[mem]
    return result

def typeE (inst, line) :

    result = ""

    if len(inst) != 2:
        raise Exception(f"TypeD instruction requires 1 command! Error in line {line}")

    op = inst[0]
    mem = inst[1]

    if mem not in labels.keys() :
        raise Exception(f"Label not declared! Error in line {line}")

    if mem in StoredVars.keys() :
        raise Exception(f"Cannot use Variables in this instruction! Error in line {line}")

    result += opcodes[op] + "000" + labels[mem]

    return result

def typeF () :

    result = "01010"
    x = "0" * 11
    result += x
    return result

result = []
lineNo = 0
halt = False
varDef = False
error = False

for line in stdin:
#for line in code:

    inst = line.split()
    if line != "" :

#handling errors
        if halt == True :
            raise Exception(f"Halt should be last instruction! Error in line {lineNo}")

        if len(instructions) > 256 :
            raise Exception(f"Memory Overflow! Error in line {lineNo}")

        if ((inst[0] != "var") and (varDef == False)) :
            varDef = True

        elif ((inst[0] == "var") and (varDef == True)):
            raise Exception(f"Variable should be defined in the begining! Error in line {lineNo}")


#handling labels
        if ":" in line: 
            lIndex = line.index(":")

            if " " in line[0:lIndex] :
                raise Exception(f"Space between label and colon! Error in line {lineNo}")

            name = line[0:lIndex]

            if name in labels.keys() :
                raise Exception(f"Illegal naming of label! Label name already exists. Error in line {lineNo}")
            
            if name in StoredRegisters.keys() :
                raise Exception(f"Illegal naming of label! Can not use register names. Error in line lineNo{lineNo}")

            labels[name] = convertToBin(lineNo+1, 8)
            inst = inst[1:]
            instructions.append(inst)
            lineNo += 1
            continue


# handling variables
        if inst[0] == "var" and varDef == False :

            if len(inst) > 2 :
                raise Exception("Illegal Variable Naming! Error in line {lineNo}")
            
            if inst[1] in StoredVars.keys():
                raise Exception(f"Illegal naming of label! Variable name already exists. Error in line {lineNo}")

            if inst[1] in StoredRegisters.keys() :
                raise Exception(f"Illegal naming of label! Variable name cannot be registers. Error in line {lineNo}")

            StoredVars[inst[1]] = "0"
            continue


# handling instructions
        if inst[0] in opcodes.keys():

            instructions.append(inst)
            lineNo += 1

            Op = inst[0]

            if (
                Op == "add" or
                Op == "sub" or
                Op == "mul" or
                Op == "xor" or
                Op == "or" or
                Op == "and" ):
                if ErrorA(inst, lineNo):
                    continue
            elif Op == "mov":

                if "$" in i[-1] and ErrorB(inst, lineNo):
                    continue

                elif "$" not in i[-1] and ErrorC(inst, lineNo):
                    continue
                    
            elif (Op == "rs" or Op == "ls") :
                if ErrorB(inst, lineNo):
                    continue

            elif (Op == "div" or Op == "not" or Op == "cmp") :
                if ErrorC(inst, lineNo):
                    continue

            elif (Op == "ld" or Op == "st") :
                if ErrorD(inst, lineNo):
                    continue

            elif (Op == "jmp" or Op == "jlt" or Op == "jgt" or Op == "je"):
                if ErrorE(inst, lineNo):
                    continue

        else:
            raise Exception(f"Invalid Syntax Error in line {lineNo + 1}")


n = len(StoredVars)
x = 1

for key in StoredVars.keys() :
    StoredVars[key] = convertToBin(lineNo + x, 8)
    x += 1

lines = n + lineNo

if instructions[-1] != ["hlt"]:
    raise Exception("Mising or Improper use of Hlt")

for i in range(lineNo) :

    ins= instructions[i]
    Op = ins[0]

    if (
        Op == "add" or
        Op == "sub" or
        Op == "mul" or
        Op == "xor" or
        Op == "or" or
        Op == "and" ):

        result.append(typeA(ins, i + n))

    elif Op == "mov":

        if "$" in i[-1]:
            result.append(typeB(ins, i + n))

        else:
            result.append(typeC(ins, i + n))

    elif (Op == "rs" or Op == "ls") :
        result.append(typeB(ins, i + n))

    elif (Op == "div" or Op == "not" or Op == "cmp") :
        result.append(typeC(ins, i + n))

    elif (Op == "ld" or Op == "st") :
        result.append(typeD(ins, i + n))

    elif (Op == "jmp" or Op == "jlt" or Op == "jgt" or Op == "je"):
        result.append(typeE(ins, i + n))

    elif Op == "hlt" :
        result.append(typeF())

    else:
        raise Exception("Invalid Operation Code! Error in line {line}")



for i in result :
    print(i)
