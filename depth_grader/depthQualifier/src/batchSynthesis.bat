@REM @ECHO off

@REM %0 - the executable (batch file) name as specified in the command line;
@REM %1 - first argument;

@REM get current directory from terminal - from PYTHON doesn't work
SET TERMINAL_PATH = %CD%
SET BATCH_PATH = %~dp0

SET FORMAT=yuv420p
SET FORMAT_16=yuv420p16le
SET WIDTH=1920
SET HEIGHT=1080

SET START=0
SET STEP=1
SET STOP=9

SET FOLDER_LOCATION=%1
SET IN_NAME_TEXTURE=texture_1920x1080_yuv420p8le.yuv
SET PROCESS_TEXTURE_MP4=ENCODED_texture

SET IN_NAME_DEPTH=depth_1920x1080_yuv400p16le.yuv
SET PROCESS_DEPTH_420=depth_1920x1080_yuv420p16le.yuv
SET PROCESS_DEPTH_MP4=ENCODED_depth

SET ENC_DEPTH_420=depth_1920x1080_yuv420p16le_ENC.yuv

SET QP_DEPTH=18
SET QP_TEXT=24

@REM CD %BATCH_PATH%
@REM CD "./media/%FOLDER_LOCATION%"

@REM INFO: paths are working with backslashes only "\", not "/"

@REM media\raw_textures\PoznanFencing_texture

@REM TEXTURE CODING

FOR /l %%c IN (%START%, %STEP5, %STOP%) DO (
    .\media\media_handling\ffmpeg.exe -f rawvideo -pix_fmt %FORMAT% -s:v %WIDTH%:%HEIGHT% -r 25 -i ".\media\raw_textures\PoznanFencing_texture\v%%c_%IN_NAME_TEXTURE%" -c:v libx265 -crf %QP_TEXT% -pix_fmt yuv420p ".\media\%FOLDER_LOCATION%\v%%c_%PROCESS_TEXTURE_MP4%_%QP_TEXT%.mp4"
    .\media\media_handling\ffmpeg.exe -i ".\media\%FOLDER_LOCATION%\v%%c_%PROCESS_TEXTURE_MP4%_%QP_TEXT%.mp4" -f rawvideo -pix_fmt %FORMAT% ".\media\%FOLDER_LOCATION%\v%%c_%IN_NAME_TEXTURE%"
    DEL ".\media\%FOLDER_LOCATION%\v%%c_%PROCESS_TEXTURE_MP4%_%QP_TEXT%.mp4" /Q
)

@REM TODO: rethink PoznanFencing...