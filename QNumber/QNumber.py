class QNum:
    # Class for the signed Q-number. Assumes Qm.n
    # bit_depth = 1 (sign bit) + num_int_bits + num_frac_bits
    # Negative numbers can be represented in various ways:
    # bin_format -> 0: sign_magnitude, 1: 1's compement, 2: 2's complement. 
    # https://en.wikipedia.org/wiki/Q_(number_format)
    def __init__(self, qdata=0, num_int_bits=5, num_frac_bits=10, bit_depth=16, bin_format=2):
        self.qdata = str(qdata)
        self.bin_format = bin_format
        self.num_int_bits = int(num_int_bits)
        self.num_frac_bits = int(num_frac_bits)
        self.bit_depth = int(bit_depth)

    # Make a copy of the object
    def copy(self):
        qdata = self.qdata
        bin_format = self.bin_format
        num_frac_bits = self.num_frac_bits
        num_int_bits = self.num_int_bits
        bit_depth = self.bit_depth
        q_num_copied = QNum(qdata=qdata, num_int_bits=num_int_bits, num_frac_bits=num_frac_bits, bit_depth=bit_depth, bin_format=bin_format)
        return q_num_copied
    
    # Get the sign of the number
    def getSign(self):
        qdata = self.qdata
        return bool(int(qdata[0], 2))
    
    # Toggle the sign bit
    def signToggle(self):
        qdata = self.qdata
        bin_format = self.bin_format
        num_frac_bits = self.num_frac_bits
        num_int_bits = self.num_int_bits
        bit_depth = self.bit_depth

        new_sign_bit = str(int(not(self.getSign())))
        qdata = new_sign_bit + qdata[1:]

        q_num_inv = QNum(qdata=qdata, num_int_bits=num_int_bits, num_frac_bits=num_frac_bits, bit_depth=bit_depth, bin_format=bin_format)
        return q_num_inv
    
    # Convert the Q-number into floating number
    def q2Float(self):
        qdata = self.qdata
        bin_format = self.bin_format
        num_frac_bits = self.num_frac_bits
        num_int_bits = self.num_int_bits
        bit_depth = self.bit_depth

        if (num_int_bits+num_frac_bits+1 != bit_depth):
            print("Error in number of bits")

        is_neg = self.getSign()
        f_num = float(int(qdata[-(bit_depth-1):], 2)) / (2**num_frac_bits)

        # If data is positive get the straightforward calculation
        if is_neg:
            if bin_format == 0:
                f_num = -f_num
                return f_num

            ones_qdata = qdata
            # if it is 2s complement
            if bin_format == 2:
                twos_qdata = bin(int(qdata, 2) - 1)
                ones_qdata = twos_qdata[-bit_depth:]

            sign_mag_qdata = ones_qdata[0]
            for ii in range(1, len(ones_qdata)): sign_mag_qdata = sign_mag_qdata + str(int(not(bool(int(ones_qdata[ii], 2)))))

            f_num = -float(int(sign_mag_qdata[-(bit_depth-1):], 2)) / (2**num_frac_bits)

        return f_num
    
    # Perform bit shift left operation
    def bitShiftLeft(self, sat=True):
        f_num = self.q2Float()

        # Bit shift Left
        f_num = f_num * 2

        num_frac_bits = self.num_frac_bits
        num_int_bits = self.num_int_bits
        bit_depth = self.bit_depth

        q_num = float2Q(f_num, num_int_bits=num_int_bits, num_frac_bits=num_frac_bits, bit_depth=bit_depth, sat=sat)

        return q_num
    
    # Perform bit shift right operation.
    # Note that the right shift operation for the negative numbers are usually 
    # implementation dependent.
    def bitShiftRight(self, sat=True):
        f_num = self.q2Float()

        # Bit shift Right
        f_num = f_num / 2

        num_frac_bits = self.num_frac_bits
        num_int_bits = self.num_int_bits
        bit_depth = self.bit_depth
        bin_format = self.bin_format

        q_num = float2Q(f_num, num_int_bits=num_int_bits, num_frac_bits=num_frac_bits, bit_depth=bit_depth, sat=sat, bin_format=bin_format)

        return q_num
    
    # Clear and set number to 0
    def clr(self):
        f_num = 0.0

        num_frac_bits = self.num_frac_bits
        num_int_bits = self.num_int_bits
        bit_depth = self.bit_depth
        bin_format = self.bin_format

        q_num = float2Q(f_num, num_int_bits=num_int_bits, num_frac_bits=num_frac_bits, bit_depth=bit_depth, sat=True, bin_format=bin_format)

        return q_num

    # Invert all the bits of Q-number
    def inv(self):
        qdata = self.qdata
        num_frac_bits = self.num_frac_bits
        num_int_bits = self.num_int_bits
        bit_depth = self.bit_depth
        bin_format = self.bin_format

        new_qdata = ''
        for ii in range(len(qdata)): new_qdata = new_qdata + str(int(not(bool(int(qdata[ii], 2)))))

        q_num = QNum(qdata=new_qdata, num_int_bits=num_int_bits, num_frac_bits=num_frac_bits, bit_depth=bit_depth, bin_format=bin_format)

        return q_num
    
