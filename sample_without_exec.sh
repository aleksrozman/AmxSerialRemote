if [ -e ~/tvmuteon ]
then
 echo -n "off[156,3]\r" > /dev/ttyS0
 mv tvmuteon tvmuteoff
else
 echo -n "on[156,3]\r" > /dev/ttyS0
 mv tvmuteoff tvmuteon
fi
 
