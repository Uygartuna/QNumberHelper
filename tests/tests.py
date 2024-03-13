"""
Simple example of using tests
You would normally have your code in another file in another folder
And your test in a folder named "test".
Here an example of what the folder directory would look like:
package
  - math
      - square.py
      - __init__.py
  - test
      - square_test.py
      - __.init__.py
  - __init__.py
The __init__.py makes the folder as a python module.
In TDD (Test Driven Development) you would first write the test,
then you would implement the code to make the test pass.
Finally you would refactor your code to make it smaller, more lisible
and more integrated with the rest.
"""

# Default python library for unit testing
import unittest

import os, sys
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, path)

from QNumber import *

def are_QNums_same(q_num_1, q_num_2):
    ret_val = (q_num_1.qdata == q_num_2.qdata) and \
    (q_num_1.bin_format == q_num_2.bin_format) and \
    (q_num_1.num_int_bits == q_num_2.num_int_bits) and \
    (q_num_1.num_frac_bits == q_num_2.num_frac_bits) and \
    (q_num_1.bit_depth == q_num_2.bit_depth)
    
    return ret_val


class QNumTests(unittest.TestCase):
    """
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
    """

    def test_QNum_FNum_conversions(self):
        """
        Check the back and forth conversions
        """
        f_num = 10.65625
        # Positive GT value
        q_num_gt_p = '0010101010100000'
        # Negative GT values for 3 different bin_formats
        q_num_gt_n = ['1010101010100000', '1101010101011111', '1101010101100000']
        
        q_num_test = float2Q(f_num=f_num, num_int_bits=5, num_frac_bits=10, bit_depth=16, sat=True, bin_format=2)
        self.assertEqual(q_num_test.qdata, q_num_gt_p)
        f_num_test = q_num_test.q2Float()
        self.assertEqual(f_num_test, f_num)

        for b_f in range(3):
            q_num_test = float2Q(f_num=-f_num, num_int_bits=5, num_frac_bits=10, bit_depth=16, sat=True, bin_format=b_f)
            self.assertEqual(q_num_test.qdata, q_num_gt_n[b_f])
            f_num_test = q_num_test.q2Float()
            self.assertEqual(f_num_test, -f_num)

        # Test some border values
        f_num = [0, 1, -1, 31.9990234375, -31.9990234375, 0.0009765625, -0.0009765625,]
        # GT values, Negative GT values in 2s complement
        q_num_gt = ['0000000000000000', '0000010000000000', '1111110000000000', '0111111111111111', '1000000000000001','0000000000000001','1111111111111111']

        for ii in range(len(f_num)):
            q_num_test = float2Q(f_num=f_num[ii], num_int_bits=5, num_frac_bits=10, bit_depth=16, sat=True, bin_format=2)
            self.assertEqual(q_num_test.qdata, q_num_gt[ii])
            f_num_test = q_num_test.q2Float()
            self.assertEqual(f_num_test, f_num[ii])

    def test_QNum_operations(self):
        num_frac_bits = 10
        f_nums = [10.75390625, -7.099609375]
        q_nums = []
        [q_nums.append(float2Q(f_num=f_nums[ii], num_int_bits=5, num_frac_bits=num_frac_bits, bit_depth=16, sat=True, bin_format=2)) for ii in range(len(f_nums))]

        q_nums_out = q_nums[0].copy()
        self.assertTrue(are_QNums_same(q_nums_out, q_nums[0]))

        # Sum:
        f_nums_op = sum(f_nums)
        q_nums_out = qSum(q_num_in_1=q_nums[0], q_num_in_2=q_nums[1], q_num_out=q_nums_out, sat=True)
        f_nums_op_test = q_nums_out.q2Float()
        self.assertEqual(f_nums_op_test, f_nums_op)

        # Sub:
        f_nums_op = f_nums[0] - f_nums[1]
        q_nums_out = qSub(q_num_in_1=q_nums[0], q_num_in_2=q_nums[1], q_num_out=q_nums_out, sat=True)
        f_nums_op_test = q_nums_out.q2Float()
        self.assertEqual(f_nums_op_test, f_nums_op)

        # Mul:
        f_nums_op = f_nums[0] * f_nums[1]
        if f_nums_op > 31.9990234375 : f_nums_op = 31.9990234375
        if f_nums_op < -31.9990234375 : f_nums_op = -31.9990234375
        q_nums_out = qMul(q_num_in_1=q_nums[0], q_num_in_2=q_nums[1], q_num_out=q_nums_out, sat=True)
        f_nums_op_test = q_nums_out.q2Float()
        self.assertEqual(f_nums_op_test, f_nums_op)

        # Div:
        f_nums_op = f_nums[0] / f_nums[1]
        q_nums_out = qDiv(q_num_in_1=q_nums[0], q_num_in_2=q_nums[1], q_num_out=q_nums_out, sat=True)
        f_nums_op_test = q_nums_out.q2Float()
        self.assertAlmostEqual(f_nums_op_test, f_nums_op, None, None, 1/(2**num_frac_bits))

    def test_QNum_bit_operations(self):
        num_frac_bits = 10
        f_nums = [10.75390625, -7.099609375]
        q_nums = []
        int_nums = []
        [q_nums.append(float2Q(f_num=f_nums[ii], num_int_bits=5, num_frac_bits=num_frac_bits, bit_depth=16, sat=True, bin_format=2)) for ii in range(len(f_nums))]
        [int_nums.append(int(q_nums[ii].qdata,2)) for ii in range(len(f_nums))]

        q_nums_out = q_nums[0].copy()
        self.assertTrue(are_QNums_same(q_nums_out, q_nums[0]))

        # And:
        q_nums_out_gt = bin(int_nums[0] & int_nums[1])[2:]
        q_nums_out_test = qAnd(q_num_in_1=q_nums[0], q_num_in_2=q_nums[1], q_num_out=q_nums_out)
        self.assertEqual(q_nums_out_test.qdata[-len(q_nums_out_gt):], q_nums_out_gt)

        # Or:
        q_nums_out_gt = bin(int_nums[0] | int_nums[1])[2:]
        q_nums_out_test = qOr(q_num_in_1=q_nums[0], q_num_in_2=q_nums[1], q_num_out=q_nums_out)
        self.assertEqual(q_nums_out_test.qdata[-len(q_nums_out_gt):], q_nums_out_gt)

        # Nand:
        max_int_data = int(str(1) * (16), 2)
        q_nums_out_gt = bin(max_int_data-(int_nums[0] & int_nums[1]))[2:]
        q_nums_out_test = qNand(q_num_in_1=q_nums[0], q_num_in_2=q_nums[1], q_num_out=q_nums_out)
        self.assertEqual(q_nums_out_test.qdata[-len(q_nums_out_gt):], q_nums_out_gt)

        # Nor:
        q_nums_out_gt = bin(max_int_data-(int_nums[0] | int_nums[1]))[2:]
        q_nums_out_test = qNor(q_num_in_1=q_nums[0], q_num_in_2=q_nums[1], q_num_out=q_nums_out)
        self.assertEqual(q_nums_out_test.qdata[-len(q_nums_out_gt):], q_nums_out_gt)

        # Xor:
        q_nums_out_gt = bin((int_nums[0] ^ int_nums[1]))[2:]
        q_nums_out_test = qXor(q_num_in_1=q_nums[0], q_num_in_2=q_nums[1], q_num_out=q_nums_out)
        self.assertEqual(q_nums_out_test.qdata[-len(q_nums_out_gt):], q_nums_out_gt)

        # BSL & BSR:
        for ii in range(len(q_nums)):
            q_nums_out_test = q_nums[ii].bitShiftLeft()
            f_nums_out_test = q_nums_out_test.q2Float()
            f_nums_out_gt = f_nums[ii]*2
            self.assertEqual(f_nums_out_test, f_nums_out_gt)

            f_nums_out_test = (q_nums_out_test.bitShiftRight()).q2Float()
            f_nums_out_gt = f_nums[ii]
            self.assertEqual(f_nums_out_test, f_nums_out_gt)

        # clear & inverse:
        for ii in range(len(q_nums)):
            q_nums_out_test = qAnd(q_nums[ii], q_nums[ii].inv(), q_nums_out)
            f_nums_out_test = q_nums_out_test.q2Float()
            self.assertEqual(f_nums_out_test, 0.0)

            q_nums_out_test = q_nums[ii].clr()
            f_nums_out_test = q_nums_out_test.q2Float()
            self.assertEqual(f_nums_out_test, 0.0)

if __name__ == "__main__":
    unittest.main()