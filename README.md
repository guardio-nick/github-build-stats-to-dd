# Build Stats: Gather action stats & Ship it as Metrics to Datadog

This GitHub Action automates the process of gathering statistics from a specific run and pushing the collected data to Datadog as metrics.

## Usage

1. Create an API and APP Keys in datadog.

2. Add the Datadog API Key to the Action. Name the secret `DD_API_KEY`.

3. Add the Datadog API Key to the Action. Name the secret `DD_APP_KEY`.

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
        uses: guardio-nick/github-build-stats-to-dd@main
        with: 
          DD_API_KEY: ${{ secrets.DD_API_KEY }}
          DD_API_KEY: ${{ secrets.DD_API_KEY }}
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          GITHUB_ORG_ID: myOrg


## Inputs
All inputs are required!

`GITHUB_TOKEN`: GitHub token to access the build stats. Repo access should be good enough

`GITHUB_ORG_ID`: GitHub Organization this action is running for.

`DD_API_KEY`: Datadog API Key

`DD_APP_KEY`: Datadog API Key


## Contributions
* This Project was forked from SallyBlichG/github-build-stats Github action.

* This project is using [Valgrind](https://valgrind.org/) for caching APT packages in GitHub Actions workflow.
  Valgrind is an instrumentation framework for building dynamic analysis tools. It can detect memory leaks and threading bugs, which are common in C and C++ programs.

