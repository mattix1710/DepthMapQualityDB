@REM %0 - the executable (batch file) name as specified in the command line;
@REM %1 - first argument etc...;

SET FORMAT=yuv420p
SET FORMAT_16=yuv420p16le
SET WIDTH=1920

SET FOLDER_LOCATION=%1
SET TERMINAL_PATH=%2
SET METHOD_PATH=%3
SET METHOD_NAME=%4
SET SEQ_NAME=%5
SET QP_DEPTH=%6

SET START=0
SET STEP=1
IF %SEQ_NAME%==PoznanFencing (
    SET HEIGHT=1080
    SET STOP=9
    SET IN_NAME_DEPTH=depth_1920x1080_yuv400p16le.yuv
    SET PROCESS_DEPTH_420=depth_1920x1080_yuv420p16le.yuv
    SET IN_NAME_SYNTH=synth_1920x1080_yuv420p8le.yuv
    SET ENC_DEPTH_420=depth_1920x1080_yuv420p16le_ENC.yuv
)

IF %SEQ_NAME%==Carpark (
    SET HEIGHT=1088
    SET STOP=8
    SET IN_NAME_DEPTH=depth_1920x1088_yuv400p16le.yuv
    SET PROCESS_DEPTH_420=depth_1920x1088_yuv420p16le.yuv
    SET IN_NAME_SYNTH=synth_1920x1088_yuv420p8le.yuv
    SET ENC_DEPTH_420=depth_1920x1088_yuv420p16le_ENC.yuv
)

SET PROCESS_DEPTH_MP4=ENCODED_depth
SET COMPRESSED_SYNTH=synth_COMPRESSED.mp4
SET QP_SYNTH=20

SET TEMP_FOLDER=_TEMP

@REM INFO: paths are working with backslashes only "\", not "/"

@REM =================================================================
@REM                 -- START SEQUENCE PROCESSING --
@REM =================================================================
MKDIR .\media\%FOLDER_LOCATION%\%TEMP_FOLDER%\
@REM IF temp directory exists, empty folder
DEL .\media\%FOLDER_LOCATION%\%TEMP_FOLDER%\*.* /Q

@REM -----------------------------------
@REM       -- DEPTH PROCESSING --
@REM -----------------------------------

@REM Depth is processed in a few steps...
@REM 1) chroma needs to be changed from 4:0:0 to 4:2:0 due to ffmpeg limitations (it only uses chroma 4:2:0)
@REM 2) depth map is compressed depending on QP_DEPTH setting (to .mp4 file)
@REM 3) depth is converted back to .yuv file, but still has chroma 4:2:0
@REM 4) chroma is converted back to 4:0:0
@REM 5) such prepared depth can be used for further processing (eg. synthesis)

IF %QP_DEPTH%==raw GOTO raw_data
@REM DEPTH compression
FOR /l %%c IN (%START%, %STEP%, %STOP%) DO (
    .\media\media_handling\fc8.1.exe "./media/%FOLDER_LOCATION%/%SEQ_NAME%/v%%c_%IN_NAME_DEPTH%" -iw %WIDTH% -ih %HEIGHT% -ics 400 -ocs 420 -w %WIDTH% -h %HEIGHT% -o "./media/%FOLDER_LOCATION%/%TEMP_FOLDER%/v%%c_%PROCESS_DEPTH_420%"
    .\media\media_handling\ffmpeg.exe -f rawvideo -pix_fmt %FORMAT_16% -s:v %WIDTH%x%HEIGHT% -r 25 -i "./media/%FOLDER_LOCATION%/%TEMP_FOLDER%/v%%c_%PROCESS_DEPTH_420%" -c:v libx265 -crf %QP_DEPTH% -pix_fmt %FORMAT% "./media/%FOLDER_LOCATION%/%TEMP_FOLDER%/v%%c_%PROCESS_DEPTH_MP4%_%QP_DEPTH%.mp4"
    DEL ".\media\%FOLDER_LOCATION%\%TEMP_FOLDER%\v%%c_%PROCESS_DEPTH_420%" /Q

    .\media\media_handling\ffmpeg.exe -i "./media/%FOLDER_LOCATION%/%TEMP_FOLDER%/v%%c_%PROCESS_DEPTH_MP4%_%QP_DEPTH%.mp4" -f rawvideo -pix_fmt %FORMAT_16% "./media/%FOLDER_LOCATION%/%TEMP_FOLDER%/v%%c_%ENC_DEPTH_420%"
    .\media\media_handling\fc8.1.exe "./media/%FOLDER_LOCATION%/%TEMP_FOLDER%/v%%c_%ENC_DEPTH_420%" -iw %WIDTH% -ih %HEIGHT% -ibps 16 -ics 420 -ocs 400 -w %WIDTH% -h %HEIGHT% -o "./media/%FOLDER_LOCATION%/%TEMP_FOLDER%/v%%c_%IN_NAME_DEPTH%"
    DEL ".\media\%FOLDER_LOCATION%\%TEMP_FOLDER%\v%%c_%PROCESS_DEPTH_MP4%_%QP_DEPTH%.mp4" /Q
    DEL ".\media\%FOLDER_LOCATION%\%TEMP_FOLDER%\v%%c_%ENC_DEPTH_420%" /Q
)

