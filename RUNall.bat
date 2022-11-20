@REM calling will open new terminal window <- it is important due to the need of 3 concurrent windows open
@REM -----------------------------------------------
@REM First: for Redis message broker working in WSL
@REM Second: for Celery task queueing service
@REM Third: for running python-based Django project
@REM ===============================================

@REM running Redis-server
START CMD /k wsl.exe "redis-server"

@REM assuming the location of this file is in the root folder
@REM opening the main project folder
CD depth_grader

@REM running Celery broker
START CMD /k python -m celery -A depth_grader worker -l info -P gevent

@REM running Django project
START CMD /k python manage.py runserver