# Float to Q-number converter
def float2Q(f_num=0, num_int_bits=5, num_frac_bits=10, bit_depth=16, sat=True, bin_format=2) -> QNum:
    # Check if the numbers of bits are set correctly. If not adjust them
    if (num_int_bits+num_frac_bits+1 != bit_depth):
        print("Error in number of bits. Adjustying them using integer bit priority")
        if (bit_depth < (num_int_bits+1)):
            num_int_bits = bit_depth-1
            num_frac_bits = 0
        else:
            num_frac_bits = bit_depth-1-num_int_bits

    print("Using: num_int_bits:", num_int_bits, ", num_frac_bits:", num_frac_bits, ", bit_depth:", bit_depth, ", sign_bit = 1")
    
    is_neg = (f_num<0)
    q_num = QNum(qdata=0, num_int_bits=num_int_bits, num_frac_bits=num_frac_bits, bit_depth=bit_depth, bin_format=bin_format)

    # Check if the number can be represented with the given bit-depth
    max_f_num = (2**(bit_depth-1) - 1) / (2**num_frac_bits)
    if abs(f_num) > max_f_num and sat is True:
        q_num.qdata = str(int(is_neg)) + str(1) * (bit_depth-1)
        print("Bit-depth is not enough for the input data. Saturating the input from ", f_num, " to ", [-max_f_num if is_neg else max_f_num])
    else:
        # Shift the data to the left to get fractional bits as int bits and then quantize
        f_num_int = abs(int(f_num*(2**num_frac_bits)))
        b_num_str = str(0) * (bit_depth) + bin(f_num_int)[2:]

        # The 1st bit is sign bit
        q_num.qdata = str(int(is_neg)) + b_num_str[-(bit_depth-1):]

    # If the data is negative and either 1's or 2's complement is required
    if is_neg and bool(bin_format):
        # 1's complement
        ones_qdata = q_num.qdata[0]
        for ii in range(1, len(q_num.qdata)): ones_qdata = ones_qdata + str(int(not(bool(int(q_num.qdata[ii], 2)))))
        new_qdata = ones_qdata

        # 2's complement
        if bin_format == 2:
            twos_qdata = bin(int(ones_qdata, 2) + 1)
            new_qdata = twos_qdata[-bit_depth:]

        q_num.qdata = new_qdata

    return q_num

# Q-number to Float converter
def q2Float(q_num: QNum) -> QNum:
    return q_num.q2Float()

# Sum given two Q-numbers and return into the container defined by q_num_out
def qSum(q_num_in_1: QNum, q_num_in_2: QNum, q_num_out: QNum, sat=True) -> QNum:
    num_int_bits=q_num_out.num_int_bits
    num_frac_bits=q_num_out.num_frac_bits
    bit_depth=q_num_out.bit_depth
    bin_format = q_num_out.bin_format

    f_num_out = q_num_in_1.q2Float() + q_num_in_2.q2Float()

    q_num_out = float2Q(f_num_out, num_int_bits=num_int_bits, num_frac_bits=num_frac_bits, bit_depth=bit_depth, sat=sat, bin_format=bin_format)

    return q_num_out

