import requests
import urllib
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
from clarifai.rest import ClarifaiApp


APP_ACCESS_TOKEN = '1460590625.b4a2325.64a3386400124dfa93f31e777e6a0aae'


BASE_URL = 'https://api.instagram.com/v1/'

#Function declaration to get your own info


def self_info():
    request_url = (BASE_URL + 'users/self/?access_token=%s') % (APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            print 'Username: %s' % (user_info['data']['username'])
            print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (user_info['data']['counts']['media'])
        else:
            print 'User does not exist!'
    else:
        print 'Status code other than 200 received!'


#Function declaration to get the ID of a user by username


def get_user_id(insta_username):
    request_url = (BASE_URL + 'users/search?q=%s&access_token=%s') % (insta_username, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            return user_info['data'][0]['id']
        else:
            return None
    else:
        print 'Status code other than 200 received!'
        exit()


#Function declaration to get the info of a user by username


def get_user_info(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            print 'Username: %s' % (user_info['data']['username'])
            print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (user_info['data']['counts']['media'])
        else:
            print 'There is no data for this user!'
    else:
        print 'Status code other than 200 received!'


#Function declaration to get your recent post

def get_own_post():
    request_url = (BASE_URL + 'users/self/media/recent/?access_token=%s') % (APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    own_media = requests.get(request_url).json()

    if own_media['meta']['code'] == 200:
        if len(own_media['data']):
            image_name = own_media['data'][0]['id'] + '.jpeg'
            image_url = own_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print 'Your image has been downloaded!'
        else:
            print 'Post does not exist!'
    else:
        print 'Status code other than 200 received!'


#Function declaration to get the recent post of a user by username


def get_user_post(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            image_name = user_media['data'][0]['id'] + '.jpeg'
            image_url = user_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print 'Your image has been downloaded!'
        else:
            print 'Post does not exist!'
    else:
        print 'Status code other than 200 received!'

#Function declaration to get the ID of the recent post of a user by username


def get_post_id(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            return user_media['data'][0]['id']
        else:
            print 'There is no recent post of the user!'
            exit()
    else:
        print 'Status code other than 200 received!'
        exit()



#Function declaration to like the recent post of a use

def like_a_post(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/likes') % (media_id)
    payload = {"access_token": APP_ACCESS_TOKEN}
    print 'POST request url : %s' % (request_url)
    post_a_like = requests.post(request_url, payload).json()
    if post_a_like['meta']['code'] == 200:
        print 'Like was successful!'
    else:
        print 'Your like was unsuccessful. Try again!'


#Function declaration to make a comment on the recent post of the user


def post_a_comment(insta_username):
    media_id = get_post_id(insta_username)
    comment_text = raw_input("Your comment: ")
    payload = {"access_token": APP_ACCESS_TOKEN, "text" : comment_text}
    request_url = (BASE_URL + 'media/%s/comments') % (media_id)
    print 'POST request url : %s' % (request_url)

    make_comment = requests.post(request_url, payload).json()

    if make_comment['meta']['code'] == 200:
        print "Successfully added a new comment!"
    else:
        print "Unable to add comment. Try again!"


#Function declaration to make delete negative comments from the recent post

def delete_negative_comment(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/comments/?access_token=%s') % (media_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    comment_info = requests.get(request_url).json()

    if comment_info['meta']['code'] == 200:
        if len(comment_info['data']):
            #Here's a naive implementation of how to delete the negative comments :)
            for x in range(0, len(comment_info['data'])):
                comment_id = comment_info['data'][x]['id']
                comment_text = comment_info['data'][x]['text']
                blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())
                if (blob.sentiment.p_neg > blob.sentiment.p_pos):
                    print 'Negative comment : %s' % (comment_text)
                    delete_url = (BASE_URL + 'media/%s/comments/%s/?access_token=%s') % (media_id, comment_id, APP_ACCESS_TOKEN)
                    print 'DELETE request url : %s' % (delete_url)
                    delete_info = requests.delete(delete_url).json()

                    if delete_info['meta']['code'] == 200:
                        print 'Comment successfully deleted!\n'
                    else:
                        print 'Unable to delete comment!'
                else:
                    print 'Positive comment : %s\n' % (comment_text)
        else:
            print 'There are no existing comments on the post!'
    else:
        print 'Status code other than 200 received!'

# function to get list of users who like user's media
def get_like_list(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/likes?access_token=%s') % (media_id, APP_ACCESS_TOKEN)
    # Printing the url that is being called/requested

    print 'GET request url : %s' % (request_url)
    like_list = requests.get(request_url).json()
    print like_list

    if like_list['meta']['code'] == 200:
        if len(like_list['data']):
            for i in range(0, len(like_list['data'])):
                print 'Username: %s' % (like_list['data'][i]['username'])

        else:
            print 'There is no like for this user media!'
    else:
        print 'Query was unsuccessful!'


#This function depicts the values of various object in an image..
def image_depiction(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            image_name = user_media['data'][0]['id'] + '.jpeg'
            image_url = user_media['data'][0]['images']['standard_resolution']['url']

            app = ClarifaiApp(api_key='a9a2f1b7b8034a5baceb72f61a584b18')
            model = app.models.get("general-v1.3")
            response = model.predict_by_url(url=image_url)
            print response
        else:
            print 'Post does not exist!'
    else:
        print 'Status code other than 200 received!'

# Function to post the promotional message...
def post_promotional_comment(insta_promotional_message, insta_username):
    # Fetching recent media id
    media_id = get_post_id(insta_username)
    payload = {"access_token": APP_ACCESS_TOKEN, "text": insta_promotional_message}
    request_url = (BASE_URL + 'media/%s/comments') % (media_id)
    # Printing the url that is being called/requested
    print 'POST request url : %s' % (request_url)

    # Commenting the
    make_comment = requests.post(request_url, payload).json()

    if make_comment['meta']['code'] == 200:
        print "Successfully added a promotional comment!"
    else:
        print "Unable to add comment. Try again!"


#function to do Marketing on Instagram..
def insta_marketing(insta_keyword,insta_promotional_message,insta_username):
    # Analyze comments
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/comments/?access_token=%s') % (media_id, APP_ACCESS_TOKEN)
    # Printing the url that is being called/requested
    print 'GET request url : %s' % (request_url)
    comment_info = requests.get(request_url).json()
    print comment_info
    if comment_info['meta']['code'] == 200:

        if len(comment_info['data']):

            for index_var in range(0, len(comment_info['data'])):
                comment_text = comment_info['data'][index_var]['text']
                print comment_text
                comment_words = comment_text.split()
                print comment_words
                for i in range(0,comment_words.__len__()):
                    if(comment_words[i] == insta_keyword):
                        post_promotional_comment(insta_promotional_message,insta_username)
                        break
    else:
        print 'Status code other than 200 received'

    # Analyze tags
    request_url = (BASE_URL+'media/%s?access_token=%s') % (media_id, APP_ACCESS_TOKEN)
    # Printing the url that is being called/requested
    print 'GET request url : %s' % (request_url)
    media_data=requests.get(request_url).json()

    if(media_data) is not None:

        print media_data

        if (media_data['meta']['code']== 200):

            if len(media_data['data']['tags']):
                # Fetching the tags on a post
                insta_tag = media_data['data']['tags']
                for index_var in range(0,insta_tag.__len__()):
                    if insta_tag[index_var]==insta_keyword:
                        print insta_tag[index_var]
                        post_promotional_comment(insta_promotional_message,insta_username)
                        break
                    else:
                        print 'Not matched'
            else:
                print 'No tags'

    #Analyzing Caption

            if (media_data['data']['caption']) is not None:
            # Fetching the captions on a post
                insta_caption = media_data['data']['caption']['text']
                type(insta_caption)
                insta_caption_words = insta_caption.split()

                for p in range(0, insta_caption_words.__len__()):
                    if (insta_caption_words[p] == insta_keyword):
                        print insta_caption_words[p]
                        post_promotional_comment(insta_promotional_message, insta_username)
                        break
                    else:
                        print 'Not matched'
            else:
                print 'No caption'
        else:
            print 'Status code other than 200 received'
    else:
        print 'Media Does not Exist'


def start_bot():
    while True:
        print '\n'
        print 'Hey! Welcome to instaBot!'
        print 'Here are your menu options:'
        print "a.Get your own details\n"
        print "b.Get details of a user by username\n"
        print "c.Get your own recent post\n"
        print "d.Get the recent post of a user by username\n"
        print "e.Like the recent post of a user\n"
        print "f.Make a comment on the recent post of a user\n"
        print "g.Delete negative comments from the recent post of a user\n"
        print "h.Get a list of people who have liked the recent post of a user\n"
        print "i.Image Depiction\n"
        print "j.For Marketing over Instagram\n"
        print "k.Exit"

        choice = raw_input("Enter you choice: ")
        if choice == "a":
            self_info()
        elif choice == "b":
            insta_username = raw_input("Enter the username of the user: ")
            get_user_info(insta_username)
        elif choice == "c":
            get_own_post()
        elif choice == "d":
            insta_username = raw_input("Enter the username of the user: ")
            get_user_post(insta_username)
        elif choice == "e":
           insta_username = raw_input("Enter the username of the user: ")
           like_a_post(insta_username)
        elif choice == "f":
           insta_username = raw_input("Enter the username of the user: ")
           post_a_comment(insta_username)
        elif choice == "g":
           insta_username = raw_input("Enter the username of the user: ")
           delete_negative_comment(insta_username)
        elif choice == "h":
            insta_username = raw_input("Enter the username of the user: ")
            get_like_list(insta_username)
        elif choice == "i":
            insta_username = raw_input("Enter the username of the user: ")
            image_depiction(insta_username)
        elif choice == "j":
            insta_keyword = raw_input("Enter the keyword to be searched :")
            insta_promotional_message = raw_input("Enter the text to be commented :")
            insta_username = raw_input("Enter the username :")
            insta_marketing(insta_keyword, insta_promotional_message, insta_username)
        elif choice == "k":
            exit()
        else:
            print "wrong choice"

start_bot()