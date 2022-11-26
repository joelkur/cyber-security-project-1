# cyber-security-project-1

A TODO app with security flaws.

## Setup

1. Clone the repository with `git clone https://github.com/joelkur/cyber-security-project-1.git`
2. In the project root folder, run migrations with `python3 manage.py migrate`
3. Create test data with `python3 manage.py initdatabase`
4. Run the server with `python3 manage.py runserver`
5. The project should be running at http://localhost:8000

### Test users
The `initdatabase` command creates the following users:

- admin:admin
- user1:user1
- user2:user2

## Flaws

### Flaw 1: [Cryptographic Failure](https://owasp.org/Top10/A02_2021-Cryptographic_Failures/)
Links to the flaw sources:
- [/todoapp/models.py#L11](/todoapp/models.py#L11)

Currently raw passwords are stored in database unencrypted. This is not ideal as the passwords of all users might potentially be leaked if the site gets hacked.

A simple fix for this could be using Django's built-in password management for hashing and other password related logic. Since the `User` model class is extended from `AbstractUser`, which already has password hashing functionality, the `set_password` and `check_password` methods could simply be removed in `User` model.

### Flaw 2: [Broken Access Control](https://owasp.org/Top10/A01_2021-Broken_Access_Control/)
Links to the flaw sources:
- [/todoapp/views.py#L9](/todoapp/views.py#L9)
- [/todoapp/views.py#L20](/todoapp/views.py#L20)

Currently it is permitted to modify todos of other users. One could, for example, on any authenticated account iterate through possible todo id's and modify or delete the todo regardless of whether the todo belongs to the requesting user.

This can be fixed by implementing a check that the user matches the owner of the target resource, and if a mismatch occurs the access should be prevented. Both of the views containing the flaw has commented out code for a possible fix.

Links to the fixes:
- [/todoapp/views.py#L12](/todoapp/views.py#L12)
- [/todoapp/views.py#L23](/todoapp/views.py#L23)
