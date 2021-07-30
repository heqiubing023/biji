#!/bin/bash

#计入计划任务每5分钟执行一次，输出日志到指定文件： 
#crontab -e: */5 * * * * bash  /home/createw/monitor.web.sh   >> /var/log/monitor.output.log 2>&1

#变量=tomcat的安装路径
tomcat_home='/data/apache-tomcat-8.5.11/'

#变量=tomcat的关闭路径
SHUTDOWN='$tomcat_home/bin/shutdown.sh'

#变量=tomcat的启动路径
STARTTOMCAT='$tomcat_home/bin/startup.sh'

#变量=tomcat的页面访问路径
url='http://172.29.207.41:9090/ns/door/#/main/user'

#变量=访问tomcat页面，只需要返回值：200
code=`curl -I -m 30 -o /dev/null -s -w %{http_code}"\n" $url`


#记录访问时间,输出到指定日志文件,没有这个文件会自动创建
echo "访问时间是：`date '+%Y%m%d %H:%M:%S'`--$code--->$url" >>  /var/log/monitor.tomcat.visit.log  

#返回值和200作相等判断
if [  $code  -eq  200 ];then
	
	#相等就返回运行正常的时间
        echo "Tomcat运行正常,时间为:`date '+%Y%m%d %H:%M:%S'`" 

else	
	#做第二次判断，以免第一次失误
        echo "再次判断"

                if [  $code  -eq  200 ];then

                        echo "网页真的运行正常!!!"
                else
			
			#第二次判断，记录启动时间
                        echo "这次真的要重新启动!!!时间为:`date '+%Y%m%d %H:%M:%S'`"

			#先搜索tomcat进程再杀掉
                        ps -ef|grep tomcat |awk  'NR==1{ print $2}' | xargs kill -9
                        
			#进到tomcat启动脚本的目录下
			cd /data/apache-tomcat-8.5.11/bin/
                        
			#进行启动程序操作放入后台
			bash startup.sh &
                fi
fi 


