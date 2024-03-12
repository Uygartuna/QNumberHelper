# QNumberHelper
A handy helper for operations with Q-format numbers.

# Installation
Create the environment and make sure that you installed the packages as given in the requirements.txt

conda create --name <env> --file requirements.txt
conda activate <env> 

# Running the UI
execute

RunHelper

or run via the command below

python QNumberHelperUI.py

# Some Notes
## QNum Class
You can get the QNum class from QNumber/QNumber.py. It includes the definition of the QNum class together with some private and public methods. The class assumes Qm.n format as explained in https://en.wikipedia.org/wiki/Q_(number_format). So the total bitdepth includes the sign bit as well, bit_depth = 1 (sign bit) + num_int_bits + num_frac_bits.

Negative numbers can be represented in various ways, sign_magnitude, 1's compement, 2's complement. The default representation is 2's complement

Note that some of the operations defined for the negative numbers, such as bit shift, division etc. are highly implementation dependent. Therefore, it would be beneficial to look into their implementation before using.

## User Interface
Enjoy!