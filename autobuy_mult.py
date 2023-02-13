from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
import threading

class MyThread(threading.Thread):
    def __init__(self,num):
        threading.Thread.__init__(self)
        self.num = num

    def run(self):
        print("Thread",self.num+1,"執行中")
        autobuy()
        sleep(1)


def autobuy():
    driver = webdriver.Chrome()

    def start():
        url = 'https://myship.7-11.com.tw/Home/Main'
        driver.get(url)
        try:
            cancel = WebDriverWait(driver,1,0.5).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[2]/main/div[2]/div/div')))  
            cancel.click()
        finally:
            driver.get(url)
            login = WebDriverWait(driver,1,0.5).until(EC.presence_of_element_located((By.ID,'login_button')))
            login.click()          #點擊登入鍵
    
    def login(email,password):

        choose_fb = WebDriverWait(driver,1,0.5).until(EC.presence_of_element_located((By.XPATH,'//*[@id="returnUrl"]/button[1]')))  #選擇登入fb
        choose_fb.click()
        
        fb_account = WebDriverWait(driver,1,0.5).until(EC.presence_of_element_located((By.XPATH,'//*[@id="email"]')))  #輸入帳號密碼
        fb_account.send_keys(email)

        fb_password = WebDriverWait(driver,1,0.5).until(EC.presence_of_element_located((By.XPATH,'//*[@id="pass"]')))  #輸入帳號密碼
        fb_password.send_keys(password)
        
        login_btn = WebDriverWait(driver,1,0.5).until(EC.presence_of_element_located((By.ID,'loginbutton')))  #登入
        login_btn.click()



    def buy(url,size_xpath,quantity_xpath,quantity,buynow):

        driver.get(url)

        while(1):
            try:
                size = WebDriverWait(driver,1,0.5).until(EC.presence_of_element_located((By.XPATH,size_xpath)))     #選擇尺寸
                size.click()
                print('已開始')
                break            
            except:
                print('尚未開始拍賣')
                driver.refresh()      

        if(quantity > 1):
            for i in range(quantity-1):
                count = WebDriverWait(driver,20,0.5).until(EC.presence_of_element_located((By.XPATH,quantity_xpath)))    #數量+1
                count.click() 
                

        buynow = WebDriverWait(driver,20,0.5).until(EC.presence_of_element_located((By.XPATH,buynow)))
        buynow.click()             #結帳


        check = WebDriverWait(driver,20,0.5).until(EC.presence_of_element_located((By.CSS_SELECTOR,'div.checkbox>label')))      #勾選同意條款
        check.click()         

    def checkout(phone,email):
        btnNext = WebDriverWait(driver,20,0.5).until(EC.presence_of_element_located((By.XPATH,'//*[@id="btnNext"]')))
        btnNext.click()  
        
        enter_phone = WebDriverWait(driver,20,0.5).until(EC.presence_of_element_located((By.XPATH,'//*[@id="OrdMobile"]')))
        enter_phone.send_keys(phone)

        enter_email = WebDriverWait(driver,20,0.5).until(EC.presence_of_element_located((By.XPATH,'//*[@id="OrdEmail"]')))
        enter_email.send_keys(email)

        #driver.find_element(By.XPATH,'//*[@id="btnNext"]').click()              #送出訂單

    start()
    sleep(5)

    login('','')        #填入fb帳號,密碼
    sleep(5)

    buy('https://myship.7-11.com.tw/general/detail/GM2211081464286','//*[@id="divGoodList"]/div[3]/div/div[2]/div[3]/div[1]/div/span[3]','//*[@id="divGoodList"]/div[3]/div/div[2]/div[3]/div[2]/div[1]/div/input[3]',3,'//*[@id="divGoodList"]/div[3]/div/div[2]/div[3]/div[2]/div[2]/button[2]')      
    #輸入搶購頁面,尺寸xpath,數量加號xpath、數量、購買按鈕xpath
        
    checkout('','')  #填入電話、email

    sleep(100)
        

if __name__ == "__main__":

    threads = []
    thread_num = 2

    for i in range(thread_num):
        threads.append(MyThread(i))
        threads[i].start()
