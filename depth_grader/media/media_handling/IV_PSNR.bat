@REM IVPSNR gitlab src: https://gitlab.com/mpeg-i-visual/ivpsnr
setlocal enableDelayedExpansion

set NFRAMES=5

SET CURR_PATH=%1
SET METHOD_PATH=%2
SET METHOD_NAME=%3
SET SEQ_NAME=%4
SET COMPRESSION_FACTOR=%5

@REM TODO: na koniec zmienić na 0..9 (wszystkie widoki)
SET START=0
SET STEP=1

IF %SEQ_NAME%==PoznanFencing (
    SET STOP=9
    FOR /l %%c IN (%START%, %STEP%, %STOP%) DO ".\media\media_handling\IV_PSNR.exe" -i0 ".\media\%CURR_PATH%\v%%c_texture_1920x1080_yuv420p8le.yuv" -i1 ".\media\%CURR_PATH%\v%%c_synth_1920x1080_yuv420p8le.yuv" -w 1920 -h 1080 -l %NFRAMES% -bd 8 -cf 420 -o .\media\%METHOD_PATH%\ivpsnr_SL_%METHOD_NAME%_%SEQ_NAME%_%COMPRESSION_FACTOR%.txt
)

IF %SEQ_NAME%==Carpark (
    SET STOP=8
    FOR /l %%c IN (%START%, %STEP%, %STOP%) DO ".\media\media_handling\IV_PSNR.exe" -i0 ".\media\%CURR_PATH%\v%%c_texture_1920x1088_yuv420p8le.yuv" -i1 ".\media\%CURR_PATH%\v%%c_synth_1920x1088_yuv420p8le.yuv" -w 1920 -h 1080 -l %NFRAMES% -bd 8 -cf 420 -o .\media\%METHOD_PATH%\ivpsnr_SL_%METHOD_NAME%_%SEQ_NAME%_%COMPRESSION_FACTOR%.txt
)