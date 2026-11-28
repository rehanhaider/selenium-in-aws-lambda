Relevant [blog post](https://cloudbytes.dev/snippets/run-selenium-in-aws-lambda-for-ui-testing) with detailed explanation.
------

# Using the GitHub repository directly

You need Node.js, uv, Docker with Buildx, the AWS CLI, and configured AWS credentials.

Clone the repository and install the project-local CDK CLI and Python dependencies.

```bash
git clone https://github.com/rehanhaider/selenium-in-aws-lambda.git
cd selenium-in-aws-lambda/selenium
npm ci
uv sync
```

Run `npx cdk bootstrap` once for the target AWS account and region before your first deployment. Then deploy the stack.

```bash
npx cdk deploy
```

The stack has no trigger. Attach your own or invoke the function directly by replacing `<FunctionName output>` with the name printed by CDK. The event names the page to read, and the function returns its meta description as `{"url": ..., "description": ...}`. A missing or invalid `url` fails the invocation.

```bash
aws lambda invoke --function-name '<FunctionName output>' --cli-binary-format raw-in-base64-out --payload '{"url": "https://cloudbytes.dev/"}' out.json && cat out.json
```

Remove the stack when you're finished.

```bash
npx cdk destroy
```
