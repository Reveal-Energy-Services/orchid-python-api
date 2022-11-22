import pythonnet
pythonnet.load('netfx')

import clr
from System import DateTimeOffset, TimeSpan

print('108 == DateTimeOffset.MaxValue')
try:
    108 == DateTimeOffset.MaxValue
except TypeError as te:
    print(f'{te}')

print('108 == TimeSpan.MaxValue')
try:
    108 == TimeSpan.MaxValue
except TypeError as te:
    print(f'{te}')

print('108 == TimeSpan.MinValue')
try:
    108 == TimeSpan.MinValue
except TypeError as te:
    print(f'{te}')
