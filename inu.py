import sys
sys.path.append("C:/Users/nayeon/AppData/Local/Programs/Python/Python37-32/Lib")

from datetime import datetime
from selenium import webdriver
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText

uname = ''
pword = ''
email = ''
email_key = ''


def login():
    driver.implicitly_wait(3)

    driver.get('https://cyber.inu.ac.kr/login.php')
    driver.find_element_by_id('input-username').send_keys(uname)
    driver.find_element_by_id('input-password').send_keys(pword)
    driver.find_element_by_xpath('//*[@id="region-main"]/div/div/div/div[1]/div[1]/div[2]/form/div[2]/input').click()


def parser(name, link):
    driver.get(link)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    current_course = soup.find('div', {'class': 'course_box course_box_current'})
    todo = current_course.find_all('span')

    message = '*****' + name + '*****' + '\n'
    for t in todo:
        if str(t['class']) == '[\'instancename\']' or str(t['class']) == '[\'text-ubstrap\']':
            if t.text.find('콘텐츠 CMS'):
                message += t.text.replace('콘텐츠 CMS', '').strip() + '\n'
            else:
                message += t.text.strip() + '\n'

    message += '-------------\n\n\n'
    return message


def sendMail(message):
    # 세션 생성
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # TLS 보안 시작
    s.starttls()

    # 로그인 인증
    s.login(email, email_key)

    # 보낼 메시지 설정
    msg = MIMEText(message)
    msg['Subject'] = str(datetime.today().month) + '/' + str(datetime.today().day) + '의 수업과 과제'

    # 메일 보내기
    s.sendmail(email, email, msg.as_string())

    # 세션 종료
    s.quit()


if __name__ == '__main__':
    driver = webdriver.Chrome('/chromedriver')
    courses = [{'name': '프로그래밍 입문', 'link': 'http://cyber.inu.ac.kr/course/view.php?id=26226'}
        , {'name': 'Java 언어', 'link': 'http://cyber.inu.ac.kr/course/view.php?id=26228'}
        , {'name': '대학영어회화1', 'link': 'http://cyber.inu.ac.kr/course/view.php?id=26553'}
        , {'name': '소프트웨어 모델링', 'link': 'http://cyber.inu.ac.kr/course/view.php?id=26771'}
        , {'name': '디지털 공학', 'link': 'http://cyber.inu.ac.kr/course/view.php?id=28448'}
        , {'name': '데이터통신', 'link': 'http://cyber.inu.ac.kr/course/view.php?id=28917'}
        , {'name': '운영체제', 'link': 'http://cyber.inu.ac.kr/course/view.php?id=28453'}
               ]

    message = ''
    login()
    for course in courses:
        message += parser(course['name'], course['link'])
    sendMail(message)
