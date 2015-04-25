import random


'''
mafia = 0
detective = 1
doctor = 2
civilian = 3
'''

def select_role(room):
    int count = 0
    list users
    for user in room:'''select userID from user where user.room = room'''
        count++
        users.push_back(user)'''store all user ID inside a container'''
    if (count<4):
        return
    else if (count>=4 and count<8):
        for n in range(0,count):
            index = random(0,count-n)
            if (n>3):
                users[index].role = 3
            else:
                users[index].role = n
            users.remove(index)'''once done with role assignment, pop out from the list of user ID'''
    else if (count>=8 and count<16):'''2 mafia, 1 detective, 2 doctor'''
        for n in range(0,count):
            index = random(0,count-n)
            if (n<2):'''assign 2 mafia'''
                users[index].role = 0
            else if (n>=2 and n<4):'''assign 2 doctors'''
                users[index].role = 2
            else if (n == 4):'''assign 1 detective'''
                users[index].role = 1
            else:'''assign civilian to all other users'''
                users[index] = 3
            users.remove(index)

def eachturnend(room):
    mafia_count = 0
    civilian_count = 0
    for user in room:'''select userID from user where user.room = room'''
        if (user.recently_killed == 1 and user.recently_healed == 0):
            user.alive = 0
        else if (user.recently_healed == 1):
            user.recently_healed = 0
        if (user.role == 0):
            mafia_count++
        else:
            civilian_count++
    room.voting.clear()
    if (mafia_count == 0):
        return 1
    else if (civilian_count == 0):
        return 2
    else:
        return 0

def kill(room,userID):
    '''select userID from user where user.room = room and user.userID = userID and user.alvie = 1'''
    userID.recently_killed = 1
    
def heal(room,userID):
    '''select userID from user where user.room = room and user.userID = userID and user.alive = 1'''
    userID.recently_healed = 1

def check(room,userID):
    '''select userID from user where user.room = room and user.userID = userID and user.alvie = 1'''
    return userID.role

def vote(room,userID):
    '''select userID from user where user.room = room and user.userID = userID and user.alvie = 1'''
    '''select room from room where room.ID  = room'''
    room.voting.push_back(userID)

def exectuing(room):
    result = maxreapting(room.voting)
    result.alive = 0
