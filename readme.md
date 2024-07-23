# Project Setup Guide

This project uses GitHub Actions to fetch data from another repository and notify via Telegram about power outages. Here's how you can fork this project and set it up for your own use:

## Forking the Repository

1. Click on the 'Fork' button at the top right of this repository. This will create a copy of this repository in your GitHub account.

## Setting Up the Project

1. Clone the forked repository to your local machine.

```bash
git clone https://github.com/<your-github-username>/<repository-name>.git
```

2. Navigate to the cloned repository.

```bash
cd <repository-name>
```

3. Install the required Python packages.

```bash
pip install -r requirements.txt
```

## Configuring GitHub Actions

This project uses two GitHub Actions workflows:

1. `fetch_file.yml`: This workflow fetches a file from another repository and commits it to the `fetched_files` directory in this repository.
2. `notify.yml`: This workflow runs the `notify.py` script which sends a notification about power outages via Telegram.

To configure these workflows, you need to set up the following secrets in your GitHub repository:

- `GITHUB_TOKEN`: This is a token that GitHub provides to authenticate your GitHub Actions workflows. You don't need to manually set this secret; GitHub automatically creates it for you.
- `BOT_TOKEN`: This is the token of your Telegram bot. You can get this token by creating a new bot on Telegram.
- `CHAT_ID`: This is the ID of the Telegram chat where you want to send the notifications. You can get this ID by sending a message to your Telegram bot and then using the Telegram API to get the update.

To set these secrets:

1. Go to the main page of your GitHub repository.
2. Click on 'Settings'.
3. Click on 'Secrets and variables'.
4. Click on the 'Secrets' tab.
5. Click on 'New repository secret'.
6. Enter the name of the secret and its value, then click on 'Add secret'.

Next is to configure GitHub variables in your repository to monitor for a specific district and locality

- `LOCALITY`: The area/region/ for which you want to monitor for power cuts.
- `DISTRICT`: The district in which your locality is located. A list of district values can be found below:

```json
{
  "DISTRICT": [
    "blackriver",
    "flacq",
    "grandport",
    "moka",
    "pamplemousses",
    "plainewilhems",
    "portlouis",
    "rivieredurempart",
    "savanne",
    "rodrigues"
  ]
}
```

To set the `DISTRICT` and `LOCALITY` variables:

1. Go to the main page of your GitHub repository.
2. Click on 'Settings'.
3. Click on 'Secrets and variables'.
4. Click on the 'Variables' tab.
5. Click on 'New repository variable'.
6. Enter the name of the variable and its value, then click on 'Add variable'.

## Running the Project

Once you've set up the secrets, the GitHub Actions workflows will automatically run according to their triggers. The `fetch_file.yml` workflow runs every hour from 6 through 18, and the `notify.yml` workflow runs whenever you push to the `main` branch.

You can also manually trigger these workflows:

1. Go to the 'Actions' tab in your GitHub repository.
2. Click on the workflow you want to run.
3. Click on 'Run workflow'.
4. Select the branch where you want to run the workflow, then click on 'Run workflow'.

That's it! You've now set up the project to fetch data and send notifications about power outages.
