#This file is for the control of errors, in the case that the any class raise an
#error, this file prints the type of the error in the terminal and continue

#Generic class for other exceptions
class Error(Exception):
   """Base class for other exceptions"""
   pass

#In the case that do not find the specified file
class NotFileFound(Error):
   """The sequence number is incorrect"""
   pass

#In the case that the sequence number is not correct
class WrongSequenceNumber(Error):
   """The sequence number is incorrect"""
   pass

#In the case that a timeout is produced
class TimeoutError(Error):
   """Timeout"""
   pass

#In the case that we recive a wrong payload
class WrongPayloadSize(Error):
   """Payload is too large"""
   pass

#In the case that we recive a mode that is not from the ones implemented
class ModeError(Error):
   """The mode is not defined correctly"""
   pass
