## The scigym library

SciGym exists as a library on [github](https://github.com/hendrikpn/scigym)! With this library we made an attempt to collect and curate standardized RL environments for science. We encourage you to add your science environment to this library. Of course, you don't have to do this. We are also happy to host your personal environment on scigym.ai. In either case, we recommend to standardize your environment according to the OpenAI gym [policy](https://github.com/HendrikPN/scigym/blob/master/CONTRIBUTING.md#how-to-standardize-your-environment) for RL environments.

## Standardized Environments

In short, any standard RL environment needs to be a python class inheriting from the OpenAI [`gym.Env`](https://github.com/openai/gym/blob/master/gym/core.py) class. This class includes three major methods which should be present in all environments:

1. `reset(self)`: This method *resets* the environment to an initial state. It returns an `observation` which contains the necessary information about the current state of the environment.
2. `step(self, action)`: This method describes one *step* in the interaction between agent and environment. It returns a tuple containing an `observation`, the current `reward` and a binary value `done` which signals whether or not the environment is *done*.
3. `render(self, mode='human', close='False')`: This methods renders one frame of the environment. The default `mode` will do something human friendly, such as pop up a window. Passing the `close` flag signals the renderer to close any such windows. While OpenAI flags this method as required, we don't actually necessitate you to provide it.

For a more detailed description on how to create your own `gym` environment look [here](https://github.com/HendrikPN/scigym/blob/master/CONTRIBUTING.md#how-to-standardize-your-environment). A simple template which is in accordance with this policy can be found [here](https://github.com/HendrikPN/gym-template).

## Add your environment to SciGym.ai

This is rather simple. In principle, you don't even have to be in accordance with the OpenAI gym policy for standardized environments. Nevertheless, we still recommend it since we would need to flag your environment as `unverified` otherwise. This flag would be displayed visibly at your environment. 

To upload your environment just follow the next few steps after standardizing your environment:

* Log in with your github account and refresh your repositories. We will do a brief scan for the main features of a standardized environment and sort your public repositories accordingly. 
* Choose the environment you wish to upload to SciGym.ai. 
* Click `+`.
* Edit the information that will be displayed on our webpage as you desire. By default, your repository's `README` will also be displayed.
* Submit your environment.
* We will be informed about your submission and check whether the repository is valid.
* Once we have accepted the submission, it will appear under `Recent Environments` for everyone to see!

## Add your environment to the scigym library

To add your repository to our scigym package, just follow the steps in the [`CONTRIBUTING.md`](https://github.com/HendrikPN/scigym/blob/master/CONTRIBUTING.md#how-to-add-an-environment-to-scigym) file in our repository.

