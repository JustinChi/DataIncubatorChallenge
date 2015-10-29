#!/usr/bin/python

####################################################################################################
# Q1: There is a lost tourist in Grandeville. The streets in Grandeville run east to west and go   #
# from:                                                                                            #
#      ..., S. 2nd St., S. 1st St., Broadway St., N. 1st St., N. 2nd St., ...                      #
# The avenues run north to south and go from:                                                      #
#      ..., E. 2nd Ave., E. 1st Ave., Broadway Ave., W. 1st Ave., W. 2nd Ave., ...                 #
# These streets form a square block grid. For each of the questions below, the tourist starts at   #
# the intersection of Broadway St. and Broadway Avenue and moves one block in each of the four     #
# cardinal directions with equal probability.                                                      #
####################################################################################################

# Header, import statements etc.
import time
import numpy as np
import matplotlib.pyplot as plt

def CalcDistanceThreshProb(ntrials, startx, starty, nmoves, distthresh_fin, distthresh_ins):
  nMoves, nDirections = nmoves, 4 #Number of moves we're going to make and the number of directions we can travel.
  xMove = [1, 0, -1,  0] # We're going to randomly pick a number between 0 and 3, and then choose a direction
  yMove = [0, 1,  0, -1] # in x and y corresponding to that number.
  nPassedThreshold_Final = 0
  nPassedThreshold_Inst  = 0
  # Generate the walking path for this simulation.
  WalkingPath = np.random.randint(low=0, high=nDirections, size=(ntrials, nMoves))
  for iTrial in range(ntrials):
    # Reset the current position and the instantaneous threshold pass flag.
    currentX, currentY = startx, starty
    PassedInstFlag = False
    # Step through the walking path, and figure out where we end up...
    for step in WalkingPath[iTrial]:
      currentX += xMove[step]
      currentY += yMove[step]
      currentDistance = np.sqrt(((currentX - startx)**2) + ((currentY - starty)**2))
      if(currentDistance > distthresh_ins): PassedInstFlag = True
    # Calculate how far we got, and increment the coutner if we got farther than the threshold.
    DistanceTraveled = np.sqrt(float( ((currentX - startx)**2) + ((currentY - starty)**2)) )
    if(DistanceTraveled > distthresh_fin): nPassedThreshold_Final += 1
    if(PassedInstFlag): nPassedThreshold_Inst += 1
  # Calculate the fraction passing the thresholds and pass it back to the main code.
  FractionPassed_Final = float(nPassedThreshold_Final) / float(ntrials)
  FractionPassed_Inst = float(nPassedThreshold_Inst) / float(nTrials)
  return nPassedThreshold_Final, FractionPassed_Final, nPassedThreshold_Inst, FractionPassed_Inst

def CalcBackTrackingProb(ntrials, startx, starty, nmoves, eastthresh, westthresh):
  nMoves, nDirections = nmoves, 4 #Number of moves we're going to make and the number of directions we can travel.
  xMove = [1, 0, -1,  0] # We're going to randomly pick a number between 0 and 3, and then choose a direction
  yMove = [0, 1,  0, -1] # in x and y corresponding to that number.
  nPassed = 0
  # Generate the walking path for this simulation.
  WalkingPath = np.random.randint(low=0, high=nDirections, size=(ntrials, nMoves))
  for iTrial in range(ntrials):
    # Reset the current position and the instantaneous threshold pass flag.
    currentX, currentY = startx, starty
    PassedEastThresh = False
    # Step through the walking path, and figure out where we end up...
    for step in WalkingPath[iTrial]:
      currentX += xMove[step]
      currentY += yMove[step]
      # Check if at any point on our path, we cross the east threshold...
      if(currentX > eastthresh): PassedEastThresh = True
    # See if the east threshold was passed and if our final localtion passes the west threshold.
    if(PassedEastThresh and (currentX < westthresh)): 
      nPassed += 1
  # Calculate the fraction passing the thresholds and pass it back to the main code.
  FractionPassed = float(nPassed) / float(ntrials)
  return nPassed, FractionPassed

def CalcNmovesForDist(ntrials, startx, starty, distthresh):
  nDirections = 4 # Number of directions we can travel.
  xMove = [1, 0, -1,  0] # We're going to randomly pick a number between 0 and 3, and then choose a direction
  yMove = [0, 1,  0, -1] # in x and y corresponding to that number.
  nMovesToHitDistThresh = 0 #Track the total number of moves to hit the threshold across all the trials
  for iTrial in range(ntrials):
    # Reset the current position for this trial.
    currentX, currentY = startx, starty
    # Step through the walking path, and figure out where we end up...
    iStep = 0
    currentDistance = 0.
    while(currentDistance < distthresh):
      iStep += 1
      step = np.random.randint(low=0, high=nDirections, size=1)
      currentX += xMove[step]
      currentY += yMove[step]
      currentDistance = np.sqrt(((currentX - startx)**2) + ((currentY - starty)**2))
    nMovesToHitDistThresh += iStep
  # Normalize the running tally of the number of moves by the number of trials, then return the value.
  AvgNumMoves = float(nMovesToHitDistThresh) / float(ntrials)
  return AvgNumMoves


