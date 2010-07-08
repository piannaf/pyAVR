'''Copyright (c) 2010, Justin Mancinelli
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
    * Neither the name of the <organization> nor the
      names of its contributors may be used to endorse or promote products
      derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

'''

class InvalidInstruction(Exception):
    def __init__(self, expr, msg):
        self.expr = expr
        self.msg = msg

class ISA:
    """Instruction set architecture of the AVR8515
    
    This includes a list of available instructions, and the ability to convert
    an instruction into its opcode
    
    """
    _instructions = {"ADC": "0001 11%c%c %s %s",
                    "ADD":  "0000 11%c%c %s %s",
                    "ADIW": "1001 0110 %s%s %s",
                    "AND":  "0010 00%c%c %s %s",
                    "ANDI": "0111 %s %s %s",
                    "ASR":  "1001 010%c %s 0101",
                    "BCLR": "1001 0100 1%s 1000",
                    "BLD":  "1111 100%c %s 0%s",
                    "BRBC": "1111 01%s %s %c%s",
                    "BRBS": "1111 00%s %s %c%s",
                    "BRCC": "1111 01%s %s %c000",
                    "BRCS": "1111 00%s %s %c000",
                    "BREQ": "1111 00%s %s %c001",
                    "BRGE": "1111 01%s %s %c100",
                    "BRHC": "1111 01%s %s %c101",
                    "BRHS": "1111 00%s %s %c000",
                    "BRID": "1111 01%s %s %c111",
                    "BRIE": "1111 00%s %s %c111",
                    "BRLO": "1111 00%s %s %c000",
                    "BRLT": "1111 00%s %s %c100",
                    "BRMI": "1111 00%s %s %c010",
                    "BRNE": "1111 01%s %s %c001",
                    "BRPL": "1111 01%s %s %c010",
                    "BRSH": "1111 01%s %s %c000",
                    "BRTC": "1111 01%s %s %c110",
                    "BRTS": "1111 00%s %s %c110",
                    "BRVC": "1111 01%s %s %c011",
                    "BRVS": "1111 00%s %s %c000",
                    "BSET": "1001 0100 0%s 1000",
                    "BST":  "1111 101%c %s 0%s",
                    "CBI":  "1001 1000 %s %c%s",
                    "CBR":  "0111 %s %s %s",    # First take compliment of K
                    "CLC":  "1001 0100 1000 1000",
                    "CLH":  "1001 0100 1101 1000",
                    "CLI":  "1001 0100 1111 1000",
                    "CLN":  "1001 0100 1010 1000",
                    "CLR":  "0010 01%c%c %s %s",    # DDDDD=ddddd
                    "CLS":  "1001 0100 1100 1000",
                    "CLT":  "1001 0100 1110 1000",
                    "CLV":  "1001 0100 1011 1000",
                    "CLZ":  "1001 0100 1001 1000",
                    "COM":  "1001 010%c %s 0000",
                    "CP":   "0001 01%c%c %s %s",
                    "CPC":  "0000 01%c%c %s %s",
                    "CPI":  "0011 %s %s %s",
                    "CPSE": "0001 00%c%c %s %s",
                    "DEC":  "1001 010%c %s 1010",
                    "EOR":  "0010 01%c%c %s %s",
                    "ICALL":"1001 0101 0000 1001",
                    "IJMP": "1001 0100 0000 1001",
                    "IN":   "1011 0%s%c %s %s",
                    "INC":  "1001 010%c %s 0011",
                    "LD":   "1000 000%c %s %s%s", # several cases here
                    "LDD":  "10%c0 %s0%c %s %c%s",
                    "LDI":  "1110 %s %s %s",
                    "LDS":  "1001 000%c %s 0000\n%s %s %s %s",
                    "LPM":  "1001 0101 1100 1000",
                    "LSL":  "0000 11%c%c %s %s",    # DDDDD=ddddd
                    "LSR":  "1001 010%c %s 0110",
                    "MOV":  "0010 11%c%c %s %s",
                    "NEG":  "1001 010%c %s 0001",
                    "NOP":  "0000 0000 0000 0000",
                    "OR":   "0010 10%c%c %s %s",
                    "ORI":  "0110 %s %s %s",
                    "OUT":  "1011 1%s%c %s %s",
                    "POP":  "1001 000%c %s 1111",
                    "PUSH": "1001 001%c %s 1111",
                    "RCALL":"1101 %s %s %s",
                    "RET":  "1001 0101 0000 1000",
                    "RETI": "1001 0101 0001 1000",
                    "RJMP": "1100 %s %s %s",
                    "ROL":  "0001 11%c%c %s %s",    # DDDDD=ddddd
                    "ROR":  "1001 010%c %s 0111",
                    "SBC":  "0000 10%c%c %s %s",
                    "SBCI": "0100 %s %s %s",
                    "SBI":  "1001 1010 %s %c%s",
                    "SBIC": "1001 1001 %s %c%s",
                    "SBIS": "1001 1011 %s %c%s",
                    "SBIW": "1001 0111 %s%s %s",
                    "SBR":  "0110 %s %s %s",
                    "SBRC": "1111 110%c %s 0%s",
                    "SBRS": "1111 111%c %s 0%s",
                    "SEC":  "1001 0100 0000 1000",
                    "SEH":  "1001 0100 0101 1000",
                    "SEI":  "1001 0100 0111 1000",
                    "SEN":  "1001 0100 0010 1000",
                    "SER":  "1110 1111 %s 1111",
                    "SES":  "1001 0100 0100 1000",
                    "SET":  "1001 0100 0110 1000",
                    "SEV":  "1001 0100 0011 1000",
                    "SEZ":  "1001 0100 0001 1000",
                    "SLEEP":"1001 0101 1000 1000",
                    "ST":   "100%c 001%c %s %s%s", # several cases here
                    "STD":  "10%c0 %s1%c %s %c%s",
                    "STS":  "1001 001%c %s 0000\n%s %s %s %s",
                    "SUB":  "0001 10%c%c %s %s",
                    "SUBI": "0101 %s %s %s",
                    "SWAP": "1001 010%c %s 0010",
                    "TST":  "0010 00%c%c %s %s",    # DDDDD=ddddd
                    "WDR":  "1001 0101 1010 1000"}
    _gp_registers = ("r0",
                  "r1",
                  "r2",
                  "r3",
                  "r4",
                  "r5",
                  "r6",
                  "r7",
                  "r8",
                  "r9",
                  "r10",
                  "r11",
                  "r12",
                  "r13",
                  "r14",
                  "r15",
                  "r16",
                  "r17",
                  "r18",
                  "r19",
                  "r20",
                  "r21",
                  "r22",
                  "r23",
                  "r24",
                  "r25",
                  "r26",
                  "r27",
                  "r28",
                  "r29",
                  "r30",
                  "r31")
    _io_registers = ()  # TODO
    
    def __init__(self):
        self.instructions = [instruction for instruction in
                   [method[1:].upper() for method in dir(self) if
                    hasattr(getattr(self, method), '__call__')] if
               instruction in ISA._instructions.keys()]

        self._instruction_mapping = {}
        for i in self.instructions:
            self._instruction_mapping[i] = getattr(self, "_%s" % i.lower())

        self._gp_register_mapping = {}
        for r in ISA._gp_registers:
            self._gp_register_mapping[r] = self._integer_to_padded_binary(
                int(r[1:]))
                
        self._rhrl_mapping = {"r25:r24": "00", 
                              "r27:r26": "01", 
                              "r29:r28": "10",
                              "r31:r30": "11",
                              "XH:XL": "01",
                              "YH:YL": "10",
                              "ZH:ZL": "11"}

    def _integer_to_padded_binary(self, i, b = 8):
        """Convert an integer to a 0-padded binary string
        where b is the minimum number of bits (default is 8).

        """
        s = bin(i)[2:]
        return ''.join(['0'] *  (b - len(s)) + list(s))

    def _adc(self, rd, rr):
        """Add two registers with carry"""
        try:
            rdCode, rrCode = self._gp_register_mapping[rd], \
                             self._gp_register_mapping[rr]
        except KeyError:
            return None
        
        return ISA._instructions["ADC"] % (rdCode[-5], rrCode[-5], rdCode[-4:],
                                     rrCode[-4:])
                                     
    def _add(self, rd, rr):
        """Add to registers"""
        try:
            rdCode, rrCode = self._gp_register_mapping[rd], \
                             self._gp_register_mapping[rr]
        except KeyError:
            return None
        
        return ISA._instructions["ADD"] % (rdCode[-5], rrCode[-5], rdCode[-4:],
                                     rrCode[-4:])

    def _adiw(self, rhrl, k):
        """Add immidiate to Word (0 <= K <= 63)"""
        try:
            dd = self._rhrl_mapping[rhrl]
        except KeyError:
            return None
        
        if k < 0 or k > 63:
            return None
            
        try:
            kCode = self._integer_to_padded_binary(int(k))
        except ValueError:
            return None
            
        return ISA._instructions["ADIW"] % (kCode[-6:-4], dd, kCode[-4:])

    def _and(self, rd, rr):
        """Logical AND two registers"""
        try:
            rdCode, rrCode = self._gp_register_mapping[rd], \
                             self._gp_register_mapping[rr]
        except KeyError:
            return None
        
        return ISA._instructions["AND"] % (rdCode[-5], rrCode[-5], rdCode[-4:],
                                     rrCode[-4:])

    def _andi(self, rd, k):
        """Logical AND with immediate (16 <= d <= 31)"""
        try:
            rdCode = self._gp_register_mapping[rd]
        except KeyError:
            return None
        
        if '1' not in rdCode[0:4]:  # checks rd >= r16
            return None
        
        k = self._integer_to_padded_binary(k)
        return ISA._instructions["ANDI"] % (k[0:4], rdCode[-4:], k[4:])

    def _asr(self, rd):
        """Arithmetic shift right"""
        try:
            rdCode = self._gp_register_mapping[rd]
        except KeyError:
            return None
        
        return ISA._instructions["ASR"] % (rdCode[-5], rdCode[-4:])

    def _bclr(self, s):
        """Clear bit in status register"""
        if not 0 <= s <= 7:
            return None
        
        s = self._integer_to_padded_binary(s)
        return ISA._instructions["BCLR"] % (s[-3:])
        
    def _bld(self, rd, b):
        """Load bit in register from T"""
        try:
            rdCode = self._gp_register_mapping[rd]
        except KeyError:
            return None
        
        if not 0 <= b <= 7:
            return None
        
        b = self._integer_to_padded_binary(b)
        return ISA._instructions["BLD"] % (rdCode[-5], rdCode[-4:], b[-3:])

    def _brbc(self, s, k):
        """Branch if status register flag cleared"""
        if not 0 <= s <= 7:
            return None
        
        s = self._integer_to_padded_binary(s)
        k = self._integer_to_padded_binary(k)
        return ISA._instructions["BRBC"] % (k[-7:-5], k[-5:-1], k[-1], s[-3:])

    def _brbs(self, s, k):
        """Branch if status register flag set"""
        if not 0 <= s <= 7:
            return None
        
        s = self._integer_to_padded_binary(s)
        k = self._integer_to_padded_binary(k)
        return ISA._instructions["BRBS"] % (k[-7:-5], k[-5:-1], k[-1], s[-3:])

    def _brcc(self, k):
        """Branch if carry cleared"""
        k = self._integer_to_padded_binary(k)
        return ISA._instructions["BRCC"] % (k[-7:-5], k[-5:-1], k[-1])

    def _brcs(self, k):
        """Branch if carry set"""
        k = self._integer_to_padded_binary(k)
        return ISA._instructions["BRCS"] % (k[-7:-5], k[-5:-1], k[-1])

    def _breq(self, k):
        """Branch if equal"""
        k = self._integer_to_padded_binary(k)
        return ISA._instructions["BREQ"] % (k[-7:-5], k[-5:-1], k[-1])

    def _brge(self, k):
        """Branch if greater or equal (signed)"""
        k = self._integer_to_padded_binary(k)
        return ISA._instructions["BRGE"] % (k[-7:-5], k[-5:-1], k[-1])

    def _brhc(self, k):
        """Branch if half-carry flag cleared"""
        k = self._integer_to_padded_binary(k)
        return ISA._instructions["BRHC"] % (k[-7:-5], k[-5:-1], k[-1])

    def _brhs(self, k):
        """Branch if half-carry flag set"""
        k = self._integer_to_padded_binary(k)
        return ISA._instructions["BRHS"] % (k[-7:-5], k[-5:-1], k[-1])

    def _brid(self, k):
        """Branch if interrupt disabled"""
        k = self._integer_to_padded_binary(k)
        return ISA._instructions["BRID"] % (k[-7:-5], k[-5:-1], k[-1])
    
    def _brie(self, k):
        """Branch if interrupt enabled"""
        k = self._integer_to_padded_binary(k)
        return ISA._instructions["BRIE"] % (k[-7:-5], k[-5:-1], k[-1])

    def _brlo(self, k):
        """Branch if lower (unsigned)"""
        k = self._integer_to_padded_binary(k)
        return ISA._instructions["BRLO"] % (k[-7:-5], k[-5:-1], k[-1])

    def _brlt(self, k):
        """Branch if less than (signed)"""
        k = self._integer_to_padded_binary(k)
        return ISA._instructions["BRLT"] % (k[-7:-5], k[-5:-1], k[-1])

    def _brmi(self, k):
        """Branch if minus"""
        k = self._integer_to_padded_binary(k)
        return ISA._instructions["BRMI"] % (k[-7:-5], k[-5:-1], k[-1])

    def _brne(self, k):
        """Branch if not equal"""
        k = self._integer_to_padded_binary(k)
        return ISA._instructions["BRNE"] % (k[-7:-5], k[-5:-1], k[-1])

    def _brpl(self, k):
        """Branch if plus"""
        k = self._integer_to_padded_binary(k)
        return ISA._instructions["BRPL"] % (k[-7:-5], k[-5:-1], k[-1])

    def _brsh(self, k):
        """Branch if same or higher (unsigned)"""
        k = self._integer_to_padded_binary(k)
        return ISA._instructions["BRSH"] % (k[-7:-5], k[-5:-1], k[-1])

    def _brtc(self, k):
        """Branch if T flag cleared"""
        k = self._integer_to_padded_binary(k)
        return ISA._instructions["BRTC"] % (k[-7:-5], k[-5:-1], k[-1])

    def _brts(self, k):
        """Branch if T flag set"""
        k = self._integer_to_padded_binary(k)
        return ISA._instructions["BRTS"] % (k[-7:-5], k[-5:-1], k[-1])

    def _brvc(self, k):
        """Branch if overflow flag is cleared"""
        k = self._integer_to_padded_binary(k)
        return ISA._instructions["BRVC"] % (k[-7:-5], k[-5:-1], k[-1])

    def _brvs(self, k):
        """Branch if overflow flag is set"""
        k = self._integer_to_padded_binary(k)
        return ISA._instructions["BRVS"] % (k[-7:-5], k[-5:-1], k[-1])

    def _bset(self, s):
        """Set bit in status register"""
        if not 0 <= s <= 7:
            return None
        
        # TODO: change this pattern to ...binary(s, 3) & ... % (s)
        s = self._integer_to_padded_binary(s)
        return ISA._instructions["BRVS"] % (s[-3:])

    def _bst(self, rr, b):
        """Bit store from register to T"""
        try:
            rrCode = self._gp_register_mapping[rr]
        except KeyError:
            return None
        
        if not 0 <= b <= 7:
            return None
        
        b = self._integer_to_padded_binary(b)
        return ISA._instructions["BRBS"] % (rrCode[-7:-5], rrCode[-5:-1], 
                                            rrCode[-1], b[-3:])

    def _cbi(self, p, b):
        """Clear bit in I/O register (0 <= P <= 31)"""
        pass


    def _cbr(self, rd, k):
        """Clear bit(s) in register (16 <= d <= 31)"""
        try:
            rdCode = self._gp_register_mapping[rd]
        except KeyError:
            return None
        
        if '1' not in rdCode[0:4]:  # checks rd >= r16
            return None
        
        k = self._integer_to_padded_binary(~k)
        return ISA._instructions["ANDI"] % (k[0:4], rdCode[-4:], k[4:])

    def _clc(self):
        """Clear carry flag"""
        return ISA._instructions["CLC"]

    def _clh(self):
        """Clear half-carry flag"""
        return ISA._instructions["CLH"]

    def _cli(self):
        """Clear global interrupt flag (disable interrupts)"""
        return ISA._instructions["CLI"]

    def _cln(self):
        """Clear negative flag"""
        return ISA._instructions["CLN"]

    def _clr(self, rd):
        """Clear register"""
        pass


    def _cls(self):
        """Clear signed flag"""
        return ISA._instructions["CLS"]

    def _clt(self):
        """Clear T flag"""
        return ISA._instructions["CLT"]

    def _clv(self):
        """Clear overflow flag"""
        return ISA._instructions["CLV"]
    
    def _clz(self):
        """Clear zero flag"""
        return ISA._instructions["CLZ"]

    def _com(self, rd):
        """One's complement (inversion)"""
        pass

    def _cp(self, rd, rr):
        """Compare"""
        try:
            rdCode, rrCode = self._gp_register_mapping[rd], \
                             self._gp_register_mapping[rr]
        except KeyError:
            return None
        
        return ISA._instructions["CP"] % (rdCode[-5], rrCode[-5], rdCode[-4:],
                                     rrCode[-4:])

    def _cpc(self, rd, rr):
        """Compare with Carry"""
        try:
            rdCode, rrCode = self._gp_register_mapping[rd], \
                             self._gp_register_mapping[rr]
        except KeyError:
            return None
        
        return ISA._instructions["CPC"] % (rdCode[-5], rrCode[-5], rdCode[-4:],
                                     rrCode[-4:])

    def _cpi(self, rd, k):
        """Compare with immediate (16 <= d <= 31)"""
        try:
            rdCode = self._gp_register_mapping[rd]
        except KeyError:
            return None
        
        if '1' not in rdCode[0:4]:  # checks rd >= r16
            return None
        
        k = self._integer_to_padded_binary(k)
        return ISA._instructions["CPI"] % (k[0:4], rdCode[-4:], k[4:])

    def _cpse(self, rd, rr):
        """Compare, skip if equal"""
        try:
            rdCode, rrCode = self._gp_register_mapping[rd], \
                             self._gp_register_mapping[rr]
        except KeyError:
            return None
        
        return ISA._instructions["CPSE"] % (rdCode[-5], rrCode[-5], rdCode[-4:],
                                     rrCode[-4:])

    def _dec(self, rd):
        """Decrement register"""
        pass

    def _eor(self, rd, rr):
        """Exclusive OR two registers"""
        try:
            rdCode, rrCode = self._gp_register_mapping[rd], \
                             self._gp_register_mapping[rr]
        except KeyError:
            return None
        
        return ISA._instructions["EOR"] % (rdCode[-5], rrCode[-5], rdCode[-4:],
                                     rrCode[-4:])

    def _icall(self):
        """Indirect call to [Z] (High bits of Z discarded)"""
        return ISA._instructions["ICALL"]

    def _ijmp(self):
        """Indirect jump to [Z] (High bits of Z discarded)"""
        return ISA._instructions["IJMP"]

    def _in(self, rd, p):
        """Load an I/O Location to Register"""
        pass

    def _inc(self, rd):
        """Increment register"""
        pass

    def _ld(self, rd, xyz):
        """Load Indirect (different cases depending on second parameter)"""
        pass

    def _ldd(self, rd, yz):
        """Load inderect with Displacement (Y or Z only)"""
        pass

    def _ldi(self, rd, k):
        """Load Immediate (16 <= d <= 31)"""
        try:
            rdCode = self._gp_register_mapping[rd]
        except KeyError:
            return None
        
        if '1' not in rdCode[0:4]:  # checks rd >= r16
            return None
        
        k = self._integer_to_padded_binary(k)
        return ISA._instructions["LDI"] % (k[0:4], rdCode[-4:], k[4:])

    def _lds(self, rd, k):
        """Load Direct from SRAM (0 <= k <= 655355)"""
        pass

    def _lpm(self):
        """Load program memory (Z contains a byte address). Least significant
        bit of Z selects low byte of program word (if 0) or high byte (if 1)
        
        """
        return ISA._instructions["LPM"]

    def _lsl(self, rd):
        """Logical shift left"""
        pass

    def _lsr(self, rd):
        """Logical shift right"""
        pass

    def _mov(self, rd, rr):
        """Move between registers"""
        try:
            rdCode, rrCode = self._gp_register_mapping[rd], \
                             self._gp_register_mapping[rr]
        except KeyError:
            return None
        
        return ISA._instructions["MOV"] % (rdCode[-5], rrCode[-5], rdCode[-4:],
                                     rrCode[-4:])

    def _neg(self, rd):
        """Two's complement (negation)"""
        pass

    def _nop(self):
        """No operation"""
        return ISA._instructions["NOP"]

    def _or(self, rd, rr):
        """Logical OR two registers"""
        try:
            rdCode, rrCode = self._gp_register_mapping[rd], \
                             self._gp_register_mapping[rr]
        except KeyError:
            return None
        
        return ISA._instructions["OR"] % (rdCode[-5], rrCode[-5], rdCode[-4:],
                                     rrCode[-4:])

    def _ori(self, rd, k):
        """Logical OR with immediate (16 <= d <= 31)"""
        try:
            rdCode = self._gp_register_mapping[rd]
        except KeyError:
            return None
        
        if '1' not in rdCode[0:4]:  # checks rd >= r16
            return None
        
        k = self._integer_to_padded_binary(k)
        return ISA._instructions["ORI"] % (k[0:4], rdCode[-4:], k[4:])

    def _out(self, p, rr):
        """Store register to I/O Location"""
        pass

    def _pop(self, rd):
        """Pop register from stack"""
        pass

    def _push(self, rr):
        """Push register on stack"""
        pass

    def _rcall(self, k):
        """Relative Subroutine Call (-2048 <= k <= 2047)"""
        pass

    def _ret(self):
        """Subroutine return"""
        return ISA._instructions["RET"]

    def _reti(self):
        """Return from interrupt (and enable interrupts)"""
        return ISA._instructions["RETI"]

    def _rjmp(self, k):
        """Relative Jump (-2048 <= k <= 2047)"""
        pass

    def _rol(self, rd):
        """Rotate left through carry"""
        pass

    def _ror(self, rd):
        """Rotate right through carry"""
        pass

    def _sbc(self, rd, rr):
        """Subtract two registers with carry"""
        try:
            rdCode, rrCode = self._gp_register_mapping[rd], \
                             self._gp_register_mapping[rr]
        except KeyError:
            return None
        
        return ISA._instructions["SBC"] % (rdCode[-5], rrCode[-5], rdCode[-4:],
                                     rrCode[-4:])

    def _sbci(self, rd, k):
        """Subtract immediate with carry (16 <= d <= 31)"""
        try:
            rdCode = self._gp_register_mapping[rd]
        except KeyError:
            return None
        
        if '1' not in rdCode[0:4]:  # checks rd >= r16
            return None
        
        k = self._integer_to_padded_binary(k)
        return ISA._instructions["SBCI"] % (k[0:4], rdCode[-4:], k[4:])

    def _sbi(self, p, b):
        """Set bit in I/O register (0 <= P <= 31)"""
        pass

    def _sbic(self, p, b):
        """Skip if bit in I/O register is cleared (0 <= P <= 31)"""
        pass

    def _sbis(self, p, b):
        """Skip if bit in I/O register is set (0 <= P <= 31)"""
        pass

    def _sbiw(self, rhrl, k):
        """Subtract immediate from word (0 <= K <= 63)"""
        try:
            dd = self._rhrl_mapping[rhrl]
        except KeyError:
            return None
            
        if k < 0 or k > 63:
            return None
            
        try:
            kCode = self._integer_to_padded_binary(int(k))
        except ValueError:
            return None
            
        return ISA._instructions["SBIW"] % (kCode[-6:-4], dd, kCode[-4:])

    def _sbr(self, rd, k):
        """Set bit(s) in register (16 <= d <= 31)"""
        pass

    def _sbrc(self, rr, b):
        """Skip if bit in register is cleared"""
        pass

    def _sbrs(self, rr, b):
        """Skip if bit in register is set"""
        pass

    def _sec(self):
        """Set carry flag"""
        return ISA._instructions["SEC"]

    def _seh(self):
        """Set half-carry flag"""
        return ISA._instructions["SEH"]

    def _sei(self):
        """Set global interrupt flag (enable interruppts). Instruction
        following sei will always be executed before any pending interrupts are
        handled.
        
        """
        return ISA._instructions["SEI"]

    def _sen(self):
        """Set negative flag"""
        return ISA._instructions["SEN"]

    def _ser(self, rd):
        """Set register (16 <= d <= 31)"""
        pass

    def _ses(self):
        """Set signed flag"""
        return ISA._instructions["SES"]

    def _set(self):
        """Set T flag"""
        return ISA._instructions["SET"]

    def _sev(self):
        """Set overflow flag"""
        return ISA._instructions["SEV"]

    def _sez(self):
        """Set zero flag"""
        return ISA._instructions["SEZ"]

    def _sleep(self):
        """Sleep. Sets CPU in sleep mode defined by the MCU control register"""
        return ISA._instructions["SLEEP"]

    def _st(self, xyz, rr):
        """Store Indirect (different cases depending on second parameter)"""
        pass

    def _std(self, yzq, rr):
        """Store indirect with displacement (Y or Z only)"""
        pass

    def _sts(self, k, rr):
        """Store direct to SRAM"""
        pass

    def _sub(self, rd, rr):
        """Subtract two registers"""
        try:
            rdCode, rrCode = self._gp_register_mapping[rd], \
                             self._gp_register_mapping[rr]
        except KeyError:
            return None
        
        return ISA._instructions["SUB"] % (rdCode[-5], rrCode[-5], rdCode[-4:],
                                     rrCode[-4:])

    def _subi(self, rd, k):
        """Subtract immediate (16 <= d <= 31)"""
        try:
            rdCode = self._gp_register_mapping[rd]
        except KeyError:
            return None
        
        if '1' not in rdCode[0:4]:  # checks rd >= r16
            return None
        
        k = self._integer_to_padded_binary(k)
        return ISA._instructions["SUBI"] % (k[0:4], rdCode[-4:], k[4:])

    def _swap(self, rd):
        """Swap nibbles (i.e. high 4 bits is exchanged with low 4 bits)"""
        pass

    def _tst(self, rd):
        """Test for zero or minus"""
        pass

    def _wdr(self):
        """Watchdog reset"""
        return ISA._instructions["WDR"]
    
    def inst2code(self, inst, a = None, b = None):
        print(self._instruction_mapping[inst.upper()](a, b))

