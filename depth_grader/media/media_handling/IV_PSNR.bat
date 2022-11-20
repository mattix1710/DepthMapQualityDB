@REM IVPSNR gitlab src: https://gitlab.com/mpeg-i-visual/ivpsnr
setlocal enableDelayedExpansion

set NFRAMES=5

SET CURR_PATH=%1
SET SEQ_PATH=%2
SET SEQ_NAME=%3

SET START=0
SET STEP=1
SET STOP=2

for /l %%c in (%START%, %STEP%, %STOP%)   do ".\media\media_handling\IV_PSNR.exe" -i0 ".\media\%CURR_PATH%\v%%c_texture_1920x1080_yuv420p8le.yuv"  -i1 ".\media\%CURR_PATH%\v%%c_synth_1920x1080_yuv420p8le.yuv" -w 1920 -h 1080 -l %NFRAMES% -bd 8 -cf 420 -o .\media\%SEQ_PATH%\ivpsnr_SL_%SEQ_NAME%.txt