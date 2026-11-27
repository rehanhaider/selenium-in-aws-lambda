Relevant [blog post](https://cloudbytes.dev/articles/run-selenium-in-aws-lambda-for-ui-testing) with detailed explanation.
------

# Using the GitHub repository directly

You need Node.js, Python 3.10 or later, Docker with Buildx, the AWS CLI, and configured AWS credentials. The target AWS account and region must be bootstrapped once with `npx cdk bootstrap`. The command uses the project-local CDK CLI installed by `npm ci`.

Clone the repository and install the CDK dependencies.

```bash
git clone https://github.com/rehanhaider/selenium-in-aws-lambda.git
cd selenium-in-aws-lambda/selenium
npm ci
python3 -m venv .venv && . .venv/bin/activate && pip install -r requirements-cdk.txt
```

Deploy the stack.

```bash
npx cdk deploy
```

The stack has no trigger. Attach your own or invoke the function directly by replacing `<FunctionName output>` with the name printed by CDK.

```bash
aws lambda invoke --function-name '<FunctionName output>' --cli-binary-format raw-in-base64-out --payload '{}' out.json && cat out.json
```

Remove the stack when you're finished.

```bash
npx cdk destroy
```
