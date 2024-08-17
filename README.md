# CTFd First Blood & Solve Discord Announcer

A Dockerized bot that uses Discord channel webhooks to announce CTFd first bloods & solves.

## How to use

1. Clone the repo:
   ```bash
   git clone https://github.com/ArcusTen/CTFd-Discord-First-Blood.git
   ```

2. Create a [Discord channel webhook](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks) for the channel where you want the first bloods to be announced and copy the webhook link.

3. Create a [CTFd API token](https://docs.ctfd.io/docs/api/getting-started/#:~:text=Go%20to%20the%20%22Settings%22%20page,you%20should%20copy%20and%20save.) in your user settings and copy that down.
   
4. Update `.env` file with the webhook link from your discord channel and also add CTFd API token from your instance of CTFd.

5. Run following command:
   ```bash
   ./docker-build.sh
   ```

## Note 

In case of any changes in Docker, run:

```bash
docker exec -it <name-or-id-of-running-container> bash
```

After making changes, you can export your newly modified image:

```
docker commit <container-id> <image-name-to-be-created>:<tag>
```

Please keep in mind that I am not an expert when it comes to making Discord bots. If you find any issues in this code or want to contribute, please fork the repository and submit a pull request with any improvements.

