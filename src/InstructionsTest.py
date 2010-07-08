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

import unittest
import pyAVR

class Test(unittest.TestCase):
    
    def setUp(self):
        self.isa = pyAVR.ISA()

#######
# ADC #
#######

    def test_ADC_low_low(self):
        result = self.isa._adc("r0", "r0")
        expected = "0001 1100 0000 0000"
        self.assertEqual(result, expected ,
                         "Unexpected Opcode");
        
    def test_ADC_high_high(self):
        result = self.isa._adc("r31", "r31")
        expected = "0001 1111 1111 1111"
        self.assertEqual(result, expected,
                         "\n\tExpected: %s\n\tGot: %s" % (expected, result));
        
    def test_ADC_low_high(self):
        result = self.isa._adc("r0", "r31")
        expected = "0001 1101 0000 1111"
        self.assertEqual(result, expected,
                         "\n\tExpected: %s\n\tGot: %s" % (expected, result));
                         
    def test_ADC_high_low(self):
        result = self.isa._adc("r31", "r0")
        expected = "0001 1110 1111 0000"
        self.assertEqual(result, expected,
                         "\n\tExpected: %s\n\tGot: %s" % (expected, result));
                         
    def test_ADC_mid_mid(self):
        result = self.isa._adc("r15", "r17")
        expected = "0001 1101 1111 0001"
        self.assertEqual(result, expected,
                         "\n\tExpected: %s\n\tGot: %s" % (expected, result));
                            
    def test_ADC_invalid_valid(self):
        self.assertRaises(pyAVR.InvalidInstruction,
                           self.isa._adc, "r55", "r17");
                            
    def test_ADC_valid_invalid(self):
        self.assertRaises(pyAVR.InvalidInstruction,
                           self.isa._adc, "r15", "r57");

#######
# ADD #
#######

    def test_ADD_low_low(self):
        result = self.isa._add("r0", "r0")
        expected = "0001 1100 0000 0000"
        self.assertEqual(result, expected ,
                         "Unexpected Opcode");
        
    def test_ADD_high_high(self):
        result = self.isa._add("r31", "r31")
        expected = "0001 1111 1111 1111"
        self.assertEqual(result, expected,
                         "\n\tExpected: %s\n\tGot: %s" % (expected, result));
        
    def test_ADD_low_high(self):
        result = self.isa._add("r0", "r31")
        expected = "0001 1101 0000 1111"
        self.assertEqual(result, expected,
                         "\n\tExpected: %s\n\tGot: %s" % (expected, result));
                         
    def test_ADD_high_low(self):
        result = self.isa._add("r31", "r0")
        expected = "0001 1110 1111 0000"
        self.assertEqual(result, expected,
                         "\n\tExpected: %s\n\tGot: %s" % (expected, result));
                         
    def test_ADD_mid_mid(self):
        result = self.isa._add("r15", "r17")
        expected = "0001 1101 1111 0001"
        self.assertEqual(result, expected,
                         "\n\tExpected: %s\n\tGot: %s" % (expected, result));
                            
    def test_ADD_invalid_valid(self):
        self.assertRaises(pyAVR.InvalidInstruction,
                           self.isa._add, "r55", "r17");
                            
    def test_ADD_valid_invalid(self):
        self.assertRaises(pyAVR.InvalidInstruction,
                           self.isa._add, "r15", "r57");
                           
########
# ADIW #
########

    def test_ADIW(self):
        pass

#######
# AND #
#######

    def test_AND(self): #
        pass

########
# ANDI #
########

    def test_ANDI(self):
        pass

#######
# ASR #
#######

    def test_ASR(self):
        pass

########
# BCLR #
########

    def test_BCLR(self):
        pass

#######
# BLD #
#######

    def test_BLD(self):
        pass

########
# BRBC #
########

    def test_BRBC(self):
        pass

########
# BRBS #
########

    def test_BRBS(self):
        pass

########
# BRCC #
########

    def test_BRCC(self):
        pass

########
# BRCS #
########

    def test_BRCS(self):
        pass

########
# BREQ #
########

    def test_BREQ(self):
        pass

########
# BRGE #
########

    def test_BRGE(self):
        pass

########
# BRHC #
########

    def test_BRHC(self):
        pass

########
# BRHS #
########

    def test_BRHS(self):
        pass

########
# BRID #
########

    def test_BRID(self):
        pass

########
# BRIE #
########

    def test_BRIE(self):
        pass

########
# BRLO #
########

    def test_BRLO(self):
        pass

########
# BRLT #
########

    def test_BRLT(self):
        pass

########
# BRMI #
########

    def test_BRMI(self):
        pass

########
# BRNE #
########

    def test_BRNE(self):
        pass

########
# BRPL #
########

    def test_BRPL(self):
        pass

########
# BRSH #
########

    def test_BRSH(self):
        pass

########
# BRTC #
########

    def test_BRTC(self):
        pass

########
# BRTS #
########

    def test_BRTS(self):
        pass

