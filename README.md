# Comics publisher

The program can publish comics from  [xkcd.com](https://xkcd.com/) to your group on [vk.com](https://vk.com/).

## Prerequisites

Python 3.11 is required.

## Installing

- Download the project files.
- It is recommended to use [venv](https://docs.python.org/3/library/venv.html?highlight=venv#module-venv) for project isolation.
- Set up packages:

```bash
pip install -r requirements.txt
```

- Set up environmental variables in your operating system or in .env file. The variables are:
  - `ACCESS_TOKEN` - see the instruction [here](https://vk.com/dev/implicit_flow_user);
  - `GROUP_ID` is ID of your group on VK, you can get it [here](https://regvk.com/id/);

To set up variables in .env file, create it in the root directory of the project and fill it up like this:

```bash
ACCESS_TOKEN=yourtoken
GROUP_ID=123456789
```

## Using the script

- Run:

```bash
python main.py
```

- Check that a random comic was published in your group on [vk.com](https://vk.com/).

## Project goals

The project was created for educational purposes.
It's a lesson for python and web developers at [Devman](https://dvmn.org/).
