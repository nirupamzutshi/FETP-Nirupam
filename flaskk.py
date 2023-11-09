from flask import Flask, request, redirect, url_for, session
import secrets
import requests

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
CLIENT_ID = '1035490928140-bbleqfca1ca217be6rc0b25idci5k6ut.apps.googleusercontent.com' 
CLIENT_SECRET = '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' 
REDIRECT_URI = 'http://localhost:5000/oauth2callback'  

@app.route('/')
def home():
    return 'Welcome to your Gmail sign-in application! <a href="/login">Sign in with Gmail</a>'

@app.route('/login')
def login():
    
    state = secrets.token_urlsafe(16)
    session['state'] = state

    
    auth_url = f'https://accounts.google.com/o/oauth2/auth?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope=https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email&response_type=code&state={state}'

    return redirect(auth_url)

@app.route('/oauth2callback')
def oauth2callback():
    if 'code' in request.args and 'state' in request.args and request.args['state'] == session.get('state'):
        code = request.args.get('code')

        token_url = 'https://oauth2.googleapis.com/token'
        token_params = {
            'code': code,
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'redirect_uri': REDIRECT_URI,
            'grant_type': 'authorization_code',
        }
        
        
        response = requests.post(token_url, data=token_params)
        token_data = response.json()

        if 'access_token' in token_data:
            access_token = token_data['access_token']

           
            user_info_url = 'https://www.googleapis.com/oauth2/v3/userinfo'
            headers = {'Authorization': f'Bearer {access_token}'}

            user_info_response = requests.get(user_info_url, headers=headers)
            user_info_data = user_info_response.json()

            
            user_name = user_info_data.get('name', '')
            profile_picture_url = user_info_data.get('picture', '')

            
            return f'Name: {user_name}<br><img src="{profile_picture_url}" width="100"><br><br><a href="/logout">Sign out</a> Hello {user_name} \n you are signed in'

    return 'Authorization failed.'

@app.route('/logout')
def logout():
    
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
