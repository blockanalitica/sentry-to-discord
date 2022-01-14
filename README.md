# sentry-to-discord

Service for sending Sentry errors to your Discord channel

## Heroku

Before deploying to Heroku you should be familiar with the basic concepts of [Git](https://git-scm.com/) and [Heroku](https://heroku.com/).

If you keep your project on GitHub you can use 'Deploy to Heroku' button thanks to which the deployment can be done in web browser with minimal configuration required.
The configuration used by the button is stored in `app.json` file.

<a href="https://heroku.com/deploy" style="display: block"><img src="https://www.herokucdn.com/deploy/button.svg" title="Deploy" alt="Deploy"></a>
    <br>

Deployment by using [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli):

* Create Heroku App. You can leave your app name, change it, or leave it blank (random name will be generated)

    ```bash
    heroku create sentry-to-discord
    ```

* Add buildpacks

    ```bash
    heroku buildpacks:add --index=1 heroku/python
    ```
* Set environmental variables (change `SENTRY_SECRET` and `DISCORD_SENTRY_WEBHOOK` value)

    ```bash
    heroku config:set SENTRY_SECRET=not-so-secret
    heroku config:set FLASK_APP=app.py
    heroku config:set DISCORD_SENTRY_WEBHOOK=discord-webhook-url
    ```

* Deploy on Heroku by pushing to the `heroku` branch

    ```bash
    git push heroku master
    ```