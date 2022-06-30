# Run Selenium in AWS Lambda

Let me begin by expressing my frustration 😡😡😡 with the fact that AWS doesn't have a pre-configured selenium image for Lambda on their public ECR marketplace. Selenium is the go-to tool for UI testing and for building many kinds of bots but running it on Lambda is complicated. 

The easiest method is, as [I explained earlier](0017-run-lambda-on-container-sam.md),  to to use Docker for Lambda to create an image with selenium, chrome / chromium headless and webdriver, but given the way Lambda restricts the environment making it work on selenium is quite difficult but not impossible. 

Relevant [blog post](https://cloudbytes.dev/articles/run-selenium-in-aws-lambda-for-ui-testing) with detailed explanation.

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