from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
import csv


class Comment:
    def __init__(self, username, content):
        self.username = username
        self.content = content

class Post:
    def __init__(self, link, date, content,nbr_likes=0,nbr_reposts=0,comments=None):
        self.link = link
        self.date = date
        self.content = content
        self.nbr_likes = nbr_likes
        self.nbr_reposts = nbr_reposts
        self.comments = comments if comments is not None else []

    def add_comment(self, url, comment):
        # Logic to create a comment on a post
        self.comments.append(comment)
    def show_all_comments(self):
        for comment in self.comments:
            print(f"{comment.username}: {comment.content}")



class User:

    def __init__(self, username, password, url="", connection_nbr=0,posts=None):
        self.username = username
        self.password = password
        self.url = url
        self.connection_nbr = connection_nbr
        self.posts = posts if posts is not None else []

    def set_url(self,url):
        self.url = url

    def set_connection_nbr(self,connection_nbr):
        self.connection_nbr = connection_nbr

    def add_post(self,post):
        self.post = post

    def create_post(self, content):
        driver.get('https://linkedin.com/feed/')
        sleep(1)
        driver.find_element_by_class_name('share-box-feed-entry__trigger').click()
        sleep(0.5)
        driver.find_element_by_css_selector('div.ql-editor.ql-blank').send_keys(content)
        sleep(2)
        driver.find_element_by_class_name('artdeco-button--primary').click()

        # post = Post(self.url, self.content)
        # Additional logic to store the post or perform any necessary actions
        return 0

    def create_comment(self, post_url, content):
        driver.get(post_url)
        sleep(1)
        driver.find_element_by_class_name('ql-blank').send_keys(content)
        sleep(1)
        driver.find_element_by_class_name('comments-comment-box__submit-button').click()

        return 0

    def show_all_posts(self):
        for post in self.posts:
            print(f"Date: {post.date}, \nPost: {post.content}\nLikes: {post.nbr_likes}, Reposts: {post.nbr_reposts}\n")
            post.show_all_comments()
# name_file=input("Name of your file :")
# load selenium driver
driver = webdriver.Chrome("C:\linkedIn_project\chromedriver.exe")
driver.get('https://linkedin.com/login/')
sleep(1)

# get username and password input boxes path
username = driver.find_element_by_id("username")
password = driver.find_element_by_id("password")
# input the email id and password input("Enter your username: ")  input("Enter your password: ")

username_txt =input("Please enter your email address: ")
password_txt = input("Please enter your password ")
username.send_keys(username_txt)
password.send_keys(password_txt)
user = User(username_txt,password_txt)

### click the login button
login_btn = driver.find_element_by_class_name("btn__primary--large")
sleep(1)
login_btn.click()
# email_exist = driver.find_element_by_css_selector('#username')
# password_correct = driver.find_element_by_css_selector('#organic-otp-link-in-error-message')
sleep(20)

