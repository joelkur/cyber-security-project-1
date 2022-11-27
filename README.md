# cyber-security-project-1

A todo app with security flaws.

## Setup

As prerequisities python 3 and django should be installed. The course's [installation instructions](https://cybersecuritybase.mooc.fi/installation-guide) should be enough to get everything needed installed.

### Installing and running the project
1. Clone the repository with `git clone https://github.com/joelkur/cyber-security-project-1.git`
2. In the project root folder, run migrations with `python3 manage.py migrate`
3. Create test data with `python3 manage.py initdatabase`
4. Run the server with `python3 manage.py runserver`
5. The project should be running at http://localhost:8000

### Test users
The `initdatabase` command creates the following users:

- admin:admin
- alice:redqueen
- bob:squarepants

## Flaws

### Flaw 1: [Cryptographic Failure](https://owasp.org/Top10/A02_2021-Cryptographic_Failures/)
Links to the flaw sources:
- [/todoapp/models.py#L9](/todoapp/models.py#L9)
- [/todoapp/models.py#L13](/todoapp/models.py#L13)

Currently raw passwords are stored in database unencrypted. This is not ideal as the passwords of all users might potentially be leaked if the site gets hacked. The impact of this vulnerability is described in more detail in flaw 3.

A simple fix for this could be using Django's built-in password management for hashing and other password related logic. Since the `User` model class is extended from `AbstractUser`, which already has password hashing functionality, the `set_password` and `check_password` methods could simply be removed in `User` model to enable Django's original password management functionality.

Below are links to Django's built-in way of handling passwords, found in the Django source code:
https://github.com/django/django/blob/main/django/contrib/auth/hashers.py#L38
https://github.com/django/django/blob/main/django/contrib/auth/hashers.py#L72

### Flaw 2: [Broken Access Control](https://owasp.org/Top10/A01_2021-Broken_Access_Control/)
Links to the flaw sources:
- [/todoapp/views.py#L8](/todoapp/views.py#L8)
- [/todoapp/views.py#L19](/todoapp/views.py#L19)
- [/todoapp/views.py#L31](/todoapp/views.py#L31)

Currently it is permitted to view details or modify todos of other users. One could, for example, on any authenticated account iterate through possible todo id's and access or modify or delete the todo regardless of whether the todo belongs to the requesting user. To reproduce this, with the initial test data log in with e.g. user `bob` and go to link http://localhost:8000/todos/10/. This should open a view that displays todo belonging to user `alice` - with the ability to mark the todo as done or delete it.

This can be fixed by implementing a check that the requesting user matches the owner of the target resource, and if a mismatch occurs the access should be prevented. Each of the views containing the flaw has commented out code for a possible fix.

Links to the fixes:
- [/todoapp/views.py#L11](/todoapp/views.py#L11)
- [/todoapp/views.py#L22](/todoapp/views.py#L22)
- [/todoapp/views.py#L34](/todoapp/views.py#L34)

### Flaw 3: [SQL injection](https://owasp.org/Top10/A03_2021-Injection/)
Links to the flaw sources:
- [/todoapp/views.py#L55](/todoapp/views.py#L55)

The todo search functionality is vulnerable to SQL injections. This is a critical issue as a hacker can access anything in the database via the SQL injection. For example, here we can see the impact of the unencrypted passwords described in flaw 1, as with a SQL injection it is possible to retrieve plaintext passwords for each user.

To reproduce the SQL injection in the application, you can type e.g. `%' UNION SELECT username, password FROM auth_user WHERE username LIKE '%%` to the search input and then press search. This should display all todos, and additionally plaintext passwords of each user in the list. Although not visible in the rendered view in browser, also usernames of each user is included in the response, which can be seen if inspecting the raw HTML response. The username is included in the `href`s of links under `li` elements, in the format of `/todos/{username}/...`.

One fix for this flaw is to use Django's built-in object relational mapper for building, executing and reading the database query. This suggested fix is commented out in the code after the flawed line. Another way of fixing the issue via raw SQL would be by using prepared statements. Prepared statements builds the query beforehand without executing it, leaving placeholders for parameters. Later the compiled query can be executed with different input as parameters, without the worry of the input affecting the original query. Prepared statements are typically written in following format `SELECT * FROM table WHERE column = ?`, where `?` is placeholder for parameters.

Links to the fixes:
- [/todoapp/views.py#L58](/todoapp/views.py#L58)

### Flaw 4: [Cross-site scripting (XSS)](https://owasp.org/Top10/A03_2021-Injection/)
Links to the flaw sources:
- [/project/settings.py#73](/project/settings.py#L73)

Currently any user input is not escaped before sending rendered HTML to users, meaning that any user input gets rendered as-is to the document. This makes the application vulnerable to XSS, as an attacker may enter e.g. malicious javascript to the input fields, that are then executed on the user's browser. This could especially be dangerous when combined with broken access control, as an attacker could e.g. create a todo with malicious input and send link to that todo to a group of target users. The malicious script may, for example, read the visiting user's session and send it to the attacker.

One way of reproducing this scenario can be achieved with the following steps:
1. Log in with `alice`
2. To one of the input fields in "Add new todo" form, write `<script>alert(document.cookie)</script>`, and submit the form
3. Copy the link of the new todo to clipboard, log out and login with `bob`
4. Go to the link in clipboard
5. Now an alert should appear containing the contents of bob's cookie

In this particular case, the root of the issue comes from the project settings, where templates are configured to not automatically escape user input. Removing this line enables the automatic input escaping functionality and thus fixing XSS issues.

Links to the fixes:
- [/project/settings.py#73](/project/settings.py#L73)

### Flaw 5: [Identification and Authentication Failures](https://owasp.org/Top10/A07_2021-Identification_and_Authentication_Failures/)
Links to the flaw sources:
- [/project/session.py#L5](/project/session.py#L5)
- [/project/settings.py#L34](/project/settings.py#L34)

Session keys are predictable and sessions are not invalidated during logout. This can lead to session hijacking meaning an attacker can impersonate other users. Since the session key is predictable and not properly invalidated, an attacker could easily guess session keys by brute forcing it. Also, session cookie is accessible with javascript, meaning that combined with an XSS attack an attacker can access the session key.

The session key should be fixed to be unpredictable, as an example a securely generated random bytes. The session should also be expired and invalidated when the user logs out of the system. Django has this functionality already built-in, so again a simple fix in this application would be to remove the custom `SessionStore` and use Django's built-in one.

To fix the session cookie being accessible with javascript, the session cookie should be set as HTTP only.

Links to the fixes:
- [/project/settings.py#L30](/project/settings.py#L30)
- [/project/settings.py#L33](/project/settings.py#L33)
