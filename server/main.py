import json
import os
import shutil
from typing import List
from fastapi import FastAPI, File, HTTPException, Form, UploadFile
import pyautogui
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys 
from selenium.common.exceptions import NoSuchElementException
from pydantic import BaseModel
from passlib.context import CryptContext
from fastapi.middleware.cors import CORSMiddleware # Import Keys modules
import time


from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from instagrapi import Client

from PIL import Image
from moviepy.editor import VideoFileClip

app = FastAPI()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

clint_initialized=False

class UserCreate(BaseModel):
    username: str
    password: str

origins = [
    "http://localhost",
    "http://localhost:5173",
      # Example frontend URL
    # Add more origins as needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization", "Content-Type"],
)

UPLOAD_DIR="tempUploads"

#####################################################################


from models import User
from mongoengine import connect

ACCESS_TOKEN_EXP_TIME=30 #in minutes


connect(db="trial",host="mongodb+srv://test-01:123reset456@cluster0.w3hoof9.mongodb.net/")

class NewUser(BaseModel):
    username: str
    password: str

def get_password_hash(password):
    return pwd_context.hash(password)


@app.post("/sign_up")
def sign_up(newUser:NewUser):
    username = newUser.username
    password = newUser.password
    try:
        user = json.loads(User.objects.get(username=username).to_json())

        return {
            "status":"failed",
            "message":"user already exists!!"
        }
    
    except User.DoesNotExist:
        user = User(username=username,
                    password=get_password_hash(password))
        user.save()

    return {
        "status":"success",
        "message":"New user data saved."
        }


from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def authenticate_user(username, password):

    try:
        user = json.loads(User.objects.get(username=username).to_json())

        password_check = pwd_context.verify(password, user['password'])
        return password_check
    
    except User.DoesNotExist:
        return False

from datetime import timedelta,datetime
from jose import jwt

SECRET_KEY="a9aff04ddd4eecd177c405923a213bf4"
ALGORITHM = "HS256"

def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()

    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp":expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt



@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends() ):
    username = form_data.username
    password = form_data.password

    if authenticate_user(username, password):
        access_token = create_access_token(
            data={"sub":username},
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXP_TIME)
        )


        return {"access_token": access_token, "username":username}
    else:
        raise HTTPException(status_code=400,detail="Incorrect username or password.")

    print(username, password)

@app.get("/verify_token")
def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(payload)
        return {
            "access":"allow",
            "token":payload    
        }
    except Exception as e:
        print("except = ",e)
        return {
            "access":"deny"
        }


# @app.get('/login')
# def login(username:str, password:str):

#     check = authenticate_user(username,password)
#     if(check==False):
#         return {
#             "status":"Failed",
#             "message":"Credentials are wrong!!"
#         }

#     global driver
#     chrome_options = Options()
#     driver_service = Service(ChromeDriverManager().install())
#     driver = webdriver.Chrome(service=driver_service, options=chrome_options)
#     driver.get('https://www.instagram.com/')
#     time.sleep(10)  # import time

#     ## try id-> test.1231650  and pass -> 123reset456  for testing purpose

#     username_input = driver.find_element(By.NAME, 'username')
#     username_input.send_keys(username)
#     password_input = driver.find_element(By.NAME, 'password')
#     password_input.send_keys(password)
                     
#     password_input.submit()

#     return {
#         "status":"success",
#         "message":"instagram opened for further usage"
#     }

################################################################################################################################################################

# Function to check Instagram login using Selenium

def check_instagram_login(username: str, password: str):
    try:
        chrome_options = Options()
        # Uncomment for headless mode
        # chrome_options.add_argument("--headless")
        global driver
 
        driver_service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(options=chrome_options)#service=driver_service,

        driver.get('https://www.instagram.com/')
        time.sleep(3)

        username_input = driver.find_element(By.NAME, 'username')
        username_input.send_keys(username)
        password_input = driver.find_element(By.NAME, 'password')
        password_input.send_keys(password)
        
        current_url = driver.current_url
        
        password_input.submit()
        time.sleep(10)
        

        # Check if login was successful
        after_url = driver.current_url

        if current_url==after_url:                         ## making changes here
            print(f"Login failed. Current URL: {current_url}")
            return False, None  # Return False and None for driver
        else:
            print(f"Login successful. Current URL: {current_url}")
            return True, driver # Return True and driver instance

    except Exception as e:
        print(f"Login error: {e}")
        return False, None
    finally:
        # Do not quit driver here, handle it externally
        pass



