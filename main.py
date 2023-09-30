#import useful lib
import utils
import numpy as np
import random
import asyncio

players = {
    'names' : ['Paul', 'Sarah', 'John', 'Emma', 'Chris'],
    'ids' : [0, 1, 2, 3, 4],
    'AIs' : ['gpt-4', 'gpt-4','gpt-4','gpt-4','gpt-4'],
}

rules = '''
    You are playing a game of Wolvesville. 
    The game feature 5 players, two of which are werewolves.
    The players are Paul, Sarah, John, Emma and Chris. 
    At the end of the day, the village will vote to eliminate a player. 
    If the player is a werewolf, the villagers wins. Otherwise, the werewolves win.
    The werewolves know each other and can cooperate to win.

    Each turn, the narrator will decide who talks.
'''#Common batch of rules

async def main() :

    game = rules #will contain all of the preprompts and thoughts
    prompts = [rules, rules, rules, rules, rules]

    random_WW = np.copy(players['ids'])
    np.random.shuffle(random_WW) #choose the two werewolfs (the first two ids)

    villager = '''
        You are a villager. Your role is to eliminate a werewolf.
        You don't know who the other two villagers are.
    ''' #Role of villager

    for id in random_WW[2:]:
        name = players['names'][id]
        identity = "Your name is {}. Please, talk only when it is you turn.".format(name) #give the name and detail of the caracter (can be modified to included personas)
        prompts[id] += identity + villager
        game += identity + villager

    identity = "Your name is {}. Please, talk only when it is you turn.".format(players['names'][random_WW[0]]) 
    WW1 = ''''
        You are a werewolf. Your role is to eliminate a villager. 
        The other werewolf is {}.
    '''.format(players['names'][random_WW[1]]) #Role of first WW, and knowledge of the second
    prompts[random_WW[0]] += identity + WW1
    game += identity + WW1

    identity = "Your name is {}. Please, talk only when it is you turn.".format(players['names'][random_WW[1]]) 
    WW2 = ''''
        You are a werewolf. Your role is to eliminate a villager.
        The other werewolf is {}.
    '''.format(players['names'][random_WW[1]]) #Role of second WW, and knowledge of the first
    prompts[random_WW[0]] += identity + WW2
    game += identity + WW2

    #Create narrator


    #Begin debate

    begin = '''
    \n THE GAME BEGINS\n\n
    '''

    instructions = '''
    The format of your answer should be the following :
    "your answer"
    Thoughts: [your thought process]
    '''

    for prompt in prompts:
        prompt += begin
    game += begin


    N_rounds = 3 #Number of debating rounds, a round is just one caracter speaking
    for r in range(N_rounds):
        next_id = r % 5 #decide how should talk next in the debate

        next_speaker = "{}:".format(players['names'][next_id]) #introducing the next speaker

        answer, answer_thoughts = await utils.api_call(prompts[next_id] + instructions + next_speaker, players['AIs'][next_id]) #api_call should return text, and text + thoughts
        
        for id in players['ids']:
            if id == next_id:
                prompts[id] += next_speaker + answer_thoughts + "\n"
            else:
                prompts[id] += next_speaker + answer + "\n"
        game += next_speaker + answer_thoughts + "\n\n"

        print(prompts[0])


    end_of_debate = '''
        \n THE GAME ENDS
        Please now vote to eliminate a player.
        Remember that the goal of the villager is to vote for a werewolf, and those of the werewolf is to vote for a villager.\n
    ''' #prompt ending the debate, now each player votes

    for prompt in prompts:
        prompt += end_of_debate
    game += end_of_debate


    votes_names = []
    for id in players['ids']:
        next_speaker = '''
        It is time for {} to vote.
        ''' + instructions + '''
        Please express your vote by saying only the name of the players you wish to eliminate. 
        You can only choose between Paul, Sarah, John, Emma and Chris.
        {}:
        '''.format(players['names'][id], players['names'][id])
        answer, answer_thought = await utils.api_call(end_of_debate + next_speaker, players['AIs'][id])
        game += next_speaker + answer_thought

        votes_names.append(utils.extract_vote(answer, players['names']))

    votes_ids = [players['names'].index(name) for name in votes_names]

    print(game)

    #Save the game

if __name__ == '__main__':
    asyncio.run(main())