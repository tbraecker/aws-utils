# check_iam_stuff

We wanted to monitor our IAM permissions and find out what access_keys/passwords are not used.
For this purpose I created this script that does the following things:

1. Check when the user used their password to login
2. Check when the user used their access_keys
3. Check for dead users (no password or access_key)
4. Check for admins without MFA-authentication
5. Check for empty groups

If passwords/access_keys are older than 30 days (to change in main class) the script will print it out

**This script only checks this things but does not delete anything**
