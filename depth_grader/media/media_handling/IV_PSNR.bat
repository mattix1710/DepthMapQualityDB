setlocal enableDelayedExpansion

set NFRAMES=5

SET CURR_PATH=%1

for /l %%c in (0,1,9)   do ".\media\media_handling\IV_PSNR.exe" -i0 ".\media\%CURR_PATH%\v%%c_texture_1920x1080_yuv420p8le.yuv"  -i1 ".\media\%CURR_PATH%\v%%c_synth_1920x1080_yuv420p8le.yuv" -w 1920 -h 1080 -l %NFRAMES% -bd 8 -cf 420 -o .\media\%CURR_PATH%\ivpsnr_SL.txt