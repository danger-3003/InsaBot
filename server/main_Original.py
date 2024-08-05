import json
from fastapi import FastAPI, HTTPException, Form
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys 
from pydantic import BaseModel
from passlib.context import CryptContext
from fastapi.middleware.cors import CORSMiddleware # Import Keys modules
import time

app = FastAPI()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

users = {}

class UserCreate(BaseModel):
    username: str
    password: str

origins = [
    "http://localhost",
    "http://localhost:5173",  # Example frontend URL
    # Add more origins as needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization", "Content-Type"],
)

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
def sign_up(new_user: NewUser):
    user = User(username=new_user.username,
                password=get_password_hash(new_user.password))
    user.save()

    return {"message":"New User created successfully."}


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

@app.get("/get_token")
def get_token(token: str = Depends(oauth2_scheme)):
    return {"token":token}


@app.get("/try-intialize")
def initialize():
    global driver
    chrome_options = Options()
    driver_service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=driver_service, options=chrome_options)
    driver.get('https://www.instagram.com/')

@app.get("/try-login")
def try_login():
    username_input = driver.find_element(By.NAME, 'username')
    username_input.send_keys('test.1231650')
    password_input = driver.find_element(By.NAME, 'password')
    password_input.send_keys('123reset456')
                     
    password_input.submit()

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@app.get("/try-follow")
def try_follow(user_id:str):
    driver.get(f'https://www.instagram.com/{user_id}')
    add_to_chart = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Follow')]")))
    add_to_chart.click()


##########################################                  Above Code by Aditya Please check it

# Function to check Instagram login using Selenium

def check_instagram_login(username: str, password: str):
    try:
        chrome_options = Options()
        # Uncomment for headless mode
        # chrome_options.add_argument("--headless")
        
        driver_service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=driver_service, options=chrome_options)

        driver.get('https://www.instagram.com/')
        time.sleep(5)

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
            return True, driver  # Return True and driver instance

    except Exception as e:
        print(f"Login error: {e}")
        return False, None
    finally:
        # Do not quit driver here, handle it externally
        pass

# Function to message multiple Instagram IDs
def message_multiple_ids(driver, ids: list, message_text: str):
    try:
        if driver is None:
            print("Cannot message. Driver not initialized.")
            return False
        
        for instagram_id in ids:
            profile_url = f"https://www.instagram.com/{instagram_id}/"
            driver.get(profile_url)
            time.sleep(5)
            
            message_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Message')]")
            message_button.click()
            time.sleep(3)
            
            message_input = driver.find_element(By.XPATH, "//textarea[@aria-label='Message']")
            message_input.send_keys(message_text)
            message_input.send_keys(Keys.ENTER)
            time.sleep(3)
            
            print(f"Message sent to {instagram_id}")
        
        return True
    
    except Exception as e:
        print(f"Error sending message: {e}")
        return False


# Function to post on Instagram
def post_to_instagram(driver, image_path: str, caption: str = "", first_comment: str = ""):
    try:
        if driver is None:
            print("Cannot post. Driver not initialized.")
            return False
        
        # Navigate to create post page
        driver.get('https://www.instagram.com/accounts/upload/')
        time.sleep(5)

        # Upload image or video
        upload_input = driver.find_element(By.XPATH, "//input[@type='file']")
        upload_input.send_keys(image_path)
        time.sleep(5)

        # Add caption
        caption_input = driver.find_element(By.XPATH, "//textarea[contains(@aria-label, 'Write a caption')]")
        caption_input.send_keys(caption)

        # Add first comment (if provided)
        if first_comment:
            caption_input.send_keys(Keys.ENTER)  # Move to new line
            caption_input.send_keys(first_comment)

        # Post the content
        post_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Share')]")
        post_button.click()
        time.sleep(10)

        print("Post successful.")
        return True

    except Exception as e:
        print(f"Error posting on Instagram: {e}")
        return False
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
        time.sleep(5)

        # Find the comment input field
        comment_input = driver.find_element(By.XPATH, "//textarea[@aria-label='Add a comment…']")
        comment_input.send_keys(comment_text)
        comment_input.send_keys(Keys.ENTER)
        time.sleep(5)

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
        time.sleep(5)

        # Find the like button and click it
        like_button = driver.find_element(By.XPATH, "//span[@aria-label='Like']")
        like_button.click()
        time.sleep(3)

        print(f"Post liked successfully.")
        return True

    except Exception as e:
        print(f"Error liking post: {e}")
        return False
    finally:
        # Do not quit driver here, handle it externally
        pass

