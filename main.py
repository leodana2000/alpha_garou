#import useful lib
import utils
import numpy as np
import random


#Initialisation


players = {
    'names' : ['Paul', 'Sarah', 'John', 'Emma', 'Chris'],
    'ids' : [0, 1, 2, 3, 4],
    'AIs' : ['gpt4', 'gpt4','gpt4','gpt4','gpt4'],
}

rules = '''
You are playing a game of Wolvesville. 
The game feature 5 players, two of which are werewolves. 
At the end of the day, the village will vote for a player. 
If the player is a werewolf, the villager wins. Otherwise, the werewolves win.
Note that the werewolves know each other and can cooperate to win.

Each turn, the narator will decide who talks. 
Each person has to first think about what to say in brackets, and then to say it for real to the players. 
Example: [I should try to win the game.] Hi guys, I'm not a werewolf.
Each players will not have access to the others' thoughts.
'''#Common batch of rules

game = rules #will contain all of the preprompts and thoughts
prompts = [rules, rules, rules, rules, rules]

random_WW = np.copy(players['ids'])
np.random.shuffle(random_WW) #choose the two werewolfs (the first two ids)

villager = '''
You are a villager. Your role is to unit with th other 2 villagers to vote for a werewolf.
You don't know who the other two villagers are.
''' #Role of villager

for id in random_WW[2:]:
    name = players['names'][id]
    identity = "Your name is {}. Please, talk only when it is you turn.".format(name) #give the name and detail of the caracter (can be modified to included personas)
    prompts[id] += identity + villager
    game += identity + villager

WW1 = ''''
You are a werewolf. Your role is to unit with the other werewolf and convince villager to vote for a villager. 
The other werewolf is {}.
'''.format(players['names'][random_WW[1]]) #Role of first WW, and knowledge of the second
identity = "Your name is {}. Please, talk only when it is you turn.".format(players['names'][random_WW[0]]) 
prompts[random_WW[0]] += identity + WW1
game += identity + WW1

WW2 = ''''
You are a werewolf. Your role is to unit with the other werewolf and convince villager to vote for a villager. 
The other werewolf is {}.
'''.format(players['names'][random_WW[0]]) #Role of second WW, and knowledge of the first
identity = "Your name is {}. Please, talk only when it is you turn.".format(players['names'][random_WW[1]]) 
prompts[random_WW[0]] += identity + WW1
game += identity + WW2

#Create narrator


#Begin debate

begin = "THE GAME BEGINS"
game += begin
for prompt in prompts:
    prompt += begin

N_rounds = 20 #Number of debating rounds, a round is just one caracter speaking
for r in range(N_rounds):
    next_id = 0 #decide how should talk next in the debate

    next_speaker = "The next speaker is {}.".format(players['names'][next_id]) #introducing the next speaker
    answer, answer_thoughts = utils.api_call(prompts[next_id] + next_speaker, players['AIs'][next_id]) #api_call should return text, and text + thoughts

    for id in players['ids']:
        if id == next_id:
            prompts[next_id] += next_speaker + answer_thoughts
            game += next_speaker + answer_thoughts
        else:
            prompts[next_id] += next_speaker + answer

end_of_debate = '''
THE GAME ENDS
Please now vote to eliminate a player.
Remember that the goal of the villager is to vote for a werewolf, and those of the werewolf is to vote for a villager.
''' #prompt ending the debate, now each player votes

votes_names = []
for id in players['ids']:
    next_speaker = '''
    It is time for {} to vote. Please express your vote by saying only the name of the players you wish to eliminate.
    '''.format(players['names'][id])
    answer, _ = utils.api_call(end_of_debate + next_speaker)

    votes_names.append(utils.extract_vote(answer))
votes_ids = [players['names'].index(name) for name in votes_names]

print(votes_ids, random_WW[:2], game)

#Save the game