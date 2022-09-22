SET START=0
SET STEP=1
SET STOP=2

.\MParallel.exe --count=3 .\TAppVvs.exe -c PoznanFencing_VVS_0.cfg : .\TAppVvs.exe -c PoznanFencing_VVS_1.cfg : .\TAppVvs.exe -c PoznanFencing_VVS_2.cfg

ECHO ENDED!!

EXIT