#/usr/bin/python
# -*- coding=utf-8 -*-
import smtplib
from email.mime.text import MIMEText
import time,datetime
import getopt,sys,os
from email.mime.application import MIMEApplication 
from email.mime.multipart import MIMEMultipart


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


def main(argv):
    mail_accout = 'test'
    mail_to = 'test@test.com'
    mail_host = "smtp.test.com"
    mail_password = 'test'
    mail_sub = "It's a test E-mail."
    mail_content = "test"
    attachFile = None
    try:
        opts,args = getopt.getopt(argv, "f:t:h:p:c:s:F:H:", ["mail_from=","mail_to=","mail_host=","mail_password=","mail_content=","mail_sub=","files=","help="])
    except getopt.GetoptError:
        useage()
        sys.exit(1)
    for opt, arg in opts:
        if opt in ("-f", "--from"):
            mail_accout = arg
        elif opt in ("-t","--to"):
            mail_to = arg
        elif opt in ("-h","--smtp"):
            mail_host = arg
        elif opt in ("-p","--password"):
            mail_password = arg
        elif opt in ("-c","--content"):
            mail_content = arg
        elif opt in ("-s","--sub"):
            mail_sub = arg
        elif opt in ("-F","--file"):
            attachFile = arg
        elif opt in ("-H","--help"):
            useage()
        else:
            sys.exit(0)    
    if len(sys.argv) >= 9:
        try:
            sendEmail(mail_accout,mail_to,mail_host,mail_password,mail_sub,mail_content,attachFile)
        except Exception , e:
            print e
    else:
        useage()
        sys.exit(1)

def useage():
    print "用法：sendEmail [选项]..."
    print ""
    print "长选项必须使用的参数对于短选项时也是必需使用的。"
    print "  -f, --from        发送邮箱地址"
    print "  -p, --password     发送邮箱密码"
    print "  -t, --to           接收邮箱地址"
    print "  -h, --smtp         发送邮箱的SMTP地址"
    print "  -c, --content      邮件正文内容"
    print "  -s, --sub          邮件主题"
    print "  -F, --file         邮件附件"
    print " "
    print "注意：-f -p -t -h 参数是必须给予的"
    print "请向303350019@qq.com 报告sendEmail 的错误"
    print " "

if __name__ == '__main__': 
    main(sys.argv[1:])