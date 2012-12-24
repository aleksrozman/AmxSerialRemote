vol=`zenity --scale --text="TV Volume" --value=75 --min-value=0 --max-value=100 --step=5`
volume_control $vol
