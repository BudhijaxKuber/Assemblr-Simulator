from sys import stdin

pc = 0
memory = []

registers = {
    "000": 0,
    "001": 0,
    "010": 0,
    "011": 0,
    "100": 0,
    "101": 0,
    "110": 0,
    "111": 0,
}

opcodes = {
    "11010": "xor",
    "11011": "or",
    "11100": "and",
    "11101": "not",
    "11110": "cmp",
    "11111": "jmp",
    "01100": "jlt",
    "01101": "jgt",
    "01111": "je",
    "01010": "hlt",
    "10000": "add",
    "10001": "sub",
    "10010": "movI",
    "10011": "movR",
    "10100": "ld",
    "10101": "st",
    "10110": "mul",
    "10111": "div",
    "11000": "rs",
    "11001": "ls",
    "00000": "addf",
    "00001": "subf",
    "00010": "movf",
} 
def flag_reset():
    registers["111"]=0

def pcReg(pc):
    print(pc, end=" ")
    for i in registers.values():
        print(convertToBin(i, 16), end=" ")
    print()

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

def memory_dump(mem):
    
    for m in range(len(mem)):
        print(mem[m])

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

def TypeA(i):
    
    opcode = i[0:5]
    dest_reg = i[13:]
    reg1 = i[10:13]
    reg2 = i[7:10]
    op1 = registers[reg1]
    op2 = registers[reg2]

    if(opcodes[opcode] == "add"):

        flag_reset()

        result = op1 + op2
        resInBin = convertToBin(result, 16)
        if len(resInBin) > 16:
            resInBin = resInBin[-16:]
            registers["111"] = 8
            result = convertToDecimal(resInBin)

    elif(opcodes[opcode] == "xor"):

        flag_reset()

        result = op1 ^ op2

    elif(opcodes[opcode] == "or"):

        flag_reset()

        result = op1 | op2

    elif(opcodes[opcode] == "sub"):

        flag_reset()

        result = op1 - op2
        if (result < 0):
            result = 0
            registers["111"] = 8

    elif(opcodes[opcode] == "mul"):

        flag_reset()

        result = op1 * op2
        resInBin = convertToBin(result, 16)
        if len(resInBin) > 16:
            resInBin = resInBin[-16:]
            registers["111"] = 8
            result = convertToDecimal(resInBin)

    elif(opcodes[opcode] == "and"):

        flag_reset()

        result = op1 & op2
    registers[dest_reg] = result


def TypeB(i):
    
    opcode = i[0:5]
    reg = i[5:8]
    immediate = convertToDecimal(i[8:])
    toShift = convertToBin(registers[reg], 16)
    shiftBy = "0"*immediate
    if (opcodes[opcode] == "movI"):

        flag_reset()
        registers[reg] = immediate


    elif (opcodes[opcode] == "rs"):

        flag_reset()
        result = shiftBy + toShift
        result = result[0:16]
        registers[reg] = convertToDecimal(result)


    elif (opcodes[opcode] == "ls"):

        flag_reset()
        result = toShift + shiftBy
        result = result[-16:]
        registers[reg] = convertToDecimal(result)

def TypeC(i, curr):
  
    opcode = i[0:5]
    reg1 = i[10:13]
    reg2 = i[13:]
    if (opcodes[opcode] == "cmp"):

        flag_reset()
        val1 = registers[reg1]
        val2 = registers[reg2]
        if (val1 > val2):

            registers["111"] = 2
        elif (val1 < val2):
            registers["111"] = 4
        else:
            registers["111"] = 1

    elif (opcodes[opcode] == "not"):

        flag_reset()
        noToFlip = convertToBin(registers[reg2], 16)

        inverting = ""
        for ch in range(len(noToFlip)):
            if(noToFlip[ch] == "1"):
                inverting = inverting + "0"
            else:
                inverting = inverting + "1"

        flippedNo = convertToDecimal(inverting)

        registers[reg1] = flippedNo

    elif (opcodes[opcode] == "movR"):

        flag_reset()
        if(reg2 == "111"):
            registers[reg1] = curr
            return
        registers[reg2] = registers[reg1]

    elif (opcodes[opcode] == "div"):

        flag_reset()
        quotient = (registers[reg1]) // (registers[reg2])
        remainder = registers[reg1] % registers[reg2]
        registers["000"] = quotient
        registers["001"] = remainder


def TypeD(i):
   
    opcode = i[0:5]
    reg = i[5:8]
    location = convertToDecimal(i[8:])
    valueToStore = registers[reg]
    valueToLoad = convertToDecimal(memory[location])

    if(opcodes[opcode] == "st"):

        flag_reset()
        memory[location] = convertToBin(valueToStore, 16)

    elif(opcodes[opcode] == "ld"):

        flag_reset()
        registers[reg] = valueToLoad


def TypeE(i, curr, progc):
   
    opcode = i[0:5]
    location = convertToDecimal(i[8:])
    if(opcodes[opcode] == "jmp"):
        progc = location

        flag_reset()

    elif (opcodes[opcode] == "jlt"):
        if(curr == 4):
            progc = location
        else:
            progc += 1

        flag_reset()
    elif (opcodes[opcode] == "je"):
        if(curr == 1):
            progc = location
        else:
            progc += 1

        flag_reset()

    elif (opcodes[opcode] == "jgt"):
        if(curr == 2):
            progc = location
        else:
            progc += 1

        flag_reset()

    return progc


x = []
y = []


for line in stdin:

    line = line.strip()

    if(line == ""):
        continue

    if line == "s":
        memory.append("1001100000000000")
        break
    memory.append(line)

while(len(memory) < 256):
    memory.append(convertToBin(0, 16))

cycleNo = 0

stopCode = False
while(pc < len(memory)):

    if stopCode:
        break

    x.append(cycleNo)
    y.append(pc)
    cycleNo += 1

    pcPr = convertToBin(pc, 8)

    
    currR = registers["111"]
    
    currR = registers["111"]
    
    registers["111"] = 0

  
    op = memory[pc][0:5]

    if(opcodes[op] == "hlt"):
        flag_reset()
        stopCode = True

    if((opcodes[op] == "sub") or (opcodes[op] == "add") or (opcodes[op] == "mul") or (opcodes[op] == "xor") or (opcodes[op] == "or") or (opcodes[op] == "and")):
        TypeA(memory[pc])

    elif ((opcodes[op] == "cmp") or (opcodes[op] == "movR") or (opcodes[op] == "div") or (opcodes[op] == "not")):
        TypeC(memory[pc], currR)

    elif((opcodes[op] == "movI") or (opcodes[op] == "ls") or (opcodes[op] == "rs")):

        TypeB(memory[pc])

    elif((opcodes[op] == "ld") or (opcodes[op] == "st")):
        cycleNo -= 1
        x.append(cycleNo)
        y.append(convertToDecimal(memory[pc][-8:]))
        cycleNo += 1
        TypeD(memory[pc])

    elif((opcodes[op] == "jmp") or (opcodes[op] == "jgt") or (opcodes[op] == "jlt") or (opcodes[op] == "je")):
        pc = TypeE(memory[pc], currR, pc)
        pcReg(pcPr)
        continue

    pcReg(pcPr)

    pc += 1


memory_dump(memory)