# Function to comment on a post
def comment_on_post(driver, post_url: str, comment_text: str):
    try:
        if driver is None:
            print("Cannot comment. Driver not initialized.")
            return False
        
        # Navigate to the post URL
        driver.get(post_url)
        time.sleep(3)

        # Find the comment input field
        comment_btn = driver.find_element(By.XPATH, """/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[1]/section/main/div/div[1]/div/div[2]/div/div[3]/section[1]/div[1]/span[2]/div""")
        comment_btn.click()
        comment_btn.click()

        time.sleep(3)

        comment_input = driver.find_element(By.XPATH,"""/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[1]/section/main/div/div[1]/div/div[2]/div/div[4]/section/div/form/div/textarea""")
        comment_input.send_keys(comment_text)

        time.sleep(3)

        comment_post = driver.find_element(By.XPATH,"""/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[1]/section/main/div/div[1]/div/div[2]/div/div[4]/section/div/form/div/div[2]/div""")
        comment_post.click()        
        # comment_input.send_keys(comment_text)
        # comment_input.send_keys(Keys.ENTER)
        time.sleep(3)

        print(f"Comment '{comment_text}' added successfully.")
        return True

    except Exception as e:
        print(f"Error commenting on post: {e}")
        return False
    finally:
        # Do not quit driver here, handle it externally
        pass


# Function to like a post
def like_post(driver, post_url: str):
    try:
        if driver is None:
            print("Cannot like. Driver not initialized.")
            return False
        
        # Navigate to the post URL
        driver.get(post_url)
        time.sleep(3)

        # Find the like button and click it
        
        
        like_button = driver.find_element(By.XPATH, """/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[1]/section/main/div/div[1]/div/div[2]/div/div[3]/section[1]/div[1]/span[1]/div/div""")
        like_button.click()
        like_button.click()
        
        time.sleep(3)

        return True

    except Exception as e:
        print(f"Error liking post: {e}")
        return False
    finally:
        # Do not quit driver here, handle it externally
        pass

# Function to follow a user
def follow_user(driver, username_to_follow: str):
    try:
        if driver is None:
            print("Cannot follow. Driver not initialized.")
            return False
        
        # Navigate to the user's profile
        profile_url = f"https://www.instagram.com/{username_to_follow}/"
        driver.get(profile_url)
        time.sleep(3)

        # Find the follow button and click it
        add_to_chart = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Follow')]")))
        add_to_chart.click()
        time.sleep(3)
        print(f"Followed user '{username_to_follow}' successfully.")
        return True

    except Exception as e:
        print(f"Error following user '{username_to_follow}': {e}")
        return False
    finally:
        # Do not quit driver here, handle it externally
        pass

# Endpoint to check Instagram login
@app.post("/check_login")
async def check_login(newUser: NewUser):
    username = newUser.username
    password = newUser.password
    global driver
    login_status, driver = check_instagram_login(username, password)
    if login_status:
        # If login successful, return success message
        return {
            "message": "Login successful",
            "login status":login_status
        }
    else:
        # If login failed, raise HTTPException
        raise HTTPException(status_code=401, detail="Login failed")



class CommentOnPost(BaseModel):
    post_url:str
    comment_text:str

# Endpoint to comment on a post
@app.post("/comment_on_post")
async def comment_instagram_post(data:CommentOnPost):
    post_url=data.post_url
    comment_text=data.comment_text
    global driver
    if driver:
        # If login successful, attempt to comment
        comment_status = comment_on_post(driver, post_url, comment_text)
        if comment_status:
            return {"message": f"Comment '{comment_text}' added successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to comment on post")
    else:
        # If login failed, raise HTTPException
        raise HTTPException(status_code=401, detail="Login failed")

class LikePost(BaseModel):
    post_url:str

# Endpoint to like a post
@app.post("/like_post")
async def like_instagram_post(data:LikePost):

    global driver
    post_url = data.post_url

    if driver:
        # If login successful, attempt to like the post
        like_status = like_post(driver, post_url)
        if like_status:
            return {"message": "Post liked successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to like the post")
    else:
        # If login failed, raise HTTPException
        raise HTTPException(status_code=401, detail="Login failed")


class UserTOFollow(BaseModel):
    usernameToFollow:str

