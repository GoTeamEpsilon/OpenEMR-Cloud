_[< previous chapter](06-Application-Servers.md) | [next chapter >](08-Administration.md)_

# ▶ Secure Domain Setup

_this section is under construction!!!_
### Route53 stuff
1. Go to Route53, and in the text box near the middle of the page enter the domain name you'd like to register. This will be what you type in your browser to access your OpenEMR instance.
2. Click "Add To Cart" if the domain is available.
3. If it is n to available, check for another site or choose one of the "Related domain suggestions".
4. Click "Continue"
5. Enter your "Registrant Contact" information. XYZ XYZ XYZ
6. Click Continue
7. Click "Complete Purchase"
8. You should be directed back to the main dashboard.

### Certificate Manager
1. Go to AWS Certificate Manager
2. Click on "Get Started"
3. In the text box in the middle of the screen type in "yourdomain.com" and then click XYZ and in the new box type "*.yourpractice.com". The asterisk followed by a dot (and then followed by your domain name) is important because it enables SSL for various versions how your site is typed into a browser and later subdomains.
4. Click "Review and request".
5. Click "Confirm and request".
6. The request has now been made. Click "Continue" to head to the next screen where you will see your domain in the "Pending verification" state.
7. Go to the email associated with your account.
8. You might have multiple emails from AWS. Don't worry and simply click the link in each of them and approve.
9. You should now be approved and you have enabled SSL/TLS for your sites on AWS!!!
