#import pytest
#from groupit import init_app
#import pdb

#@pytest.fixture(scope='module')
#def setUp(request):
    #init_app('config.DevelopConfig')
    #from groupit import db
    #db.create_all()
    ##def tearDown():
        ##db.session.remove()
        ##db.drop_all()
    ##request.addfinalizer(tearDown)
    #return db
    
#def test_createGroup(setUp):
    #from groupit.models import User, Organization, Group, Attend, Tag, \
        #GroupRoles
    #from datetime import datetime, timedelta
    
    #db = setUp
    #columbia = Organization(name="Columbia", description="At NY")
    #db.session.add(columbia)
    #db.session.commit()
    
    #eve = User(name='eve', social_id=123, oid=columbia.oid, email='eve@email.com',
        #pic_path='~/eve.jpg', description='first human')
    #eve.add_tag(Tag(tag='first female human'))
    #db.session.add(eve)
    #db.session.commit()
    
    #firstGroup = Group(oid=columbia.oid, start_time=datetime.now(),
        #end_time=datetime.now() + timedelta(hours=9), 
        #location='The garden', description='To sin')
    #db.session.add(firstGroup)
    #db.session.commit()
    
    #firstGroup.add_user(eve, GroupRoles.roles[0])
    #tag = Tag(tag='first group')
    #firstGroup.add_tag(tag)
    
    #db.session.commit()
    
    
    #assert(eve in columbia.users)
    #assert(columbia == eve.organization)
    #assert(firstGroup in columbia.groups)
    #assert(columbia == firstGroup.organization)
    
    #assert(eve in firstGroup.registered_users)
    #assert(firstGroup in eve.registered_groups)
    
    #assert(tag in firstGroup.tags)
    #assert(firstGroup == tag.group)
    
    #firstGroup.remove_user(eve)
    #db.session.commit()
    
    #assert(not eve in firstGroup.registered_users)
    #assert(not firstGroup in eve.registered_groups)
        
#def test_followUser(setUp):
    #from groupit.models import User, Organization
    
    #db = setUp
    #rhodeIsland = Organization(name="Rhode Island", description="A state")
    #db.session.add(rhodeIsland)
    #db.session.commit()
    
    #stewie = User(name='stewie', social_id=512, oid=rhodeIsland.oid, email='stewie@email.com',
        #pic_path='~/stewie.jpg', description='diabolical baby')
    #brian = User(name='brian', social_id=151, oid=rhodeIsland.oid, email='brian@email.com',
        #pic_path='~/brian.jpg', description='aspiring novelist')
    #peter = User(name='peter', social_id=153, oid=rhodeIsland.oid, email='peter@email.com',
        #pic_path='~/peter.jpg', description='the average american')
        
    #db.session.add(stewie)
    #db.session.commit()
    
    #db.session.add(brian)
    #db.session.commit()
    
    #db.session.add(peter)
    #db.session.commit()
    
    #stewie.follow(brian)
    #brian.follow(stewie)
    #db.session.commit()
    
    #assert(stewie.is_following(brian))
    #assert(brian.is_following(stewie))
    #assert(not stewie.is_following(peter))
    
    #stewie.unfollow(brian)
    #db.session.commit()
    #assert(not stewie.is_following(brian))
    #assert(brian.is_following(stewie))
    
#def test_jsonDumps(setUp):
    #import json
    #from datetime import datetime, timedelta
    #from groupit.models import User, Group, Organization
    #from groupit.json_encoder import AlchemyEncoder
    
    #db = setUp
    #heroAssociation = Organization(name="Hero Association", description="For heroes")
    #db.session.add(heroAssociation)
    #db.session.commit()
    
    #saitama = User(name='saitama', social_id=125, oid=heroAssociation.oid, email='saitama@email.com',
        #pic_path='~/saitama.jpg', description='one punch man')
    #db.session.add(saitama)
    #db.session.commit()
    
    #heroGroup = Group(oid=heroAssociation.oid, start_time=datetime.now(),
        #end_time=datetime.now() + timedelta(hours=1),
        #location='Tokyo', description='To fight monsters')
        
    #db.session.add(heroGroup)
    #db.session.commit()
    
    #print(json.dumps(saitama, cls=AlchemyEncoder))
    #print(json.dumps(heroAssociation, cls=AlchemyEncoder))
    #print(json.dumps(heroGroup, cls=AlchemyEncoder))