# Function to keep a story
def keep_story(driver):
    try:
        if driver is None:
            print("Cannot keep story. Driver not initialized.")
            return False
        
        # Navigate to own profile
        driver.get('https://www.instagram.com/accounts/access_tool/')

        # Click on the Saved tab
        saved_tab = driver.find_element(By.XPATH, "//a[contains(@href, '/saved/')]")
        saved_tab.click()
        time.sleep(5)

        # Click on Add to Saved
        add_to_saved_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Add to Saved')]")
        add_to_saved_button.click()
        time.sleep(3)

        print(f"Story kept successfully.")
        return True

    except Exception as e:
        print(f"Error keeping story: {e}")
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
        time.sleep(5)

        # Find the follow button and click it
        follow_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Follow')]")
        follow_button.click()
        time.sleep(3)
        print(f"Followed user '{username_to_follow}' successfully.")
        return True

    except Exception as e:
        print(f"Error following user '{username_to_follow}': {e}")
        return False
    finally:
        # Do not quit driver here, handle it externally
        pass

@app.post("/register/")
def register_user(user: UserCreate):
    hashed_password = pwd_context.hash(user.password)
    if user.username in users:
        raise HTTPException(status_code=400, detail="Username already registered")
    users[user.username] = hashed_password
    return {"username": user.username}

# Endpoint to get all usernames (for demo purposes)
@app.get("/users/")
def get_users():
    return {"users": list(users.keys())}

# Endpoint to check Instagram login
@app.post("/check_login")
async def check_login(username: str = Form(...), password: str = Form(...)):
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

# Endpoint to post on Instagram
@app.post("/post_to_instagram")
async def post_instagram(username: str = Form(...), password: str = Form(...),
                         image_path: str = Form(...), caption: str = Form(''),
                         first_comment: str = Form('')):
    login_status, driver = check_instagram_login(username, password)
    if login_status:
        # If login successful, attempt to post
        post_status = post_to_instagram(driver, image_path, caption, first_comment)
        if post_status:
            return {"message": "Post successful"}
        else:
            raise HTTPException(status_code=500, detail="Failed to post on Instagram")
    else:
        # If login failed, raise HTTPException
        raise HTTPException(status_code=401, detail="Login failed")
    
# # Endpoint to message multiple Instagram IDs
# @app.post("/message_multiple_ids")
# async def message_instagram_multiple_ids(username: str = Form(...), password: str = Form(...),
#                                         ids: list = Form(...), message_text: str = Form(...)):
#     login_status, driver = check_instagram_login(username, password)
#     if login_status:
#         action_result = perform_instagram_action(driver, message_multiple_ids, ids, message_text)
#         if action_result:
#             return {"message": f"Message sent to {len(ids)} Instagram IDs successfully"}
#         else:
#             raise HTTPException(status_code=500, detail="Failed to send message to Instagram IDs")
#     else:
#         raise HTTPException(status_code=401, detail="Login failed")


# Endpoint to comment on a post
@app.post("/comment_on_post")
async def comment_instagram_post(username: str = Form(...), password: str = Form(...),
                                 post_url: str = Form(...), comment_text: str = Form(...)):
    login_status, driver = check_instagram_login(username, password)
    if login_status:
        # If login successful, attempt to comment
        comment_status = comment_on_post(driver, post_url, comment_text)
        if comment_status:
            return {"message": f"Comment '{comment_text}' added successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to comment on post")
    else:
        # If login failed, raise HTTPException
        raise HTTPException(status_code=401, detail="Login failed")

# Endpoint to like a post
@app.post("/like_post")
async def like_instagram_post(username: str = Form(...), password: str = Form(...),
                              post_url: str = Form(...)):
    login_status, driver = check_instagram_login(username, password)
    if login_status:
        # If login successful, attempt to like the post
        like_status = like_post(driver, post_url)
        if like_status:
            return {"message": "Post liked successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to like the post")
    else:
        # If login failed, raise HTTPException
        raise HTTPException(status_code=401, detail="Login failed")

# Endpoint to keep a story
@app.post("/keep_story")
async def keep_instagram_story(username: str = Form(...), password: str = Form(...)):
    login_status, driver = check_instagram_login(username, password)
    if login_status:
        # If login successful, attempt to keep the story
        keep_status = keep_story(driver)
        if keep_status:
            return {"message": "Story kept successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to keep the story")
    else:
        # If login failed, raise HTTPException
        raise HTTPException(status_code=401, detail="Login failed")

# Endpoint to follow a user
@app.post("/follow_user")
async def follow_instagram_user(username: str = Form(...), password: str = Form(...),
                                username_to_follow: str = Form(...)):
    login_status, driver = check_instagram_login(username, password)
    if login_status:
        # If login successful, attempt to follow the user
        follow_status = follow_user(driver, username_to_follow)
        if follow_status:
            return {"message": f"Followed user '{username_to_follow}' successfully"}
        else:
            raise HTTPException(status_code=500, detail=f"Failed to follow user '{username_to_follow}'")
    else:
        # If login failed, raise HTTPException
        raise HTTPException(status_code=401, detail="Login failed")
