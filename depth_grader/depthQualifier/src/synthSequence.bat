@REM %0 - the executable (batch file) name as specified in the command line;
@REM %1 - first argument etc...;

@REM get current directory from terminal - from PYTHON doesn't work

SET FORMAT=yuv420p
SET FORMAT_16=yuv420p16le
SET WIDTH=1920
SET HEIGHT=1080

SET START=0
SET STEP=1
SET STOP=9

SET FOLDER_LOCATION=%1
SET TERMINAL_PATH=%2
SET SEQ_PATH=%3
SET SEQ_NAME=%4

SET IN_NAME_TEXTURE=texture_1920x1080_yuv420p8le.yuv
SET PROCESS_TEXTURE_MP4=ENCODED_texture

SET IN_NAME_DEPTH=depth_1920x1080_yuv400p16le.yuv
SET PROCESS_DEPTH_420=depth_1920x1080_yuv420p16le.yuv
SET PROCESS_DEPTH_MP4=ENCODED_depth

SET ENC_DEPTH_420=depth_1920x1080_yuv420p16le_ENC.yuv

SET QP_DEPTH=18
SET QP_TEXT=24

@REM INFO: paths are working with backslashes only "\", not "/"

@REM DEPTH compression
FOR /l %%c IN (%START%, %STEP%, %STOP%) DO (
    .\media\media_handling\fc8.1.exe "./media/%FOLDER_LOCATION%/v%%c_%IN_NAME_DEPTH%" -iw %WIDTH% -ih %HEIGHT% -ics 400 -ocs 420 -w %WIDTH% -h %HEIGHT% -o "./media/%FOLDER_LOCATION%/v%%c_%PROCESS_DEPTH_420%"
    .\media\media_handling\ffmpeg.exe -f rawvideo -pix_fmt %FORMAT_16% -s:v %WIDTH%:%HEIGHT% -r 25 -i "./media/%FOLDER_LOCATION%/v%%c_%PROCESS_DEPTH_420%" -c:v libx265 -crf %QP_DEPTH% -pix_fmt yuv420p "./media/%FOLDER_LOCATION%/v%%c_%PROCESS_DEPTH_MP4%_%QP_DEPTH%.mp4"
    DEL ".\media\%FOLDER_LOCATION%\v%%c_%IN_NAME_DEPTH%" /Q
    DEL ".\media\%FOLDER_LOCATION%\v%%c_%PROCESS_DEPTH_420%" /Q

    .\media\media_handling\ffmpeg.exe -i ".\media\%FOLDER_LOCATION%\v%%c_%PROCESS_DEPTH_MP4%_%QP_DEPTH%.mp4" -f rawvideo -pix_fmt %FORMAT_16% ".\media\%FOLDER_LOCATION%\v%%c_%ENC_DEPTH_420%"
    .\media\media_handling\fc8.1.exe ".\media\%FOLDER_LOCATION%\v%%c_%ENC_DEPTH_420%" -iw %WIDTH% -ih %HEIGHT% -ibps 16 -ics 420 -ocs 400 -w %WIDTH% -h %HEIGHT% -o ".\media\%FOLDER_LOCATION%\v%%c_%IN_NAME_DEPTH%"
    DEL ".\media\%FOLDER_LOCATION%\v%%c_%PROCESS_DEPTH_MP4%_%QP_DEPTH%.mp4" /Q
    DEL ".\media\%FOLDER_LOCATION%\v%%c_%ENC_DEPTH_420%" /Q
)

@REM TEXTURE CODING

FOR /l %%c IN (%START%, %STEP%, %STOP%) DO (
    .\media\media_handling\ffmpeg.exe -f rawvideo -pix_fmt %FORMAT% -s:v %WIDTH%:%HEIGHT% -r 25 -i ".\media\raw_textures\PoznanFencing_texture\v%%c_%IN_NAME_TEXTURE%" -c:v libx265 -crf %QP_TEXT% -pix_fmt yuv420p ".\media\%FOLDER_LOCATION%\v%%c_%PROCESS_TEXTURE_MP4%_%QP_TEXT%.mp4"
    @REM TODO: sprawdzić, czy DEL ma tu sens - wydaje się, że nie...
    DEL ".\media\%FOLDER_LOCATION%\v%%c_%IN_NAME_TEXTURE%" /Q
    .\media\media_handling\ffmpeg.exe -i ".\media\%FOLDER_LOCATION%\v%%c_%PROCESS_TEXTURE_MP4%_%QP_TEXT%.mp4" -f rawvideo -pix_fmt %FORMAT% ".\media\%FOLDER_LOCATION%\v%%c_%IN_NAME_TEXTURE%"
    DEL ".\media\%FOLDER_LOCATION%\v%%c_%PROCESS_TEXTURE_MP4%_%QP_TEXT%.mp4" /Q
)

@REM TODO: rethink PoznanFencing...

@REM copy PoznanFencing scripts to the sequence folder
XCOPY ".\media\media_handling\PoznanFencing\*.*" ".\media\%FOLDER_LOCATION%\"
@REM copy synthesizing & paralleling app to the sequence folder
XCOPY ".\media\media_handling\TAppVvs.exe" ".\media\%FOLDER_LOCATION%\"
XCOPY ".\media\media_handling\MParallel.exe" ".\media\%FOLDER_LOCATION%\"

CD .\media\%FOLDER_LOCATION%\

START /WAIT PoznanFencing.bat

CD %TERMINAL_PATH%

CALL .\media\media_handling\IV_PSNR.bat %FOLDER_LOCATION% %SEQ_PATH% %SEQ_NAME%

@REM CALL py "%TERMINAL_PATH%\media\media_handling\retrievingPSNRdata.py"

@REM cleaning data
RMDIR .\media\%FOLDER_LOCATION% /s /q