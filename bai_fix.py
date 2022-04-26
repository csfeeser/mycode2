import sys
import os
import random
import time

delay = 0

def showInstructions():
  print('''
RPG Adventure Game
==================
Instruction: You are in the center from the beginning.
You can move north/south/west/east to find a way to escape.
hint: Water kills fire.
      fire kills zombie.
      sword kills zobbie and warrior.
      A good potion will never be green.
Commands:
  go [direction]
  get [item]
  use [item]
  teleport
  help
''')

def showStatus():
  print('---------------------------')
  print('You are in the ' + currentRoom)
  time.sleep(delay)
  print('Inventory : ' + str(inventory))
  if "item" in rooms[currentRoom]:
    print(f"You see {rooms[currentRoom]['item']}")
  print("---------------------------")
  if "teleport" in rooms[currentRoom]: 
    print("\nA teleport station has been found!")
    
inventory = []

rooms = {
            'center' : {
                  'north' : 'north',
                  'south' : 'south',
                  'east' : 'east',
                  'west' : 'west',
                  'item' : ['water', 'knife'],
                  'desc' : 'You are in the center which is the starting point.' 
                },
            'north' : {
                  'south' : 'center',
                  'item' : ['fire', 'water', 'knife'],
                  'desc' : 'You are in the north'
                },
            'south' : {
                  'north' : 'center',
                  'east' : 'field',
                  'teleport' : 'east',
                  'item' : ['red potion', 'green potion', 'knife'],
                  'desc' : 'You are in the south.'
               },
            'west' : {
                  'east' : 'center',
                  'item' : ['knife', 'sword', ],
                  'teleport' : 'basement',
                  'desc' : 'You are in the west.'
                }, 
            'east' : {
                  'west' : 'center',
                  'east' : 'field',
                  'teleport' : 'basement',
                  'target' : 'warrior',
                  'desc' : 'You are in the east. A warrior appears in front of you.\nHe\'s trying to stop you from passing.'
                },
            'field' : {
                  'west' : 'east',
                  'target' : 'zombie',
                  # typo, missing the 'desc' key
                  'desc': 'You are on the field now. A zombie is running to you and trying to bite you!'
            }
         }
         
currentRoom = 'center'

showInstructions()

while True:
  showStatus()
  
  move = ''
  while move == '':
    move = input('Please type your command\n>')
  move = move.lower().split(" ", 1)
  
  os.system('clear') 
  
  if move[0] == 'go':
    # CHAD CHANGE: moved code for specific rooms to later in the code, keep code cleanly modularized
    # CHAD CHANGE: redundant to use move[1].lower(), already did that on line 90
      if move[1] in rooms[currentRoom]:
          currentRoom = rooms[currentRoom][move[1]]
      if 'desc' in rooms[currentRoom]:
          print(rooms[currentRoom]['desc'])
      else:
          print('You can\'t go that way!')        
   
  if move[0] == 'get' :
  # CHAD NOTE: I really like what you added to the "get" section, really clever!!! 
  
    if move[1] in inventory:
      print(f"You already have a {move[1]}!")
      
    elif 'item' in rooms[currentRoom] and move[1] in rooms[currentRoom]['item']:
      inventory += [move[1]]
      print(move[1] + ' got!')
      rooms[currentRoom]['item'].remove(move[1])
      
    else:
      print('Can\'t get ' + move[1] + '!')
      
  if move[0] == 'use' :
  # CHAD NOTE: a lot of this code was redundant (already covered elsewhere in the script) so I removed it.
  
        if move[1] == 'teleport':
            currentRoom = 'basement'

        elif move[1] == 'green potion':
            print('Your are tallow-faced, pressing your neck with both hands, and fell so suffocated.\nYou are dead...GAME OVER!')
            break
            
        elif move[1] == 'red potion':
            print('You suddenly feel energized...\nCongratulation! You have gained the power of mind control!')
                
        else:
            print(f"{move[1]} is not in your inventory!")
     
  if currentRoom == 'basement':
        if 'knife' in inventory:
          print("You are in the basement but the door is locked.\nBut it looks like you are able to unlock the door.")
          currentRoom == 'center'
        else:
          print('15 days later, a dead body was found in a basement...GAME OVER!')
          break
               
  if 'fire' in inventory and 'water' in inventory:
        print('The fire has disappeared.')
        inventory.remove('fire')
          
    
  if 'target' in rooms[currentRoom] and 'warrior' in rooms[currentRoom]['target']:
      action1= input('The warrior apprears. Are you taking actions? (yes or no)\n>').lower()
      if action1 == 'yes':
          action2= input('what are you going to do? (use an item)').lower()
          if action2.lower() == 'use sword':
        # CHAD NOTE: to use move[0] you'd need to use .lower.split... I simplified it to just "use sword"
               win_chance= random.randint(2,2)
                          # typo in randint
               if win_chance == 1:
                   print('You are killed by the warrior! GAME OVER!')
                   break
               else:
                 currentRoom= 'field'
                 print('You have defeated the warrior and escaped to the field!')
      elif action1 == 'no':
      # CHAD NOTE: that previously was elif action2, I changed it to action1    
          currentRoom= 'center'
          print('The warrior kicked you back to the center room!')
      else:
         print('Because you could not answer a simple yes or no question, the warrior killed you. GAME OVER!')
         break

  # CHAD NOTE: all this zombie logic MUST follow the warrior logic
  if 'target' in rooms[currentRoom] and 'zombie' in rooms[currentRoom]['target']:
      if 'fire' in inventory:
          print("There is a zombie here! You toss fire in its face and watch the ghoul burn!")
          del rooms[currentRoom]['target']
      elif "sword" in inventory:
          print("There is a zombie here! You lop off its head with your sword!")
          del rooms[currentRoom]['target']
      else:
          print('You are eaten by zombie! GAME OVER!')
          break
    
  if currentRoom == 'field' and 'target' not in rooms[currentRoom]:
    print('Congrats! You have successfully escaped. YOU WIN!')
    break

  # this contradicts the code above, so I commented it out     
  #elif 'target' in rooms[currentRoom] and 'zombie' in rooms[currentRoom]['target']:
    #action3= input('D')
    #print('The zombie has bited you... GAME OVER!')
    #break
    
  elif move[0] == 'help':
    showInstructions()
  
                       # typo fixed
  elif move[0] in ['q', 'quit']:
      print("Are you sure you want to quit? Yes/No")
      quit_query = input('>')
      if quit_query.lower() in ['y', 'yes']:
          print("Thanks for playing!")
          sys.exit()
      else:
          pass
