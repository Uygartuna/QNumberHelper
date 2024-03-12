import sys, math

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QSpinBox, QHBoxLayout, QDoubleSpinBox, QComboBox, QCheckBox, QFrame, QTextEdit
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from functools import partial

from QNumber.QNumber import *

class QNumberHelperApp(QWidget):
    def __init__(self):
        super().__init__()

        # Initialize UI components
        self.init_ui()

        # Fixed Parameters
        self.max_bitdepth = 64
        self.BN_Prefix = "Binary (s|I.F): "
        self.HEX_Prefix = "Hexadecimal: "
        self.INT_Prefix = "Integer: "

        # Some initial parameters
        self.bin_hex_int_mode = 0 #0: bin, 1:hex, 2:int
        self.BN_Format = 2
        self.sat_flag = True
        self.adjust_BDepth = False

        # Initialize variables to store values
        self.NIBs = [self.spin_box_NIB[x].value() for x in range(len(self.spin_box_NIB))]
        self.NFBs = [self.spin_box_NFB[x].value() for x in range(len(self.spin_box_NFB))]
        self.NBs = [self.spin_box_NB[x].value() for x in range(len(self.spin_box_NB))]
        self.f_nums = [self.double_spin_box_FN[x].value() for x in range(len(self.double_spin_box_FN))]
        self.q_nums = [float2Q(f_num=self.f_nums[x], num_int_bits=self.NIBs[x], num_frac_bits=self.NFBs[x], bit_depth=self.NBs[x], sat=self.sat_flag, bin_format=self.BN_Format) for x in range(len(self.f_nums))]
        self.max_num_out = (2**(self.NBs[2]-1) - 1) / (2**self.NFBs[2])

    def update_comm_window(self, in_text="in_text"):
        content = self.str_Comm_Window.toPlainText()
        new_content = content + '\n' + str(self.comm_Win_Line_Num) + ' - '  + in_text
        self.str_Comm_Window.setPlainText(new_content)
        self.comm_Win_Line_Num += 1
        self.str_Comm_Window.verticalScrollBar().setValue(self.str_Comm_Window.verticalScrollBar().maximum())
        return

    def ui_add_text(self, layout, in_text="in_text"):
        label = QLabel(in_text)
        layout.addWidget(label)
        return
    
    def ui_splitter_line(self, layout, is_hor=True, border_width=1):
        splitter_line = QFrame()
        if is_hor:
            splitter_line.setFrameShape(QFrame.HLine)  # Set the frame shape to horizontal line
        else:
            splitter_line.setFrameShape(QFrame.VLine)  # Set the frame shape to vertical line
        splitter_line.setStyleSheet(f"border-width: {border_width}px; border-style: solid;")  # Set border width to 1px for bold appearance
        layout.addWidget(splitter_line)
        return

    def ui_settings_elements(self, layout):
        layout_SET = QHBoxLayout()

        text_str = f"Settings:"
        self.ui_add_text(layout=layout_SET, in_text=text_str)
        self.ui_splitter_line(layout=layout_SET, is_hor=False, border_width=1)

        self.bin_fmt_cb = QComboBox()
        self.bin_fmt_cb.addItems(["Sign_Mag", "1sComplement", "2sComplement"])
        self.bin_fmt_cb.setCurrentText("2sComplement") 
        self.bin_fmt_cb.currentIndexChanged.connect(self.update_BN_Format)
        layout_SET.addWidget(self.bin_fmt_cb)

        self.toggle_btn = QPushButton('BIN/HEX/INT', self)
        self.toggle_btn.clicked.connect(self.bin_hex_int_btn_clicked)
        layout_SET.addWidget(self.toggle_btn)

        self.sat_flag_check = QCheckBox("Saturate?", self)
        self.sat_flag_check.setChecked(True)
        self.sat_flag_check.clicked.connect(self.sat_flag_check_clicked)
        layout_SET.addWidget(self.sat_flag_check)

        self.adjust_bitdepth_flag_check = QCheckBox("Adjust BitDepth?", self)
        self.adjust_bitdepth_flag_check.setChecked(False)
        self.adjust_bitdepth_flag_check.clicked.connect(self.adjust_bitdepth_flag_check_clicked)
        layout_SET.addWidget(self.adjust_bitdepth_flag_check)

        layout.addLayout(layout_SET)
        return

    def ui_op_elements(self, layout):
        layout_OP = QHBoxLayout()

        text_str = f"Operations:"
        self.ui_add_text(layout=layout_OP, in_text=text_str)
        self.ui_splitter_line(layout=layout_OP, is_hor=False, border_width=1)

        self.sum_btn = QPushButton('SUM (+)', self)
        self.sum_btn.clicked.connect(self.sum_btn_clicked)
        layout_OP.addWidget(self.sum_btn)

        self.sub_btn = QPushButton('SUB (-)', self)
        self.sub_btn.clicked.connect(self.sub_btn_clicked)
        layout_OP.addWidget(self.sub_btn)

        self.mul_btn = QPushButton('MUL (x)', self)
        self.mul_btn.clicked.connect(self.mul_btn_clicked)
        layout_OP.addWidget(self.mul_btn)

        self.div_btn = QPushButton('DIV (/)', self)
        self.div_btn.clicked.connect(self.div_btn_clicked)
        layout_OP.addWidget(self.div_btn)

        self.and_btn = QPushButton('AND', self)
        self.and_btn.clicked.connect(self.and_btn_clicked)
        layout_OP.addWidget(self.and_btn)

        self.or_btn = QPushButton('OR', self)
        self.or_btn.clicked.connect(self.or_btn_clicked)
        layout_OP.addWidget(self.or_btn)

        self.nand_btn = QPushButton('NAND', self)
        self.nand_btn.clicked.connect(self.nand_btn_clicked)
        layout_OP.addWidget(self.nand_btn)

        self.nor_btn = QPushButton('NOR', self)
        self.nor_btn.clicked.connect(self.nor_btn_clicked)
        layout_OP.addWidget(self.nor_btn)

        self.xor_btn = QPushButton('XOR', self)
        self.xor_btn.clicked.connect(self.xor_btn_clicked)
        layout_OP.addWidget(self.xor_btn)

        layout.addLayout(layout_OP)

    def ui_num_op_elements(self, layout, num_idx=0):
            layout_OP_BN = QHBoxLayout()
            self.sl_btn.append(QPushButton('<<', self))
            self.sl_btn[num_idx].clicked.connect(partial(self.sl_btn_clicked, num_idx))
            layout_OP_BN.addWidget(self.sl_btn[num_idx])

            self.not_btn.append(QPushButton('NOT', self))
            self.not_btn[num_idx].clicked.connect(partial(self.not_btn_clicked, num_idx))
            layout_OP_BN.addWidget(self.not_btn[num_idx])
            
            self.sign_btn.append(QPushButton('S', self))
            self.sign_btn[num_idx].clicked.connect(partial(self.sign_btn_clicked, num_idx))
            layout_OP_BN.addWidget(self.sign_btn[num_idx])

            self.clr_btn.append(QPushButton('CLR', self))
            self.clr_btn[num_idx].clicked.connect(partial(self.clr_btn_clicked, num_idx))
            layout_OP_BN.addWidget(self.clr_btn[num_idx])

            self.sr_btn.append(QPushButton('>>', self))
            self.sr_btn[num_idx].clicked.connect(partial(self.sr_btn_clicked, num_idx))
            layout_OP_BN.addWidget(self.sr_btn[num_idx])

            layout.addLayout(layout_OP_BN)

    def ui_modify_QSpinBox(self, obj, setPrefix="setPrefix", setMin=0, setMax=64, setVal=10, setAlignRight=False):
        obj.setPrefix(setPrefix)
        obj.setMinimum(setMin)
        obj.setMaximum(setMax)
        obj.setValue(setVal)
        obj.valueChanged.connect(self.update_input_values)
        if setAlignRight: obj.setAlignment(Qt.AlignRight)
        return

    def ui_number_elements(self, layout):
        layout_NUM = []
        self.spin_box_NIB = []
        self.spin_box_NFB = []
        self.spin_box_NB = []
        self.str_BN = []
        self.double_spin_box_FN = []
        self.shift_left_BN_btn = []
        self.sl_btn = []
        self.sr_btn = []
        self.clr_btn = []
        self.sign_btn = []
        self.not_btn = []
        self.BN_Format = 2
        self.bin_hex_int_mode = 0
        self.sat_flag = True
        for ii in range(3):
            if ii == 2:
                self.ui_op_elements(layout=layout)
                self.ui_splitter_line(layout=layout, is_hor=True, border_width=2)

            layout_NUM.append(QHBoxLayout())

            text_str = f"In Num {ii}:"
            if ii==2: text_str = f"Out Num:"
            self.ui_add_text(layout=layout_NUM[ii], in_text=text_str)
            self.ui_splitter_line(layout=layout_NUM[ii], is_hor=False, border_width=1)

            # Create horizontal layout for the spin boxes for Number of Integer, Fractional Bits and total Bithdepth
            layout_BIT_SET = QVBoxLayout()
            self.spin_box_NIB.append(QSpinBox())
            self.ui_modify_QSpinBox(self.spin_box_NIB[ii], setPrefix="#IntegerBits: ", setMin=0, setMax=64, setVal=5, setAlignRight=True)
            layout_BIT_SET.addWidget(self.spin_box_NIB[ii])

            self.spin_box_NFB.append(QSpinBox())
            self.ui_modify_QSpinBox(self.spin_box_NFB[ii], setPrefix="#FractionalBits: ", setMin=0, setMax=64, setVal=10, setAlignRight=True)
            layout_BIT_SET.addWidget(self.spin_box_NFB[ii])

            self.spin_box_NB.append(QSpinBox())
            self.ui_modify_QSpinBox(self.spin_box_NB[ii], setPrefix="#BitDepth: ", setMin=0, setMax=64, setVal=15, setAlignRight=True)
            layout_BIT_SET.addWidget(self.spin_box_NB[ii])
            layout_NUM[ii].addLayout(layout_BIT_SET)

            self.ui_splitter_line(layout=layout_NUM[ii], is_hor=False, border_width=1)

            layout_BN_FN_OP = QVBoxLayout()
            layout_BN_FN = QHBoxLayout()
            self.str_BN.append(QLineEdit())
            self.BN_Prefix = "Binary (s|I.F): "
            self.str_BN[ii].setText(self.BN_Prefix + str(0) * (self.spin_box_NB[ii].value()))
            self.str_BN[ii].setReadOnly(True)
            layout_BN_FN.addWidget(self.str_BN[ii])

            self.double_spin_box_FN.append(QDoubleSpinBox())
            setMin = -2**(self.spin_box_NB[ii].value()-1)
            setMax = 2**(self.spin_box_NB[ii].value()-1)
            setVal = 0
            self.ui_modify_QSpinBox(self.double_spin_box_FN[ii], setPrefix="Float: ", setMin=setMin, setMax=setMax, setVal=setVal)
            self.double_spin_box_FN[ii].setDecimals(self.spin_box_NFB[ii].value())
            self.double_spin_box_FN[ii].setSingleStep(2**(-self.spin_box_NFB[ii].value()))
            layout_BN_FN.addWidget(self.double_spin_box_FN[ii])

            layout_BN_FN_OP.addLayout(layout_BN_FN)

            self.ui_num_op_elements(layout=layout_BN_FN_OP, num_idx=ii)

            layout_NUM[ii].addLayout(layout_BN_FN_OP)
            layout.addLayout(layout_NUM[ii])

            # Add splitter line
            self.ui_splitter_line(layout=layout, is_hor=True, border_width=2)

    def ui_comm_window(self, layout):
        self.comm_Win_Line_Num = 1
        self.str_Comm_Window = QTextEdit()
        self.str_Comm_Window.setText("0 - Events History: ")
        self.str_Comm_Window.setReadOnly(True)
        layout.addWidget(self.str_Comm_Window)
        return

    def init_ui(self):
        # Create layout
        layout = QVBoxLayout()

        # Create UI elements
        self.ui_settings_elements(layout)
        self.ui_splitter_line(layout=layout, is_hor=True, border_width=2)
        self.ui_number_elements(layout)
        self.ui_comm_window(layout)

        self.setGeometry(500, 500, 1500, 1000) 

        # Set the layout for the main window
        self.setLayout(layout)

        # Set window properties
        self.setWindowTitle('Q-format (1+m+n) Helper')

        # Get the UI updated
        self.update_input_values()

        # Print that the UI is created
        print_text = "UI is created."
        self.update_comm_window(print_text)

    def show_result_numbers(self):
        [self.double_spin_box_FN[x].setValue(self.f_nums[x]) for x in range(len(self.f_nums))]
        self.show_binary_numbers()
        return
    
    def update_num_bits(self):
        self.NIBs = [self.spin_box_NIB[x].value() for x in range(len(self.spin_box_NIB))]
        self.NFBs = [self.spin_box_NFB[x].value() for x in range(len(self.spin_box_NFB))]
        self.NBs = [(self.NIBs[x] + self.NFBs[x] + 1)  for x in range(len(self.NIBs))]
        self.max_num_out = (2**(self.NBs[2]-1) - 1) / (2**self.NFBs[2])
        
        # Update the spinner internals
        [self.spin_box_NB[x].setValue(self.NBs[x]) for x in range(len(self.NIBs))]
        [self.double_spin_box_FN[x].setSingleStep(2**(-self.NFBs[x])) for x in range(len(self.NFBs))]
        [self.double_spin_box_FN[x].setMinimum(-2**(self.NBs[x]-1)) for x in range(len(self.NFBs))]
        [self.double_spin_box_FN[x].setMaximum(2**(self.NBs[x]-1)) for x in range(len(self.NFBs))]
        [self.double_spin_box_FN[x].setDecimals(self.NFBs[x]) for x in range(len(self.NFBs))]
        return

    def update_num_values(self):
        self.f_nums = [self.double_spin_box_FN[x].value() for x in range(len(self.double_spin_box_FN))]
        self.q_nums = [float2Q(f_num=self.f_nums[x], num_int_bits=self.NIBs[x], num_frac_bits=self.NFBs[x], bit_depth=self.NBs[x], sat=self.sat_flag, bin_format=self.BN_Format) for x in range(len(self.f_nums))]
        self.f_nums = [self.q_nums[x].q2Float() for x in range(len(self.double_spin_box_FN))]
        [self.double_spin_box_FN[x].setValue(self.f_nums[x]) for x in range(len(self.f_nums))]
        #print_text = "Number values are updated."
        #self.update_comm_window(print_text)
        return
    
    def print_single_binary_number(self, btn_idx=0):
        temp_str = str()
        qdata = self.q_nums[btn_idx].qdata
        cnt = 0
        for jj in range(self.NBs[btn_idx]-1):
            if cnt%4 == 0 and cnt != 0:
                temp_str = ' ' + temp_str
            
            if jj == self.NFBs[btn_idx]:
                temp_str = '.' + temp_str
                cnt = 0

            temp_str = qdata[self.NBs[btn_idx]-1-jj] + temp_str
            cnt = cnt + 1

        temp_str = self.BN_Prefix + qdata[0] + '|' + temp_str
        self.str_BN[btn_idx].setText(temp_str)

        print("Show Binary Number: Number: ", btn_idx, ": ", temp_str)

        return
    
    def print_single_hex_number(self, btn_idx=0):
        temp_str = str()
        qdata = self.q_nums[btn_idx].qdata
        hex_str = hex(int(qdata,2))
        
        temp_str = self.HEX_Prefix + hex_str[2:]
        self.str_BN[btn_idx].setText(temp_str)

        print("Show Hex Number: Number: ", btn_idx, ": ", temp_str)

        return
    
    def print_single_int_number(self, btn_idx=0):
        temp_str = str()
        qdata = self.q_nums[btn_idx].qdata
        int_str = str(int(qdata,2))
        if self.f_nums[btn_idx] < 0.0:
            temp_f_num = -self.f_nums[btn_idx]
            temp_q_nums = float2Q(f_num=temp_f_num, num_int_bits=self.NIBs[btn_idx], num_frac_bits=self.NFBs[btn_idx], bit_depth=self.NBs[btn_idx], sat=self.sat_flag, bin_format=self.BN_Format)
            qdata = temp_q_nums.qdata
            int_str = str(-int(qdata,2))

        temp_str = self.INT_Prefix + int_str
        self.str_BN[btn_idx].setText(temp_str)

        print("Show Int Number: Number: ", btn_idx, ": ", temp_str)

        return

    def show_binary_numbers(self):
        for ii in range(len(self.NBs)):
            if self.bin_hex_int_mode == 1:
                self.print_single_hex_number(btn_idx=ii)
            elif self.bin_hex_int_mode == 2:
                self.print_single_int_number(btn_idx=ii)
            else:
                self.print_single_binary_number(btn_idx=ii)
        return

    def update_input_values(self):
        self.update_num_bits()
        self.update_num_values()
        self.show_binary_numbers()
        return

    def sl_btn_clicked(self, btn_idx=0):
        self.q_nums[btn_idx] = self.q_nums[btn_idx].bitShiftLeft()
        self.f_nums[btn_idx] = self.q_nums[btn_idx].q2Float()
        self.double_spin_box_FN[btn_idx].setValue(self.f_nums[btn_idx])
        self.update_input_values()

        print_text = f"Shift left, Number: {btn_idx}"
        self.update_comm_window(print_text)
        return

    def sr_btn_clicked(self, btn_idx=0):
        self.q_nums[btn_idx] = self.q_nums[btn_idx].bitShiftRight()
        self.f_nums[btn_idx] = self.q_nums[btn_idx].q2Float()
        self.double_spin_box_FN[btn_idx].setValue(self.f_nums[btn_idx])
        self.update_input_values()

        print_text = f"Shift right, Number: {btn_idx}"
        self.update_comm_window(print_text)
        return

    def clr_btn_clicked(self, btn_idx=0):
        self.q_nums[btn_idx] = self.q_nums[btn_idx].clr()
        self.f_nums[btn_idx] = self.q_nums[btn_idx].q2Float()
        self.double_spin_box_FN[btn_idx].setValue(self.f_nums[btn_idx])
        self.update_input_values()
        
        print_text = f"Clear, Number: {btn_idx}"
        self.update_comm_window(print_text)
        return

    def sign_btn_clicked(self, btn_idx=0):
        self.q_nums[btn_idx] = self.q_nums[btn_idx].signToggle()
        self.f_nums[btn_idx] = self.q_nums[btn_idx].q2Float()
        self.double_spin_box_FN[btn_idx].setValue(self.f_nums[btn_idx])
        self.update_input_values()

        print_text = f"Change sign, Number: {btn_idx}"
        self.update_comm_window(print_text)
        return

    def not_btn_clicked(self, btn_idx=0):
        self.q_nums[btn_idx] = self.q_nums[btn_idx].inv()
        self.f_nums[btn_idx] = self.q_nums[btn_idx].q2Float()
        self.double_spin_box_FN[btn_idx].setValue(self.f_nums[btn_idx])
        self.update_input_values()
        
        print_text = f"Apply bitwise NOT, Number: {btn_idx}"
        self.update_comm_window(print_text)
        return

    def adjust_bitdepth_flag_check_clicked(self):
        self.adjust_BDepth = self.adjust_bitdepth_flag_check.isChecked()
        
        print_text = f"Adjust BitDepth Flag Setting: {self.adjust_BDepth}"
        self.update_comm_window(print_text)
        return

    def sat_flag_check_clicked(self):
        self.sat_flag = self.sat_flag_check.isChecked()
        
        print_text = f"Saturation Flag Setting: {self.sat_flag}"
        self.update_comm_window(print_text)
        return
    
    def update_BN_Format(self):
        self.BN_Format = self.bin_fmt_cb.currentIndex()
        self.update_input_values()

        print_text = f"Update Binary Number Format. New format: {self.bin_fmt_cb.currentText()}"
        self.update_comm_window(print_text)
        return
    
    def bin_hex_int_btn_clicked(self):
        self.bin_hex_int_mode += 1
        self.bin_hex_int_mode %= 3

        self.show_binary_numbers()

        print_text = f"Toggle the number view."
        self.update_comm_window(print_text)
        return

    def adjust_spin_box_NIB(self, num=0):
        self.spin_box_NIB[2].setValue(round(math.log2(num)+0.5))

        print_text = f"WARNING: Output BitDepth is adjusted to {self.NBs[2]} bits."
        self.update_comm_window(print_text)
        return
    
    def sum_btn_clicked(self):
        print_text = f"Summing the numbers."
        self.update_comm_window(print_text)

        temp_f_num_op = abs(self.f_nums[0] + self.f_nums[1])
        if temp_f_num_op > self.max_num_out:
            print_text = f"WARNING: Overflow due to {self.NBs[2]} bits in output."
            self.update_comm_window(print_text)
            if self.adjust_BDepth is True:
                self.adjust_spin_box_NIB(num=temp_f_num_op)

        self.q_nums[2] = qSum(self.q_nums[0], self.q_nums[1], self.q_nums[2], sat=self.sat_flag)
        self.f_nums[2] = self.q_nums[2].q2Float()
        self.show_result_numbers()
        
        return

    def sub_btn_clicked(self):
        print_text = f"Subtracting the numbers."
        self.update_comm_window(print_text)

        temp_f_num_op = abs(self.f_nums[0] - self.f_nums[1])
        if temp_f_num_op > self.max_num_out:
            print_text = f"WARNING: Overflow due to {self.NBs[2]} bits in output."
            self.update_comm_window(print_text)
            if self.adjust_BDepth is True:
                self.adjust_spin_box_NIB(num=temp_f_num_op)

        self.q_nums[2] = qSub(self.q_nums[0], self.q_nums[1], self.q_nums[2], sat=self.sat_flag)
        self.f_nums[2] = self.q_nums[2].q2Float()
        self.show_result_numbers()
        return
    
    def mul_btn_clicked(self):
        print_text = f"Multiplying the numbers."
        self.update_comm_window(print_text)
        
        temp_f_num_op = abs(self.f_nums[0] * self.f_nums[1])
        if temp_f_num_op > self.max_num_out:
            print_text = f"WARNING: Overflow due to {self.NBs[2]} bits in output."
            self.update_comm_window(print_text)
            if self.adjust_BDepth is True:
                self.adjust_spin_box_NIB(num=temp_f_num_op)

        self.q_nums[2] = qMul(self.q_nums[0], self.q_nums[1], self.q_nums[2], sat=self.sat_flag)
        self.f_nums[2] = self.q_nums[2].q2Float()
        self.show_result_numbers()
        return

    def div_btn_clicked(self):
        FLT_EPS = 2.220446049250313e-16
        print_text = f"Dividing the numbers."
        self.update_comm_window(print_text)

        temp_f_num_op = abs(self.f_nums[0] / (self.f_nums[1]+FLT_EPS))
        if temp_f_num_op > self.max_num_out:
            print_text = f"WARNING: Overflow due to {self.NBs[2]} bits in output."
            self.update_comm_window(print_text)
            if self.adjust_BDepth is True:
                self.adjust_spin_box_NIB(num=temp_f_num_op)

        self.q_nums[2] = qDiv(self.q_nums[0], self.q_nums[1], self.q_nums[2], sat=self.sat_flag)
        self.f_nums[2] = self.q_nums[2].q2Float()
        self.show_result_numbers()
        return

    def are_bitdepths_same(self):
        if self.q_nums[0].bit_depth == self.q_nums[1].bit_depth == self.q_nums[2].bit_depth:
            return True

        return False

    def and_btn_clicked(self):
        if not self.are_bitdepths_same():
            print_text = f"WARNING: Cannot perform Bitwise operations: Bitdepths are different between the numbers (including output number)."
            self.update_comm_window(print_text)
            return
        
        print_text = f"Bitwise AND the numbers."
        self.update_comm_window(print_text)

        self.q_nums[2] = qAnd(self.q_nums[0], self.q_nums[1], self.q_nums[2])
        self.f_nums[2] = self.q_nums[2].q2Float()
        self.show_result_numbers()
        return

    def or_btn_clicked(self):
        if not self.are_bitdepths_same():
            print_text = f"WARNING: Cannot perform Bitwise operations: Bitdepths are different between the numbers (including output number)."
            self.update_comm_window(print_text)
            return
        
        print_text = f"Bitwise OR the numbers."
        self.update_comm_window(print_text)

        self.q_nums[2] = qOr(self.q_nums[0], self.q_nums[1], self.q_nums[2])
        self.f_nums[2] = self.q_nums[2].q2Float()
        self.show_result_numbers()
        return

    def nand_btn_clicked(self):
        if not self.are_bitdepths_same():
            print_text = f"WARNING: Cannot perform Bitwise operations: Bitdepths are different between the numbers (including output number)."
            self.update_comm_window(print_text)
            return
        
        print_text = f"Bitwise NAND the numbers."
        self.update_comm_window(print_text)

        self.q_nums[2] = qNand(self.q_nums[0], self.q_nums[1], self.q_nums[2])
        self.f_nums[2] = self.q_nums[2].q2Float()
        self.show_result_numbers()
        return

    def nor_btn_clicked(self):
        if not self.are_bitdepths_same():
            print_text = f"WARNING: Cannot perform Bitwise operations: Bitdepths are different between the numbers (including output number)."
            self.update_comm_window(print_text)
            return
        
        print_text = f"Bitwise NOR the numbers."
        self.update_comm_window(print_text)

        self.q_nums[2] = qNor(self.q_nums[0], self.q_nums[1], self.q_nums[2])
        self.f_nums[2] = self.q_nums[2].q2Float()
        self.show_result_numbers()
        return

    def xor_btn_clicked(self):
        if not self.are_bitdepths_same():
            print_text = f"WARNING: Cannot perform Bitwise operations: Bitdepths are different between the numbers (including output number)."
            self.update_comm_window(print_text)
            return

        print_text = f"Bitwise XOR the numbers."
        self.update_comm_window(print_text)

        self.q_nums[2] = qXor(self.q_nums[0], self.q_nums[1], self.q_nums[2])
        self.f_nums[2] = self.q_nums[2].q2Float()
        self.show_result_numbers()
        return

def main():
    app = QApplication(sys.argv)

    # Set global font size
    font = QFont()
    font.setPointSize(12)  # Set font size to 14
    app.setFont(font)

    window = QNumberHelperApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()