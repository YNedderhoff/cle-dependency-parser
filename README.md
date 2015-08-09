# cle-dependency-parser
[![Code Issues](http://www.quantifiedcode.com/api/v1/project/18eed7d238484444811520e549c1a50d/badge.svg)](http://www.quantifiedcode.com/app/project/18eed7d238484444811520e549c1a50d)

Configure start-cle.sh to tell the programm what to do. (Train, Test, ...)

Training, Dev and Test Data has to be in ConLL06-Format (http://ilk.uvt.nl/conll/#dataformat)

Performance:

Models:

1. 1 epoch, alpha = 0.5
2. 10 epochs, alpha = 0.5
3. 10 epochs, alpha = 0.5, alpha-decreasing

English test data (F-Score in %):

| Model         | UAS           | CS    |
| ------------- |:-------------:| -----:|
| 1             | 83.0          | 13.0  |
| 2             | 87.0          | 19.0  |
| 3             | 87.0          | 18.0  |

German test data (F-Score in %):

| Model         | UAS           | CS    |
| ------------- |:-------------:| -----:|
| 1             | 85.0          | 31.0  |
| 2             | 88.0          | 37.0  |
| 3             | 89.0          | 39.0  |
