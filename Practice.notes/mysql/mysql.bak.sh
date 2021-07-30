#!/bin/bash
echo "现在时间为:`date '+%Y%m%d %H:%M:%S'`"
#DATE=`date +%Y%m%d%H:%M:%S`
DATE=`date +%Y%m%d`
printf  "数据库的操作:请输入参数(start|stop|restart|kill|status|bak.cnf):"
read num
case $num in
        start)
                systemctl start mysqld
                ;;
        stop)
                systemctl stop mysqld
                ;;

        restart)
                systemctl restart mysqld
                ;;
        kill)
                ps -ef|grep mysql |grep -v grep|grep -v PPID|awk '{ print $2}' | xargs kill -9
                ;;
        status)
                systemctl status mysqld
                ;;
        bak.cnf)
                cd /etc/  
                cp my.cnf  my.cnf.$DATE
                ;;
        *)
                echo "输入错误"
esac
