# SharePost
A social media platform that allows users to post, and comment. Creating accounts, bios, and setting a status. Users can also view other users profiles.

## Website
Click [here](https://sharepost.jonathan2018.repl.co/) to go the official SharePost website. You can create an account there or login.

## Using SharePost
### Creating an account
The first step in using SharePost is to create an account. If you are not signed in, the first thing on the site is telling you to login. If you don't have an account to sign in to, then click the `Don't have an account?` button. There, you will have the steps to creating your account.

### Logging In
If you created your account, or have an account but your aren't signed in, then go to the login page, and login with your username & password. 

**Note:** Your username should not contain the @ when signing in or creating an account. That will be added automatically.

### Homepage
After logging in, you should see the homepage with some posts. You can click on the posts, read them, and comment on them. The views will also increment by 1 everytime you visit a post. 

### Creating a post
You can create a post by clicking the plus icon at the top-right corner. There, you think of a title, and write the body of the post. The post has a limited number of characters (350 chars) so make each word matter!

### After publishing
After publishing, you will be brought to your post page by default. There, you can see the comments, and views. The comments & views are not live as of right now.

## Deleting
You can delete a single post. Go to the post you want to delete **(that is owned by you)**. There, you should see a circular trash can icon at the top right of your post. Click it, and it will delete **immediately**.

**Note:** Comments can not be individually deleted.

Delete Account in: Account -> 'DELETE ACCOUNT | Posts & comments will stay.'. Your account, and piece of information part of it will be removed from our databases. But your posts and comments will stay, though they will be anonymized under the name `[DELETED_ACCOUNT]`.

Delete EVERYTHING in: Account -> 'DELETE EVERYTHING | Everything including account.'. Everything will be deleted and nothing is saved unlike the previous options.

### Account page
On the account page at the top right. You can edit your username, set a bio, and a status. 

**Note:** If you choose to change your username, there maybe consequences. Your old profile page & username can be taken by someone else. All your posts and comments will be updated to your new username. If you accidentally changed your account name, but haven't clicked save, quickly click back home.

### Profile page
The profile page is public so it can be viewed by anyone including yourself. You can open other people's profiles by clicking on their profile picture on a post or comment they made. You can also just enter their username into the url.

## API
SharePost has an API that is free to use, and is accessible to anyone, even people without an account. The API only transfers a person's profile for now. 

- Send a request to `https://sharepost.jonathan2018.repl.co/api?profile=@Profile"`. Replace the @Profile with whatever username including the `@`. It is case-insensitive.
- SharePost will return the data of the account in JSON format. See example below:
```json
{
  "bio": "Developer of this platform.", 
  "comments": 15, 
  "posts": 5, 
  "profile_picture": "https://SharePost.jonathan2018.repl.co/static/images/profile/pfp-5.png", 
  "status": "Busy developing", 
  "username": "@Jonathan2018"
}
```
- You can do whatever you want with the data. More data could be added in the future, though it will not be too specific.
