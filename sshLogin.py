#!/usr/bin/env python  
# _#_ coding:utf-8 _*_  
import sys,re,os
import threading,time
import smtplib
from email.mime.application import MIMEApplication 
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from daemon import Daemon

reload(sys)
sys.setdefaultencoding('utf8')

mail_accout = 'xxx@qq.com'
mail_to = 'xxx@qq.com'
mail_host = "smtp.qq.com"
mail_password = 'xxx@qq.com'
mail_sub = "It's a test E-mail."
mail_content = "test"
attachFile = None
login_info = {}
securefile = '/var/log/secure'
login_str = re.compile('Accepted')


def sendEmail(e_from,e_to,e_host,e_passwd,e_sub="It's a test email.",e_content="test",attachFile=None):
    msg = MIMEMultipart() 
    EmailContent = MIMEText(e_content,_subtype='html',_charset='utf-8')
    msg.attach(EmailContent)
    msg['Subject'] = "%s " % e_sub
    msg['From'] = e_from
    if e_to.find(',') == -1:
        msg['To'] = e_to
    else: 
        e_to = e_to.split(',')
        msg['To'] = ';'.join(e_to)    
    msg['date'] = time.strftime('%Y %H:%M:%S %z')
    try:
        if attachFile:
            EmailContent = MIMEApplication(open(attachFile,'rb').read()) 
            EmailContent["Content-Type"] = 'application/octet-stream'
            fileName = os.path.basename(attachFile)
            EmailContent["Content-Disposition"] = 'attachment; filename="%s"' % fileName
        msg.attach(EmailContent)
        smtp=smtplib.SMTP()
        smtp.connect(e_host)
        smtp.login(e_from,e_passwd)
        smtp.sendmail(e_from,e_to,msg.as_string())
        smtp.quit()
    except Exception , e:
        print e


class startThread(threading.Thread):
    def __init__(self, num,interval,type):
        threading.Thread.__init__(self)
        self.thread_num = num
        self.interval = interval
        self.type = type
        self.count = 0
        self.thread_stop = False 
 
    def run(self):
        while not self.thread_stop:
            if self.type == 'get':
                self.runCheckUserLogin()
            time.sleep(self.interval)

    def runCheckUserLogin(self):
        rs = runCheck()
        if rs[1] == 'error' and self.count != 0:
            user = rs[0].get('user')
            ip = rs[0].get('ip')
            time = rs[0].get('time')
            sip = getServerIp()
            sub = "服务器：%s 用户登入" % sip
            content = "账户：%s 于  %s 从  %s 登入服务器（%s）" % (user,time,ip,sip)
            sendEmail(mail_accout,mail_to,mail_host,mail_password,sub,content)
        else:
            self.count = 1
            pass
        
def getLoginInfo():
    sList = []
    try:
        with open(securefile, "r") as f:
            for ip in f: 
                login_info = {}
                msg = ip.replace('\n','')
                if login_str.findall(msg):
                    msg = msg.split()
                    login_ip = msg[-4]
                    login_time = msg[2]
                    login_user = msg[8]
                    login_info['time'] = login_time
                    login_info['ip'] = login_ip
                    login_info['user'] = login_user
                    sList.append(login_info)
            f.close()
            return sList
    except:
        print 'secure file do not exist.'
    
def checkUserLogin(sList):
    newIp = sList[-1].get('ip')
    oldIp = login_info.get('ip')
    if  newIp != oldIp:
        login_info['time'] = sList[-1].get('time')
        login_info['ip'] = sList[-1].get('ip')
        login_info['user'] = sList[-1].get('user')
        return [login_info,'error']
    else:
        return [login_info,'ok']
    
def runCheck():
    s = getLoginInfo()
    return checkUserLogin(s)
    
def getServerIp():
    cmd = '''ifconfig |awk  'BEGIN{FS="[ :]+"}NR==2{print$4}' '''
    return os.popen(cmd).read().replace('\n','')  

class runDaemon(Daemon):
    def run(self):
            runCheck = startThread(1,30,'get')
            runCheck.start()

if __name__ == '__main__':
    daemon = runDaemon('/tmp/sshLoginMonitor.pid')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)
