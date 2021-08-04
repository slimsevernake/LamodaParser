# exporting evn vars to run python correctly:
if [ -z $PYTHONPATH ]; then 
	export PYTHONPATH=$HOME/LMonitorV1-3/:$HOME/LParserVenv/Lib/site-packages;
else
	echo "PYTHONPATH is set"
fi


# checking current dir
current_dir=${PWD##*/}
if [ "$current_dir" != "LMonitorV1-3" ]; then
	echo "!!! You should be located in the root of the project in order to start the bot !!!";
	echo "Quiting"
else
    echo "Adding execute permissions to script!"
    chmod +x LamodaBot/bot.py
	echo "Starting the bot!"	
	nohup /opt/python/python-3.8.8/bin/python3 LamodaBot/bot.py &
fi
