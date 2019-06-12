import os
# import retro
import gym

RECORD_REPLY = bool(os.getenv('RECORD_REPLY', False))
EPISODES = int(os.getenv('EPISODES', 10))
STEPS_PER_EPISODE = int(os.getenv('STEPS_PER_EPISODE', 100))
# GAME = int(os.getenv('GAME', 'StreetFighterIISpecialChampionEdition-Genesis'))
GAME = os.getenv('GAME', 'BreakoutDeterministic-v4')

AGENT_MODULE = os.getenv('AGENT_MODULE', 'algorithms._new_template.agent')
AGENT_CLASS = os.getenv('AGENT_CLASS', 'Agent')

def agent_class(module, class_name):
    sf_agent_mod = __import__(module, fromlist=["*"])
    sf_agent_class = getattr(sf_agent_mod, class_name)
    return sf_agent_class

# env = retro.make(game=GAME)
env = gym.make(GAME)

if RECORD_REPLY is True:
    env.auto_record(path='./reply/')

if __name__ == "__main__":

    sf_agent = agent_class(AGENT_MODULE, AGENT_CLASS)(env.action_space)

    for episode in range(EPISODES):
        game_finished = False
        env.reset()
        # Get initial observation (first state)
        _obs = env.render(mode='rgb_array')
        sf_agent.start_episode(episode)

        step = 0
        while not game_finished:
            sf_agent.start_step(step)

            action = sf_agent.get_action(_obs)

            _next_obs, _rew, _done, _info = env.step(action)

            sf_agent.add_experience(_obs, _rew, action, _next_obs, info=_info)

            _obs = _next_obs
            game_finished = _done or step > STEPS_PER_EPISODE

            sf_agent.end_step(step)
            step = step +1

        sf_agent.end_episode(episode)