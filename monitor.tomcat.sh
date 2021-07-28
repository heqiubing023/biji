#!/bin/bash
tomcat_home='/data/apache-tomcat-8.5.11/'
SHUTDOWN='$tomcat_home/bin/shutdown.sh'
STARTTOMCAT='$tomcat_home/bin/startup.sh'
url='http://172.29.207.41:9090/ns/door/#/main/user'
code=`curl -I -m 30 -o /dev/null -s -w %{http_code}"\n" $url`


echo "访问时间是：`date '+%Y%m%d %H:%M:%S'`--$code--->$url" >>  /var/log/monitor.tomcat.visit.log  

if [  $code  -eq  200 ];then

        echo "Tomcat运行正常,时间为:`date '+%Y%m%d %H:%M:%S'`" 

else
        echo "再次判断"
                if [  $code  -eq  200 ];then
                        echo "网页真的运行正常!!!"
                else
                        echo "这次真的要重新启动!!!时间为:`date '+%Y%m%d %H:%M:%S'`"

                        ps -ef|grep tomcat |awk  'NR==1{ print $2}' | xargs kill -9
                        cd /data/apache-tomcat-8.5.11/bin/
                        bash startup.sh &
                fi
fi 

