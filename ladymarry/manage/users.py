from flask.ext.script import Command, prompt

from ..services import users, waiting_users


class ListWaitingUserCommand(Command):
    def run(self):
        for u in waiting_users.all():
            print 'email: %s \t registered_at: %s' % (u.email, u.registered_at)


class DeleteWaitingUserCommand(Command):
    def run(self):
        email = prompt('email')
        u = waiting_users.first(email=email)
        if not u:
            print 'Invalid email.'
        else:
            waiting_users.delete(u)
            print 'Delete successfully.'