# Subtract given two Q-numbers and return into the container defined by q_num_out
def qSub(q_num_in_1: QNum, q_num_in_2: QNum, q_num_out: QNum, sat=True) -> QNum:
    num_int_bits=q_num_out.num_int_bits
    num_frac_bits=q_num_out.num_frac_bits
    bit_depth=q_num_out.bit_depth
    bin_format = q_num_out.bin_format

    f_num_out = q_num_in_1.q2Float() - q_num_in_2.q2Float()

    q_num_out = float2Q(f_num_out, num_int_bits=num_int_bits, num_frac_bits=num_frac_bits, bit_depth=bit_depth, sat=sat, bin_format=bin_format)

    return q_num_out

# Multiply given two Q-numbers and return into the container defined by q_num_out
def qMul(q_num_in_1: QNum, q_num_in_2: QNum, q_num_out: QNum, sat=True) -> QNum:
    num_int_bits=q_num_out.num_int_bits
    num_frac_bits=q_num_out.num_frac_bits
    bit_depth=q_num_out.bit_depth
    bin_format = q_num_out.bin_format

    f_num_out = q_num_in_1.q2Float() * q_num_in_2.q2Float()
       
    q_num_out = float2Q(f_num_out, num_int_bits=num_int_bits, num_frac_bits=num_frac_bits, bit_depth=bit_depth, sat=sat, bin_format=bin_format)

    return q_num_out

# Divide the given two Q-numbers and return into the container defined by q_num_out
def qDiv(q_num_in_1: QNum, q_num_in_2: QNum, q_num_out: QNum, sat=True) -> QNum:
    FLT_EPS = 2.220446049250313e-16
    f_num_out = q_num_in_1.q2Float() / (q_num_in_2.q2Float() + float(not(bool(q_num_in_2.q2Float())))*FLT_EPS)

    num_int_bits=q_num_out.num_int_bits
    num_frac_bits=q_num_out.num_frac_bits
    bit_depth=q_num_out.bit_depth
    bin_format = q_num_out.bin_format
    q_num_out = float2Q(f_num_out, num_int_bits=num_int_bits, num_frac_bits=num_frac_bits, bit_depth=bit_depth, sat=sat, bin_format=bin_format)

    return q_num_out

# Perform bitwise AND operation for the given two Q-numbers and return into the container defined by q_num_out
def qAnd(q_num_in_1: QNum, q_num_in_2: QNum, q_num_out: QNum) -> QNum:
    qdata_1 = q_num_in_1.qdata
    qdata_2 = q_num_in_2.qdata
    num_int_bits=q_num_out.num_int_bits
    num_frac_bits=q_num_out.num_frac_bits
    bit_depth=q_num_out.bit_depth
    bin_format = q_num_out.bin_format

    new_qdata = ''
    for ii in range(len(qdata_1)):
        bit_result = bool(int(qdata_1[ii], 2)) & bool(int(qdata_2[ii], 2))
        new_qdata = new_qdata + str(int(bit_result))

    q_num_out = QNum(qdata=new_qdata, num_int_bits=num_int_bits, num_frac_bits=num_frac_bits, bit_depth=bit_depth, bin_format=bin_format)
    return q_num_out

# Perform bitwise OR operation for the given two Q-numbers and return into the container defined by q_num_out
def qOr(q_num_in_1: QNum, q_num_in_2: QNum, q_num_out: QNum) -> QNum:
    qdata_1 = q_num_in_1.qdata
    qdata_2 = q_num_in_2.qdata
    num_int_bits=q_num_out.num_int_bits
    num_frac_bits=q_num_out.num_frac_bits
    bit_depth=q_num_out.bit_depth
    bin_format = q_num_out.bin_format

    new_qdata = ''
    for ii in range(len(qdata_1)):
        bit_result = bool(int(qdata_1[ii], 2)) | bool(int(qdata_2[ii], 2))
        new_qdata = new_qdata + str(int(bit_result))

    q_num_out = QNum(qdata=new_qdata, num_int_bits=num_int_bits, num_frac_bits=num_frac_bits, bit_depth=bit_depth, bin_format=bin_format)
    return q_num_out

