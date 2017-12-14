Community authentication 2.0
============================
While the old community authentication system was simply having the
clients call a PostgreSQL function on the main website server, version
2.0 of the system uses browser redirects to perform this. This allows
for a number of advantages:

* The users password never hits the "community sites", only the main
  website. This has some obvious security advantages.
* There is no need to allow external access from these sites to the
  PostgreSQL database on the main website.
* It is possible for the user to get single sign-on between all the
  community sites, not just same-password.

Each community site is still registered in the central system, to hold
encryption keys and similar details. This is now held in the main
database, accessible through the django administration system, instead
of being held in pg_hba.conf and managed through SQL.

The flow of an authentication in the 2.0 system is fairly simple:

#. The user tries to access a protected resource on the community
   site.
#. At this point, the user is redirected to an URL on the main
   website, specifically https://www.postgresql.org/account/auth/<id>/.
   The <id> number in this URL is unique for each site, and is the
   identifier that accesses all encryption keys and redirection
   information.
   In this call, the client can optionally include a parameter
   *d*, which will be passed through back on the login confirmation.
   This should be a base64 encoded parameter (other than the base64
   character, the *$* character is also allowed and can be used to
   split fields).
   The client should encrypt or sign this parameter as necessary, and
   without encryption/signature it should *not* be trusted, since it
   can be injected into the authentication process without verification.
#. The main website will check if the user holds a valid, logged in,
   session on the main website. If it does not, the user will be
   sent through the standard login path on the main website, and once
   that is done will be sent to the next step in this process.
#. The main website puts together a dictionary of information about
   the logged in user, that contains the following fields:

   u
    The username of the user logged in
   f
     The first name of the user logged in
   l
     The last name of the user logged in
   e
     The email address of the user logged in
   d
     base64 encoded data block to be passed along in confirmation (optional)
   su
     *DEPRECATED* The suburl to redirect to (optional)
   t
     The timestamp of the authentication, in seconds-since-epoch. This
     should be validated against the current time, and authentication
     tokens older than e.g. 10 seconds should be refused.

#. This dictionary of information is then URL-encoded.
#. The resulting URL-encoded string is padded with spaces to an even
   16 bytes, and is then AES encrypted with a shared key. This key
   is stored in the main website system and indexed by the site id,
   and it is stored in the settings of the community website somewhere.
   Since this key is what protects the authentication, it should be
   treated as very valuable.
#. The resulting encrypted string and the IV used for the encryption are
   base64-encoded (in URL mode, meaning it uses - and _ instead of + and /.
#. The main website looks up the redirection URL registered for this site
   (again indexed by the site id), and constructs an URL of the format
   <redirection_url>?i=<iv>&d=<encrypted data>
#. The user browser is redirected to this URL.
#. The community website detects that this is a redirected authentication
   response, and stars processing it specifically.
#. Using the shared key, the data is decrypted (while first being base64
   decoded, of course)
#. The resulting string is urldecoded - and if any errors occur in the
   decoding, the authentication will fail. This step is guaranteed to fail
   if the encryption key is mismatching between the community site and
   the main website, since it is going to end up with something that is
   definitely not an url-decodeable string.
#. The community site will look up an existing user record under this
   username, or create a new one if one does not exist already (assuming
   the site keeps local track of users at all - if it just deals with
   session users, it can just store this information in the session).
   It is recommended that the community site verifies if the first name,
   last name or email field has changed, and updates the local record if
   this is the case.
#. The community site logs the user in using whatever method it's framework
   uses.
#. If the *d* key is present in the data structure handed over, the
   community site implements a site-specific action based on this data,
   such as redirecting the user to the original location.
#. *DEPRECATED* If the *su* key is present in the data structure handed over, the
   community site redirects to this location. If it's not present, then
   the community site will redirect so some default location on the
   site.

Logging out
-----------
If the community site implements functionality to log the user out, it
should also send a redirect to the main website to cause a logout from
this site as well. If this is not done, it will appear to the user as if
the logout didn't work, since upon next login the user is redirected and
automatically logged in again.

The flow for a logout request is trivial:

#. The community website logs the user out of the local instance, however
   that works.
#. The community website redirects the user to
   https://www.postgresql.org/account/auth/<id>/logout/ (where the id
   number is the same id as during login)
#. The main website will log the user out of the community site
#. The main website redirects the user back to the community website,
   at the URL <redirection_url>?s=logout (where redirection_url is the
   same URL as when logging in)

Searching
---------
The community authentication system also supports an API for searching for
users. The idea here is to give the ability to add a user to downstream
systems even if that user has not yet logged in (normally the user is added
on first login).

In order to not leak sensitive information about users, all search results
are returned encrypted with the same key as the authentication scheme.

The flow for search is:

#. Make an API call to
   https://www.postgresql.org/account/auth/<id>/search/?<params>
   where the id is the same id as during login, and params can be one of
   the following:

   s
    Case insensitive substring search of name and email
   n
    Case insensitive substring search of name
   e
    Case insensitive substring search of email
   u
    Exact search of username

#. The returned data will be an array of JSON objects, with the following keys:

   u
    Username
   e
    Email
   f
    First name
   l
    Last name
