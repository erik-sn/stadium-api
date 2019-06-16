## Installing the SciGym library

SciGym also exists as a library on [github](https://github.com/hendrikpn/scigym)! 
Some environments might be independent python packages, but let us start there.
Installing the `scigym` library is easy:

    pip install --user scigym

Now you have `scigym` and some of the environments you can find here, all packaged in a neat python module. 
However, before you can start tackling all the science problems we have to offer, you need to understand reinforcement learning (RL) in general, and `scigym` specifically.

## Understanding the RL paradigm

The RL paradigm is visualized in the `.gif` above and described in the following. 
There are two basic basic concepts in RL: 

1. The `agent` which is the algorithm that you are using to solve a problem in RL.
2. The `environment` which describes the problem that the `agent` is attempting to solve.

Let us ignore the `agent` here. It is up to you which RL agent you are using. 
The `environment` has been standardized through the `gym` package and we will discuss the standard methods in an example below.  
As can be seen from the `.gif` above, the environment and agent are constantly interacting with each other:

* The agent receives *perceptual* input from the environment in form of a `percept` which contains
    - the `observation`, i.e. information about the current state of the `environemnt` and
    - the `reward`, i.e. a measure of how well the agent has been performing.
* After a *deliberation* process, the agent has decided on an `action`
* The `action` is performed on the `environment`, potentially changing its internal state.
* The environment responds with a new `percept`.

This process is then repeated until the environment signals that it is `done`. The task of an agent is to maximize the expected, future reward. 
This, all taken together, describes the RL paradigm in rather general terms. Next, we give a more specific example describing how to work with the `scigym` library within this paradigm.


## Understanding SciGym environments

In an attempt to standardize RL environments in computer science, [OpenAI](https://openai.com/) established the [gym](https://github.com/openai/gym) library for comparing and developing RL algorithms.
SciGym environments inherit from the gym package their most important features. 
Here, we present a typical round of interactions between a random agent and an environment which you can savely do at home.

1. Start by creating a python file `interaction.py`. 
2. In the header we just need to import scigym and numpy:

    ```python
    import scigym
    import numpy as np
    ```
This already provides us will all the necessary features of `gym`. 

3. Now let us select an environment from scigym which we want to explore. How about, `scigym-surfacecode`?
You don't know how it works, or what it is? Well, this is a rather nice feature of RL: you don't need to! Instead, consider the environment as a black box that responses to your actions in some way.  
So, let's get this environment:

    ```python
    env = scigym.make('scigym-surfacecode-v0')
    ```
`env` now contains all the information of the environment. It is basically all set up.

4. However, we still need to understand what we can do, even in principle. Sure, we can do actions, but how many are there?  
Let's find out:

    ```python
    if isinstance(env.action_space,scigym.Discrete):
        num_actions = env.action_space.n
    else:
        raise ValueError
    ```
In the first line we check whether our action space is discrete. If it is, we are satisfied and just count the number of actions available. Otherwise, we raise a value error.

5. Surprisingly, now we know exactly what actions we can do, without even knowing what they do! That is, in the scigym environments actions are just indices:

    ```python
    actions = range(num_actions)
    ```

6. We are now all set to play with the environment. So let's start this environment using the standard `reset` method:

    ```python
    observation = env.reset()
    ```
This method returns an `observation` which is a numpy array which encodes the available information about the environment's current state.

7. Given this observation, we need to make a decision, i.e. `action`. Since this is just a random agent, we make a random decision:

    ```python
    action = np.random.choice(actions)
    ```

8. Now we act with this action on the environment through the standard `step` method.  
In fact, we should repeatedly apply an action until the environment is `done`:

    ```python
    done = False
    while not done:
        (observation, reward, done) = env.step(action)
        action = np.random.choice(actions)
    ```
At each step the environment provides us with a `percept`, i.e. a tuple which contains *at least* the current `observation`, `reward` and whether or not the environment is `done`.  
Of course, if this had not been a random agent, we would have wanted it to *learn* to respond to each percept such that the expected future `reward` is maximized.


**Note:**
There is one standard method of `env` which we neglected: `env.render(mode='human', close='False')` provides a method which renders one frame of the environment. The default `mode` will do something human friendly such as a popup window. Passing the `close` flag signals the renderer to close any such window.