# Perform bitwise NAND operation for the given two Q-numbers and return into the container defined by q_num_out
def qNand(q_num_in_1: QNum, q_num_in_2: QNum, q_num_out: QNum) -> QNum:
    qdata_1 = q_num_in_1.qdata
    qdata_2 = q_num_in_2.qdata
    num_int_bits = q_num_out.num_int_bits
    num_frac_bits = q_num_out.num_frac_bits
    bit_depth = q_num_out.bit_depth
    bin_format = q_num_out.bin_format

    new_qdata = ''
    for ii in range(len(qdata_1)):
        bit_result = not(bool(int(qdata_1[ii], 2)) & bool(int(qdata_2[ii], 2)))
        new_qdata = new_qdata + str(int(bit_result))

    q_num_out = QNum(qdata=new_qdata, num_int_bits=num_int_bits, num_frac_bits=num_frac_bits, bit_depth=bit_depth, bin_format=bin_format)
    return q_num_out

# Perform bitwise NOR operation for the given two Q-numbers and return into the container defined by q_num_out
def qNor(q_num_in_1: QNum, q_num_in_2: QNum, q_num_out: QNum) -> QNum:
    qdata_1 = q_num_in_1.qdata
    qdata_2 = q_num_in_2.qdata
    num_int_bits = q_num_out.num_int_bits
    num_frac_bits = q_num_out.num_frac_bits
    bit_depth = q_num_out.bit_depth
    bin_format = q_num_out.bin_format

    new_qdata = ''
    for ii in range(len(qdata_1)):
        bit_result = not(bool(int(qdata_1[ii], 2)) | bool(int(qdata_2[ii], 2)))
        new_qdata = new_qdata + str(int(bit_result))

    q_num_out = QNum(qdata=new_qdata, num_int_bits=num_int_bits, num_frac_bits=num_frac_bits, bit_depth=bit_depth, bin_format=bin_format)
    return q_num_out

# Perform bitwise XOR operation for the given two Q-numbers and return into the container defined by q_num_out
def qXor(q_num_in_1: QNum, q_num_in_2: QNum, q_num_out: QNum) -> QNum:
    qdata_1 = q_num_in_1.qdata
    qdata_2 = q_num_in_2.qdata
    num_int_bits = q_num_out.num_int_bits
    num_frac_bits = q_num_out.num_frac_bits
    bit_depth = q_num_out.bit_depth
    bin_format = q_num_out.bin_format

    new_qdata = ''
    for ii in range(len(qdata_1)):
        bit_result = (bool(int(qdata_1[ii], 2)) ^ bool(int(qdata_2[ii], 2)))
        new_qdata = new_qdata + str(int(bit_result))

    q_num_out = QNum(qdata=new_qdata, num_int_bits=num_int_bits, num_frac_bits=num_frac_bits, bit_depth=bit_depth, bin_format=bin_format)
    return q_num_out

# Tests 
def QArithmeticsTests():
    #f_num = 0.0009765625
    f_num = -0.5
    bit_depth = 16
    num_frac_bits = 10
    num_int_bits = 5
    bin_format = 2 
    q_num = float2Q(f_num, num_int_bits=num_int_bits, num_frac_bits=num_frac_bits, bit_depth=bit_depth, sat=True, bin_format=bin_format)
    print(q_num.qdata)

    f_num_inv = q_num.q2Float()
    print(f_num_inv)
    q_out = q_num.copy()
    q_out = qSum(q_num, q_num, q_out, sat=True)
    q_out = qSum(q_num, q_num, q_out, sat=False)
    q_out = qSub(q_num, q_num, q_out, sat=True)
    q_out = qSub(q_num, q_num, q_out, sat=False)
    q_out = qMul(q_num, q_num, q_out, sat=True)
    q_out = qMul(q_num, q_num, q_out, sat=False)
    q_out = qDiv(q_num, q_num, q_out)

    return True

#QArithmeticsTests()