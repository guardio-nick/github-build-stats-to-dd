# Build Stats: Gather action stats & Ship it as Logs to Datadog

This GitHub Action automates the process of gathering statistics from a specific run and pushing the collected data to Datadog as logs.

## Usage

1. Create an API Key in datadog.

2. Add the Datadog API Key to the Action. Name the secret `DD_API_KEY`.

3. Provide the Datadog Site and the ENV you want to ship the logs to. (DD_SITE,ENV)

4. Provide a `GITHUB_TOKEN`, as an input with repo access.

5. Preferably, this action should be the last one, scheduled after all other jobs. You can utilize the `needs` keyword to achieve this.

## Getting Started

Example workflow:

    build-stats:

      name: Build Stats
      runs-on: ubuntu-latest
      needs: [last_job]
    
      steps:
      - name: Get Github Build Stats for current run
        uses: SallyBlichG/github-build-stats@main
        with: 
          DD_API_KEY: ${{ secrets.DD_API_KEY }}
          DD_SITE: "datadoghq.com"
          ENV: DEV
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}


## Inputs
All inputs are required!

`GITHUB_TOKEN`: GitHub token to access the build stats. Repo access should be good enough

`DD_API_KEY`: Datadog API Key

`DD_SITE`: Datadog Site ("datadoghq.com" for example)

`ENV`: Datadog ENV (DEV/TEST/PROD etc...)

## Contributions
* This Project was forked from SallyBlichG/github-build-stats Github action.

* This project is using [Valgrind](https://valgrind.org/) for caching APT packages in GitHub Actions workflow.
  Valgrind is an instrumentation framework for building dynamic analysis tools. It can detect memory leaks and threading bugs, which are common in C and C++ programs.