####################################
#  BEGIN MAIN BODY OF THE CODE!!!  #
####################################

# Get the start time of this calculation
StartTime = time.time()

# First part of the question:
print "\nWhat is the probability that the tourist is at least 3 city blocks (as the crow flies) from"
print "Broadway and Broadway after 10 moves?"
xStart, yStart = 0, 0
nTrials = int(1.e5)
nMoves = 10
DistanceThreshold_Final = 3.
PassFraction_Inst = 5.
nPassed_Final, PassFraction_Final, nPassed_Inst, PassFraction_Inst = CalcDistanceThreshProb(nTrials, xStart, yStart, nMoves, DistanceThreshold_Final, PassFraction_Inst)
print "\t", nPassed_Final, "out of", nTrials, "(" + "{:0.10f}".format(PassFraction_Final) + ")."

# Third part of the question:
print "\nWhat is the probability that the tourist is ever at least 5 city blocks (as the crow flies)"
print "from Broadway and Broadway within 10 moves?"
print "\t", nPassed_Inst, "out of", nTrials, "(" + "{:0.10f}".format(PassFraction_Inst) + ")."

# Second part of the question:
print "\nWhat is the probability that the tourist is at least 10 city blocks (as the crow flies) from"
print "Broadway and Broadway after 60 moves?"
nMoves = 60
DistanceThreshold_Final = 10.
PassFraction_Inst = 10.
nPassed_Final, PassFraction_Final, nPassed_Inst, PassFraction_Inst = CalcDistanceThreshProb(nTrials, xStart, yStart, nMoves, DistanceThreshold_Final, PassFraction_Inst)
print "\t", nPassed_Final, "out of", nTrials, "(" + "{:0.10f}".format(PassFraction_Final) + ")."

# Fourth part of the quetion:
print "\nWhat is the probability that the tourist is ever at least 10 city blocks (as the crow flies)"
print "from Broadway and Broadway within 60 moves?"
print "\t", nPassed_Inst, "out of", nTrials, "(" + "{:0.10f}".format(PassFraction_Inst) + ")."

# Fifth part of the question:
print "\nWhat is the probability that the tourist is ever east of East 1st Avenue but ends up west"
print "of West 1st Avenue in 10 moves?"
EastThreshold =  1
WestThreshold = -1
nMoves = 10
nPassed, PassFraction = CalcBackTrackingProb(nTrials, xStart, yStart, nMoves, EastThreshold, WestThreshold)
print "\t", nPassed, "out of", nTrials, "(" + "{:0.10f}".format(PassFraction) + ")."

# Sixth part of the question:
print "\nWhat is the probability that the tourist is ever east of East 1st Avenue but ends up west"
print "of West 1st Avenue in 30 moves?"
nMoves = 30
nPassed, PassFraction = CalcBackTrackingProb(nTrials, xStart, yStart, nMoves, EastThreshold, WestThreshold)
print "\t", nPassed, "out of", nTrials, "(" + "{:0.10f}".format(PassFraction) + ")."

# Seventh part of the question:
nTrials = int(1.e3)
print "\nWhat is the average number of moves until the first time the tourist is at least 10 city"
print "blocks (as the crow flies) from Broadway and Broadway."
DistanceThreshold = 10
AvgMoves = CalcNmovesForDist(nTrials, xStart, yStart, DistanceThreshold)
print "\tThe tourist needed to walk an average of", "{:0.10f}".format(AvgMoves), "moves to get", DistanceThreshold, "blocks."

# Eighth and final part of the question:
print "\nWhat is the average number of moves until the first time the tourist is at least 60 city"
print "blocks (as the crow flies) from Broadway and Broadway."
DistanceThreshold = 60
AvgMoves = CalcNmovesForDist(nTrials, xStart, yStart, DistanceThreshold)
print "\tThe tourist needed to walk an average of", "{:0.10f}".format(AvgMoves), "moves to get", DistanceThreshold, "blocks."

# Get the end time and report how long this calculation took
StopTime = time.time()
print "It took", StopTime - StartTime, "seconds for this code to run."
exit()

