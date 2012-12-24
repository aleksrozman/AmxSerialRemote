channel=`zenity --title="CH Presets" --list --text="Choose a channel" --column="Channel Number" --column="Channel Presets" --hide-column=1 \
"3" "MY TV" \
"8" "ABC" \
"10" "NBC" \
"11" "FOX" \
"12" "CW" \
"17" "TBS" \
"27" "Comedy" \
"29" "TNT" \
"32" "ABC Family" \
"37" "History" \
"38" "Discovery" \
"55" "Cartoon" \
"59" "FX" \
"60" "Fox News" \
"80" "Science" \
"93" "Sci-Fi"`
channel_changer $channel
