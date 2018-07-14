Ethereum EVM decompiler
=======================

This is my attempt to write a decompiler for Ethereum Virtual Machine. This project is on a very early stage and has a lot of bugs, but it Sometimes Works(TM). The output it generates is still hard to read but it's already more readable than bytecode.

I plan to improve it later if I have some time

Example
-------

Original contract:
```solidity
pragma solidity ^0.4.0;
contract Test {
    uint256 i = 0;
    
    function() payable public {
        i++;
    }
    
    function testfunc() payable public {
        i--;
    }
}
```

Decompiled:
```
(memory[0x40:+32] = 0x80)
if((sizeof(msg.data) < 0x4)) goto loc_0x3e
if((((msg.data[0x0:+32] / 0x100000000000000000000000000000000000000000000000000000000) & 0xffffffff) == 0xb39dbc6)) goto loc_0x49
loc_0x3e:
(storage[0x0] = (0x1 + storage[0x0]))
exit()
loc_0x49:
goto loc_0x51
loc_0x4f:
exit()
loc_0x51:
(storage[0x0] = (storage[0x0] - 0x1))
goto loc_0x4f
exit()
```

Raw disassembly:
```
loc_00000000:
0x00000000 60 80                      PUSH1 80 
0x00000002 60 40                      PUSH1 40 
0x00000004 52                         MSTORE 
0x00000005 60 04                      PUSH1 04 
0x00000007 36                         CALLDATASIZE 
0x00000008 10                         LT 
0x00000009 60 3e                      PUSH1 3e 
0x0000000b 57                         JUMPI 

loc_0000000c:
0x0000000c 63 ff  ff  ff  ff          PUSH4 ff ff ff ff 
0x00000011 7c 00  00  00  00  +      PUSH29 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 01 
0x0000002f 60 00                      PUSH1 00 
0x00000031 35                         CALLDATALOAD 
0x00000032 04                         DIV 
0x00000033 16                         AND 
0x00000034 63 c6  db  39  0b          PUSH4 c6 db 39 0b 
0x00000039 81                         DUP2 
0x0000003a 14                         EQ 
0x0000003b 60 49                      PUSH1 49 
0x0000003d 57                         JUMPI 

loc_0000003e:
0x0000003e 5b                         JUMPDEST 
0x0000003f 60 00                      PUSH1 00 
0x00000041 80                         DUP1 
0x00000042 54                         SLOAD 
0x00000043 60 01                      PUSH1 01 
0x00000045 01                         ADD 
0x00000046 90                         SWAP1 
0x00000047 55                         SSTORE 
0x00000048 00                         STOP 

func_0b39dbc6:
0x00000049 5b                         JUMPDEST 
0x0000004a 60 4f                      PUSH1 4f 
0x0000004c 60 51                      PUSH1 51 
0x0000004e 56                         JUMP 

loc_0000004f:
0x0000004f 5b                         JUMPDEST 
0x00000050 00                         STOP 

loc_00000051:
0x00000051 5b                         JUMPDEST 
0x00000052 60 00                      PUSH1 00 
0x00000054 80                         DUP1 
0x00000055 54                         SLOAD 
0x00000056 60 01                      PUSH1 01 
0x00000058 90                         SWAP1 
0x00000059 03                         SUB 
0x0000005a 90                         SWAP1 
0x0000005b 55                         SSTORE 
0x0000005c 56                         JUMP 
0x0000005d 00                         STOP 
0x0000005e a1                         LOG1 
0x0000005f 65 58  30  72  7a  +      PUSH6 58 30 72 7a 7a 62 
0x00000066 20                         SHA3
```