# if email_exist:
#     print("Email doesnt exist")
#     login = False
# else:
#     if password_correct:
#         print('Password incorrect')
#     else:
#         print('Login successful')
#         sleep(2)
#         login = True
if True:
    my_profil = driver.find_element_by_css_selector('a.ember-view.block')
    profil_URL = my_profil.get_attribute('href')
    driver.get("https://www.linkedin.com/search/results/people/?network=%5B%22F%22%5D&origin=MEMBER_PROFILE_CANNED_SEARCH&sid=-d!")

    sleep(5)
    # connections = driver.find_element_by_id('link-without-visited-state')
    # connections.click()
    # sleep(2)
    connections_nbr=driver.find_element_by_class_name('pb2').text.replace(' results','')
    print(profil_URL)
    user.set_url(profil_URL)
    print(connections_nbr)

    driver.get(profil_URL+'recent-activity/all/')
    profile_to_scrap='https://www.linkedin.com/in/zineb-abdi/recent-activity/all/'
    driver.get(profile_to_scrap)
    sleep(7)
    user.set_connection_nbr(connections_nbr)

    # Get the page height
    page_height = driver.execute_script("return document.body.scrollHeight")

    # Set the scroll step size and delay between steps
    scroll_step = 500  # Adjust the scroll step size as needed
    scroll_delay = 0.3  # Adjust the delay between steps as needed

    # Perform the slow scroll
    current_scroll = 0
    while current_scroll < page_height:
        # Scroll down by the scroll step size
        driver.execute_script(f"window.scrollBy(0, {scroll_step});")
        sleep(scroll_delay)
        page_height = driver.execute_script("return document.body.scrollHeight")

        current_scroll += scroll_step

    html = driver.page_source
    #print(html)
    div_posts = driver.find_elements(By.CSS_SELECTOR, 'ul.social-details-social-counts')
    testing = driver.find_elements_by_class_name('update-components-actor__sub-description')
    print("Postes Number : "+str(len(testing)))
    # ember73 > div > div.feed-shared-update-v2__description-wrapper.mr2 > div.feed-shared-inline-show-more-text.feed-shared-update-v2__description.feed-shared-inline-show-more-text--minimal-padding.feed-shared-inline-show-more-text--5-lines > div > span > span > spannline-show-more-text--minimal-padding.feed-shared-inline-show-more-text--5-lines > div > span > span > span

    #print(testing)
    dates_liste=[]
    for post in testing:
        try:
            date = post.find_element(By.XPATH, './/span[@class = "visually-hidden"]').text
            print("Date : "+date)
            dates_liste.append(date)
        except:
            print("An exception occurred")



    likes_nember=[]
    comments_nember=[]
    reposts_nember=[]
    contents_list=[]
    for reaction in div_posts:
        try:
            likes = reaction.find_element(By.XPATH,
                                          './/span[@class = "social-details-social-counts__social-proof-fallback-number"]').text
        except:
            try:
                likes = reaction.find_element(By.XPATH,
                                              './/span[@class = "social-details-social-counts__reactions-count"]').text
            except:
                likes=0
        print('Likes Number : '+likes)
        likes_nember.append(likes)

        try:
            comments = reaction.find_element(By.CSS_SELECTOR,'ul > li.social-details-social-counts__item.social-details-social-counts__comments.social-details-social-counts__item--with-social-proof > button > span').text
            sleep(3)
            reaction.find_element(By.CSS_SELECTOR,
                                   'ul > li.social-details-social-counts__item.social-details-social-counts__comments.social-details-social-counts__item--with-social-proof > button').click()

        except:
            comments = 0
        print('Comments Number : '+str(comments))
        comments_nember.append(comments)

        try:
            repost = reaction.find_element(By.XPATH, ".//li[3]/button/span").text
        except:
            repost = 0
        print('Repost Number : '+str(repost))
        reposts_nember.append(repost)


        #try:

            # try:
            #     all_comments = reaction.find_elements(By.TAG_NAME,'arcticle')
            #
            #     for comment_content in all_comments:
            #         try:
            #             print(comment_content.find_element(By.CSS_SELECTOR,'div.comments-comment-item-content-body.break-words > div > div > span').text)
            #         except:
            #             print("shit")
            #
            #
            #         #print(comment_content.find_element_by_css_selector('div.comments-comment-item-content-body.break-words > div > div.feed-shared-inline-show-more-text.comments-comment-item__inline-show-more-text > span > div > span').text)
            # except:
            #     print("shit2")
        #except:
            #print("shit2")

    #Showing_postes
    post_contents = driver.find_elements(By.CSS_SELECTOR,'li.profile-creator-shared-feed-update__container')
    for content in post_contents:
        try:
            articles_nbr = len(content.find_elements(By.CSS_SELECTOR, 'article.comments-comment-item'))
            new_value = 0
            while (new_value != articles_nbr):
                new_value = articles_nbr
                xpath_div=content.find_element(By.XPATH,'.//div/div/div[2]/div')
                div=xpath_div.find_element(By.CSS_SELECTOR,'div.social-details-social-activity.update-v2-social-activity')
                #content.find_element(By.CSS_SELECTOR,'button.comments-comments-list__load-more-comments-button').click()

                sleep(1)
                #articles_nbr = len(content.find_elements(By.CSS_SELECTOR,'article.comments-comment-item'))
            print(new_value)
        except:
            print("error")
        try:
            content_text = content.find_element(By.XPATH,'.//div/div/div[2]/div/div/div[4]/div[1]/div/span/span/span').text
        except:
            try:
                try:
                    content_text = content.find_element(By.XPATH,'.//div/div/div[2]/div/div[5]/div[1]/div/span/span/span').text
                except:
                    content_text = content.find_element(By.XPATH,'.//div/div/div[2]/div/article/div/div[2]/div/a').get_attribute('href')
            except:
                try:
                    try:
                        content_text = content.find_element(By.XPATH,'.//div/div/div[2]/div/div[4]/div[1]/div/span/span/span').text
                    except:
                        content_text = content.find_element(By.XPATH,'.//div/div/div[2]/div/div/div[5]/div[1]/div/span/span').text
                except:
                    content_text = "ERROR"
        content_text = content_text[:content_text.find("…see more")]
        print(content_text)
        contents_list.append(content_text)
        print("########################################################################################")


# # abdullah
# #     # # Combine the lists into a single list of rows
#      rows = zip(dates_liste, likes_nember, comments_nember , reposts_nember , contents_list)
# #
# #    # Open the CSV file in append mode
#      with open(f"D:\linkden project\{name_file}.csv", 'a', newline='' , encoding='ISO-8859-1') as file:
# #     #
#           writer = csv.writer(file)
#     #
#           # Write header
#           writer.writerow(['Date', 'Likes', 'Comments','reports ', 'contents'])
#           # Write each row to the CSV file
#           writer.writerows(rows)
#           print("file created")
#
#
#
# # this is working-
# #user.create_post("Aid Mubarak Said \n*Ibrahim ESSAKINE ")
# # this is working
# #user.create_comment('https://www.linkedin.com/posts/aymane-boumezzough-1b86a2239_cv-activity-7027715759954907136-ySkV?utm_source=share&utm_medium=member_desktop','Bon Courage Si Aymane')
#
#