GOTO :texture
:raw_data
XCOPY ".\media\%FOLDER_LOCATION%\%SEQ_NAME%\*.*" ".\media\%FOLDER_LOCATION%\%TEMP_FOLDER%\"

@REM -----------------------------------
@REM  -- TEXTURES & PROGRAMS COPYING --
@REM -----------------------------------
:texture
@REM copy textures with appropriate compression to %TEMP_FOLDER%
IF %QP_DEPTH%==10 XCOPY ".\media\seq_textures\%SEQ_NAME%_texture\%SEQ_NAME%_QP_18\*.*" ".\media\%FOLDER_LOCATION%\%TEMP_FOLDER%\"
IF %QP_DEPTH%==30 XCOPY ".\media\seq_textures\%SEQ_NAME%_texture\%SEQ_NAME%_QP_42\*.*" ".\media\%FOLDER_LOCATION%\%TEMP_FOLDER%\"
IF %QP_DEPTH%==raw XCOPY ".\media\seq_textures\%SEQ_NAME%_texture\%SEQ_NAME%_raw\*.*" ".\media\%FOLDER_LOCATION%\%TEMP_FOLDER%\"

@REM results will be placed in %TEMP_FOLDER%

@REM copy PoznanFencing scripts to the sequence folder
XCOPY ".\media\media_handling\seq_synth\%SEQ_NAME%\*.*" ".\media\%FOLDER_LOCATION%\%TEMP_FOLDER%\"
@REM copy synthesizing & paralleling app to the sequence folder
XCOPY ".\media\media_handling\TAppVvs.exe" ".\media\%FOLDER_LOCATION%\%TEMP_FOLDER%\"
XCOPY ".\media\media_handling\MParallel.exe" ".\media\%FOLDER_LOCATION%\%TEMP_FOLDER%\"

@REM -----------------------------------
@REM         -- SYNTH VIEWS --
@REM -----------------------------------
CD .\media\%FOLDER_LOCATION%\%TEMP_FOLDER%\
START /WAIT %SEQ_NAME%.bat

CD %TERMINAL_PATH%

@REM -----------------------------------
@REM    -- GATHER PSNR & BITRATE --
@REM -----------------------------------
@REM gather PSNR data of created synths
CALL .\media\media_handling\IV_PSNR.bat %FOLDER_LOCATION%\%TEMP_FOLDER% %METHOD_PATH% %METHOD_NAME% %SEQ_NAME% %QP_DEPTH%

@REM compress synths and gather bitrate
FOR /l %%c IN (%START%, %STEP%, %STOP%) DO (
    .\media\media_handling\ffmpeg.exe -f rawvideo -pix_fmt %FORMAT% -s:v %WIDTH%:%HEIGHT% -r 25 -i ".\media\%FOLDER_LOCATION%\%TEMP_FOLDER%\v%%c_%IN_NAME_SYNTH%" -c:v libx265 -crf %QP_SYNTH% -pix_fmt %FORMAT% ".\media\%FOLDER_LOCATION%\%TEMP_FOLDER%\v%%c_%COMPRESSED_SYNTH%"
)
@REM gather bitrate and save it to txt file
CALL py %TERMINAL_PATH%\media\media_handling\gatherBitrate.py %TERMINAL_PATH%\media\%FOLDER_LOCATION%\%TEMP_FOLDER%\ %SEQ_NAME% %METHOD_NAME% %QP_DEPTH%

@REM =================================================================
@REM                -- END OF SEQUENCE PROCESSING --
@REM =================================================================

@REM cleaning unpacked data
RMDIR .\media\%FOLDER_LOCATION%\%TEMP_FOLDER% /s /q