########
# BRVC #
########

    def test_BRVC(self):
        pass

########
# BRVS #
########

    def test_BRVS(self):
        pass

########
# BSET #
########

    def test_BSET(self):
        pass

#######
# BST #
#######

    def test_BST(self):
        pass

#######
# CBI #
#######

    def test_CBI(self):
        pass

#######
# CBR #
#######

    def test_CBR(self):
        pass

#######
# CLC #
#######

    def test_CLC(self):
        pass

#######
# CLH #
#######

    def test_CLH(self):
        pass

#######
# CLI #
#######

    def test_CLI(self):
        pass

#######
# CLN #
#######

    def test_CLN(self):
        pass

#######
# CLR #
#######

    def test_CLR(self):
        pass

#######
# CLS #
#######

    def test_CLS(self):
        pass

#######
# CLT #
#######

    def test_CLT(self):
        pass

#######
# CLV #
#######

    def test_CLV(self):
        pass

#######
# CLZ #
#######

    def test_CLZ(self):
        pass

#######
# COM #
#######

    def test_COM(self):
        pass

######
# CP #
######

    def test_CP(self): #
        pass

#######
# CPC #
#######

    def test_CPC(self): #
        pass

#######
# CPI #
#######

    def test_CPI(self):
        pass

########
# CPSE #
########

    def test_CPSE(self): #
        pass

#######
# DEC #
#######

    def test_DEC(self):
        pass

#######
# EOR #
#######

    def test_EOR(self): #
        pass

#########
# ICALL #
#########

    def test_ICALL(self):
        pass

########
# IJMP #
########

    def test_IJMP(self):
        pass

######
# IN #
######

    def test_IN(self):
        pass

#######
# INC #
#######

    def test_INC(self):
        pass

######
# LD #
######

    def test_LD(self):
        pass

#######
# LDD #
#######

    def test_LDD(self):
        pass

#######
# LDI #
#######

    def test_LDI(self):
        pass

#######
# LDS #
#######

    def test_LDS(self):
        pass

#######
# LPM #
#######

    def test_LPM(self):
        pass

#######
# LSL #
#######

    def test_LSL(self):
        pass

#######
# LSR #
#######

    def test_LSR(self):
        pass

#######
# MOV #
#######

    def test_MOV(self): #
        pass

#######
# NEG #
#######

    def test_NEG(self):
        pass

#######
# NOP #
#######

    def test_NOP(self):
        pass

######
# OR #
######

    def test_OR(self): #
        pass

#######
# ORI #
#######

    def test_ORI(self):
        pass

#######
# OUT #
#######

    def test_OUT(self):
        pass

#######
# POP #
#######

    def test_POP(self):
        pass

########
# PUSH #
########

    def test_PUSH(self):
        pass

#########
# RCALL #
#########

    def test_RCALL(self):
        pass

#######
# RET #
#######

    def test_RET(self):
        pass

########
# RETI #
########

    def test_RETI(self):
        pass

########
# RJMP #
########

    def test_RJMP(self):
        pass

#######
# ROL #
#######

    def test_ROL(self):
        pass

#######
# ROR #
#######

    def test_ROR(self):
        pass

#######
# SBC #
#######

    def test_SBC(self): #
        pass

########
# SBCI #
########

    def test_SBCI(self):
        pass

#######
# SBI #
#######

    def test_SBI(self):
        pass

########
# SBIC #
########

    def test_SBIC(self):
        pass

########
# SBIC #
########

    def test_SBIS(self):
        pass

########
# SBIW #
########

    def test_SBIW(self):
        pass

#######
# SBR #
#######

    def test_SBR(self):
        pass

########
# SBRC #
########

    def test_SBRC(self):
        pass

########
# SBRS #
########

    def test_SBRS(self):
        pass

#######
# SEC #
#######

    def test_SEC(self):
        pass

#######
# SEH #
#######

    def test_SEH(self):
        pass

#######
# SEI #
#######

    def test_SEI(self):
        pass

#######
# SEN #
#######

    def test_SEN(self):
        pass

#######
# SER #
#######

    def test_SER(self):
        pass

#######
# SES #
#######

    def test_SES(self):
        pass

#######
# SET #
#######

    def test_SET(self):
        pass

#######
# SEV #
#######

    def test_SEV(self):
        pass

#######
# SEZ #
#######

    def test_SEZ(self):
        pass

#########
# SLEEP #
#########

    def test_SLEEP(self):
        pass

######
# ST #
######

    def test_ST(self):
        pass

#######
# STD #
#######

    def test_STD(self):
        pass

#######
# STS #
#######

    def test_STS(self):
        pass

#######
# SUB #
#######

    def test_SUB(self): #
        pass

########
# SUBI #
########

    def test_SUBI(self):
        pass

########
# SWAP #
########

    def test_SWAP(self):
        pass

#######
# TST #
#######

    def test_TST(self):
        pass

#######
# WDR #
#######

    def test_WDR(self):
        pass



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()