Automate Instagram Uploads
===========

This tool allows you to automatically upload photos (not videos, sadly) to Instagram - and also set a caption.
<br/><br/>

Background
----------------

I was looking for a way for my app to automatically upload photos to Instagram but quickly found that not only does their API suck in general, it doesn't even have an upload endpoint. You HAVE to physically click, upload and whatnot.

Over the course of my research, I found uploads to be the most sought-after feature for developers. I began looking into custom Instagram APIs such as [Instagram-PHP](https://packagist.org/packages/mgp25/instagram-php), [Instabot](https://github.com/ohld/igbot), [InstaPy](https://github.com/timgrossmann/InstaPy) and a few more. All of them were either simplified versions of Instagram's existing API lacking the upload endpoint, or otherwise Instagram would notice it was a script and do a robot-check which would require manual intervention. Furthermore, they're issuing DMCA requests against custom APIs and banning the accounts of those that use them - all in all, not worth it.

Turns out if you make your browser window tiny and change your User Agent to a mobile browser, Instagram DOES allow uploads through the web interface. With that in mind I began to try a Selenium based approach, first problem, I'd never used Selenium - but turns out it's ridiculously simple. I ~~stole~~ used a lot of [OZKC's scripts](https://github.com/ozkc/selenium-instagram-uploader) as a starting point but ran into a few issues getting it working, plus I felt I could improve it.

What we have now is a very simple Docker container running a Python script containing some Selenium elements and a cursor macro. Feed in the information you need as arguments and boom!
<br/><br/>

Installation
----------------

        # git clone https://github.com/RunlevelConsulting/Automate-Instagram-Uploads.git
        # cd Automate-Instagram-Uploads/
        # sudo docker build --tag igloginandpost:1.0 .
        # sudo docker run -d -v $(pwd):/root/Desktop/:ro --name igloginandpost igloginandpost:1.0


Uploading to Instagram
----------------

The photo upload is managed by a script named **IGLoginAndPost.py**, it has 4 arguments:

 1. Your Instagram username
 2. Your Instagram password
 3. The URL of the image you wish to upload (leave empty for local upload)
 4. The caption you want to go with the image

### Method 1: Upload Image From Web
        # sudo docker exec -d -e DISPLAY=:1 -i igloginandpost bash -c 'python IGLoginAndPost.py "<Insta Username>" "<Insta Password>" "https://example.com/link/to/image.jpg" "<Your Upload Caption>"'

### Method 2: Upload Local Image
        # sudo docker cp /path/to/MyImage.jpg igloginandpost:/home/ubuntu/Desktop/pic.jpg
        # sudo docker exec -d -e DISPLAY=:1 -i igloginandpost bash -c 'python IGLoginAndPost.py "<Insta Username>" "<Insta Password>" "" "<Your Upload Caption>"'

Wait around **1 minute** after you run this command and it should appear as an upload.
<br/><br/>

Important Stuff To Note!
------
### Single & Double Quotes
**Do not use single or double quotes in your caption.** Bash parses the 'docker exec' command badly, I did try escaping but it didn't seem to cooperate. I didn't really dwell on it, but if you get it working, let me know.

### Local Image Uploads
If copying a locally-held image into the Docker container, it **must** be placed into the **/home/ubuntu/Desktop/** directory inside the container and it **must** be the only image in that directory. This is due to what the cursor macro expects.

### User Agents
The Python script sets a fake User Agent for Selenium. Instagram may start to get wise that people are using this tool and bad things could happen, one method to avoid this would be to modify the **user_agent** variable in the script to another mobile phone user agent. See [alternatives](https://deviceatlas.com/blog/mobile-browser-user-agent-strings).

### Two-Factor Authentication
This won't work with it switched on.

### Not Working?
If no image is being uploaded, ditch your container and  run:

 1.     # sudo docker run -d -v $(pwd):/root/Desktop/:ro --name igloginandpost -p 6080:80 -p 5900:5900 igloginandpost:1.0
 2. Browse to: [http://127.0.0.1:6080/](http://127.0.0.1:6080/) to see the container GUI
 3.     # sudo docker exec -e DISPLAY=:1 -i igloginandpost bash -c 'python /root/Desktop/IGLoginAndPost.py "<Insta Username>" "<Insta Password>" "" "<Your upload caption>"' 
This method will allow you to watch the Selenium in action and hopefully work out what's going wrong. It'll also alert you in your terminal if your 'docker exec' command is malformed.