# Endpoint to follow a user
@app.post("/follow_user")
async def follow_instagram_user(data:UserTOFollow):
    username_to_follow = data.usernameToFollow
    if driver:
        # If login successful, attempt to follow the user
        follow_status = follow_user(driver, username_to_follow)
        if follow_status:
            return {"message": f"Followed user '{username_to_follow}' successfully"}
        else:
            raise HTTPException(status_code=500, detail=f"Failed to follow user '{username_to_follow}'")
    else:
        # If login failed, raise HTTPException
        raise HTTPException(status_code=401, detail="Not ")


@app.post("/upload_story")
async def story_to_instagram(caption:str, file: UploadFile=File(...)):
    # 
    try:
        # Read the file content
        # file_content = await file.read()
        global client,UPLOAD_DIR

        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        path=r"C:\Users\adity\Downloads\WhatsApp_Image_2024-02-11_at_12.12.59_1c5fa8a1 (1).jpg"

        story=client.photo_upload_to_story(file_path,"caption")

        os.remove(file_path)

        print("Story uploaded successfully:", dict(story))

        return {"message":"success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
@app.post("/upload_post")
async def post_to_instagram(caption: str, file: UploadFile = File(...)):
    driver.get('https://www.instagram.com/')
    time.sleep(2)
    try:
        driver.find_element(By.XPATH , "//button[text()='Not Now']").click()
    except:
        pass
        time.sleep(1)
    asd = """//*[@aria-label='New post']"""
    abc = """//button[text()='Select from computer']"""
    nsd = """//div[text()='Next']"""
    
    try:
        # Save the uploaded file
        file_content = await file.read()
        global UPLOAD_DIR
        print("Size of file = ", file.size)
        absolute_upload_dir = os.path.abspath(UPLOAD_DIR)
        file_path = os.path.join(absolute_upload_dir, file.filename)

        
        # Ensure the upload directory exists
        os.makedirs(absolute_upload_dir, exist_ok=True)
        
        file.file.seek(0)
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        
        print(f"File saved at {file_path}")
        
        time.sleep(10)
        
        # Check if the file size exceeds Instagram's limit
        if os.path.getsize(file_path) > 20 * 1024 * 1024:  # Example size limit
            print("The image is too large.")
            return {"message": "The image is too large."}
        
        try:
            # Interact with the Instagram UI using Selenium
            New_Post = driver.find_element(By.XPATH, asd).click()
            time.sleep(2)

            time.sleep(2)
            file_input = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
            file_input.send_keys(file_path)
            time.sleep(9)
            ok_button="""/html/body/div[6]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/div/div[4]/button"""
            try:
                driver.find_element(By.XPATH, ok_button).click()
            except:
                pass
            nsd = """//div[text()='Next']"""
            driver.find_element(By.XPATH, nsd).click()
            time.sleep(1)
            driver.find_element(By.XPATH, nsd).click()
            time.sleep(2)
            
            caption_xpath = """//*[@aria-label='Write a caption...']"""
            driver.find_element(By.XPATH, caption_xpath).send_keys(caption)
            time.sleep(2)
            share_xpath = """//div[text()='Share']"""
            driver.find_element(By.XPATH, share_xpath).click()
            time.sleep(30)
            
            print("Image uploaded successfully")
        
        except Exception as e:
            print("An error occurred while uploading the image/video:", str(e))
            return {"message": "Failed to upload"}
        
        finally:
            # Clean up the uploaded file
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"File {file_path} removed")
        
        return {"message": "Success"}
    
    except Exception as e:
        print("Exception occurred:", str(e))
        raise HTTPException(status_code=500, detail=str(e))

class tempMsgToMultipleUsers(BaseModel):
    lst: List[str]
    msg: str

@app.post("/message_to_multiple_users")
async def post_to_instagram(data: tempMsgToMultipleUsers):
    
    try:
        # Read the file content
        # file_content = await file.read()
        global client

        lst = list(data.lst)
        msg = data.msg
        print(lst,"\n",msg)

        failed=[]

        for x in lst:
            time.sleep(2)
            driver.get(f'https://www.instagram.com/{x}/')
            time.sleep(4)

            try:
                driver.find_element(By.XPATH , "//div[text()='Message']").click()
                time.sleep(5)

                try:
                    driver.find_element(By.XPATH , "//button[text()='Not Now']").click()
                except:
                    pass
                time.sleep(1)

                message_box = driver.find_element(By.XPATH, "//*[@aria-label='Message']")
                time.sleep(2)
            except NoSuchElementException:
                failed.append(x)
                continue

            message_box.send_keys(msg)
            time.sleep(1)
            message_box.send_keys(Keys.RETURN)

        return {"message":"success","failed_users":failed,"reason":"username might be invalid or private account"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))