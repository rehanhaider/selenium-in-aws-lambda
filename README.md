Relevant [blog post](https://cloudbytes.dev/articles/run-selenium-in-aws-lambda-for-ui-testing) with detailed explanation.
------

# Using the GitHub repository directly

You need AWS SAM CLI installed and AWS credentials configured.

Open your terminal and run the following command to clone the [repository](https://github.com/rehanhaider/selenium-in-aws-lambda).

```git
git clone https://github.com/rehanhaider/selenium-in-aws-lambda.git
```

Navigate to the app directory. 

```bash
cd selenium-in-aws-lambda/selenium
```

Build the app.

```bash
sam build
```

Test the app locally.

```bash
sam local invoke
```

Deploy the app to AWS.

```bash
sam deploy --guided
