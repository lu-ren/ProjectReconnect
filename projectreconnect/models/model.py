from sqlalchemy.ext.associationproxy import association_proxy
from projectreconnect import db
from .constants import *

class Attend(db.Model):
    __tablename__ = 'attend'

    uid = db.Column(db.Integer, db.ForeignKey('user.uid'), primary_key=True)
    gid = db.Column(db.Integer, db.ForeignKey('group.gid'), primary_key=True)
    user_role = db.Column(db.Enum(*GroupRoles.roles, name='role'))

    group = db.relationship('Group',
        backref=db.backref('user_groups', cascade='all, delete-orphan'))

    user = db.relationship('User',
        backref=db.backref('user_groups', cascade='all, delete-orphan'))

    def __json__(self):
        return ['uid', 'gid', 'user_role']

    def __eq__(self, other):
        return (self.uid == other.uid and self.gid == self.oid)

    def __repr__(self):
        return "<Attend(uid=%s, gid=%s, user_role=%s)>" \
            % (self.uid, self.gid, self.user_role)

followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.uid')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.uid')))

#Universities/high schools etc
class Organization(db.Model):
    __tablename__ = 'organization'

    oid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.Text)

    users = db.relationship('User', back_populates='organization')
    groups = db.relationship('Group', back_populates='organization')

    def add_user(self, user):
        if not self.has_user(user):
           self.users.append(user)
        else:
            raise ValueError('user %s already exists' % user)

    def remove_user(self, user):
        if self.has_user(user):
            self.users.remove(user)
        else:
            raise ValueError('user %s does not exist' % user)

    def add_group(self, group):
        if not self.has_group(group):
           self.groups.append(group)
        else:
            raise ValueError('group %s already exists' % group)

    def remove_group(self, group):
        if self.has_group(group):
            self.groups.remove(group)
        else:
            raise ValueError('group %s does not exist' % group)

    def has_user(self, user):
        return (user in self.users)

    def has_group(self, group):
        return (group in self.groups)

    def __json__(self):
        return ['oid', 'name', 'description']

    def __eq__(self, other):
        return (self.oid == other.oid)

    def __repr__(self):
        return "<Organization(oid=%s, name=%s)>" % (self.oid, self.name)

class User(db.Model):
    __tablename__ = 'user'

    uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    social_id = db.Column(db.String, unique=True, nullable=False)
    oid = db.Column(db.Integer, db.ForeignKey('organization.oid'), nullable=False)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True)
    pic_path = db.Column(db.String, unique=True)
    description = db.Column(db.Text)

    organization = db.relationship('Organization', back_populates='users')

    registered_groups = association_proxy('user_groups', 'group',
        creator=lambda g: Attend(group=g, user_role=GroupRoles.roles[0]))

    tags = db.relationship('Tag', back_populates='user')

    #self-referential many-to-many relationship for follow feature
    followed = db.relationship('User',
            secondary=followers,
            primaryjoin=(followers.c.follower_id == uid),
            secondaryjoin=(followers.c.followed_id == uid),
            backref=db.backref('followers', lazy='dynamic'),
            lazy='dynamic')

    def add_group(self, group, role):
        if not has_group(group):
            self.user_groups.append(Attend(group=group, user_role=role))
        else:
            raise ValueError('group %s already exists' % group)

    def remove_group(self, group):
        if has_group(group):
            self.registered_groups.remove(group)
        else:
            raise ValueError('group %s does not exist' % group)

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
            return self
        else:
            raise ValueError('user %s already exists' % user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)
            return self
        else:
            raise ValueError('user %s does not exist' % user)

    def add_tag(self, tag):
        if not self.has_tag(tag):
            self.tags.append(tag)
        else:
            raise ValueError('tag %s already exists' % tag)

    def remove_tag(self, tag):
        if self.has_tag(tag):
            self.tags.remove(tag)
        else:
            raise ValueError('tag %s does not exist' % tag)

    def has_group(self, group):
        return (group in self.registered_groups)

    def is_following(self, user):
        return (self in user.followers)

    def has_tag(self, tag):
        return (tag in self.tags)

    #Not supporting banning users yet
    def is_active(self):
        return True

    def get_id(self):
        return self.social_id

    def is_authenticated(self):
        return True

    #Not supporting anonymous users
    def is_anonymous(self):
        return False

    def __json__(self):
        return ['uid', 'oid', 'name', 'email', 'pic_path', 'description']

    def __eq__(self, other):
        return (self.uid == other.uid)

    def __repr__(self):
        return "<User(uid=%s, name=%s)>" %(self.uid, self.name)

class Group(db.Model):
    __tablename__ = 'group'

    gid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    oid = db.Column(db.Integer, db.ForeignKey('organization.oid'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, db.CheckConstraint('end_time > start_time'), nullable=False)
    location = db.Column(db.String, nullable=False)
    pic_path = db.Column(db.String, unique=True)
    description = db.Column(db.Text)

    organization = db.relationship('Organization', back_populates='groups')

    #many-to-many db.relationship with users
    registered_users = association_proxy('user_groups', 'user',
        creator=lambda u: Attend(user=u, user_role=GroupRoles.roles[0]))

    #one to many db.relationship with tags
    tags = db.relationship('Tag', back_populates='group')

    def add_user(self, user, role):
        if not self.has_user(user):
            self.user_groups.append(Attend(user=user, user_role=role))
        else:
            raise ValueError('user %s already exists' % user)

    def remove_user(self, user):
        if self.has_user(user):
            self.registered_users.remove(user)
        else:
            raise ValueError('user %s does not exist' % user)

    def add_tag(self, tag):
        if not self.has_tag(tag):
            self.tags.append(tag)
        else:
            raise ValueError('tag %s already exists' % tag)

    def remove_tag(self, tag):
        if self.has_tag(tag):
            self.tags.remove(tag)
        else:
            raise ValueError('tag %s does not exist' % tag)

    def has_user(self, user):
        return (user in self.registered_users)

    def has_tag(self, tag):
        return (tag in self.tags)

    def __json__(self):
        return ['gid', 'oid', 'start_time', 'end_time', 'location', 'description']

    def __eq__(self, other):
        return (self.gid == other.gid)

    def __repr__(self):
        return "<Group(gid=%s, oid=%s, start_time=%s, end_time=%s, location=%s)>" \
            % (self.gid, self.oid, self.start_time, self.end_time, self.location)

class Tag(db.Model):
    __tablename__ = 'tag'

    tag = db.Column(db.String, primary_key=True, unique=True, nullable=False)
    gid = db.Column(db.Integer, db.ForeignKey('group.gid'))
    uid = db.Column(db.Integer, db.ForeignKey('user.uid'))

    #many to one db.relationship with group
    group = db.relationship('Group', back_populates='tags')
    user = db.relationship('User', back_populates='tags')

    def __json__(self):
        return ['gid', 'tag']

    def __eq__(self, other):
        return (self.gid == other.gid and self.tag == other.tag)

    def __repr__(self):
        return "<Tag(gid=%s, tag=%s)>" % (self.gid, self.tag)
