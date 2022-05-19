class UserBlacklisted(Exception):
    def __init__(self, message="User is blacklisted!"):
        self.message = message
        super().__init__(self.message)

class ChannelBlacklisted(Exception):
    def __init__(self, message="Channel is Blacklisted!"):
        self.message = message
        super().__init__(self.message)
        
class UserNotOwner(Exception):
    def __init__(self, message="User is not the server owner!"):
        self.message = message
        super().__init__(self.message)

#class (Exception):
 #   def __init__(self, message="User is not the server owner!"):
  #      self.message = message
   #     super().__init__(self.message)
       