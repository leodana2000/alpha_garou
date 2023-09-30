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

rules = "" #Common batch of rules

game = rules #will contain all of the preprompts and thoughts
prompts = [rules, rules, rules, rules, rules]

random_WW = np.copy(players['ids'])
np.random.shuffle(random_WW) #choose the two werewolfs (the first two ids)

villager = "" #Role of villager
for id in random_WW[2:]:
    name = players['names'][id]
    identity = "XXX {} XXX".format(name) #give the name and detail of the caracter (can be modified to included personas)
    prompts[id] += identity + villager
    game += identity + villager

WW1 = "XXX {} XXX".format(players['names'][random_WW[1]]) #Role of first WW, and knowledge of the second
identity = "XXX {} XXX".format(players['names'][random_WW[0]]) 
prompts[random_WW[0]] += identity + WW1
game += identity + WW1

WW2 = "XXX {} XXX".format(players['names'][random_WW[0]]) #Role of second WW, and knowledge of the first
identity = "XXX {} XXX".format(players['names'][random_WW[1]]) 
prompts[random_WW[0]] += identity + WW1
game += identity + WW2

#Create narrator


#Begin debate


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

end_of_debate = "" #prompt ending the debate, now each player votes
votes_names = []
for id in players['ids']:
    next_speaker = "XXX {} XXX".format(players['names'][id])
    answer, _ = utils.api_call(end_of_debate + next_speaker)

    votes_names.append(utils.extract_vote(answer))
votes_ids = [players['names'].index(name) for name in votes_names]

print(votes_ids, random_WW[:2])

#Save the game