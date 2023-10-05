import http.client
import json
import os
from datetime import datetime
from datadog import initialize, api


options = {
    'api_key': os.getenv('DD_API_KEY'),
    'app_key': os.getenv('DD_APP_KEY')
}

def main():
    initialize(**options)
    get_build_state_github()


def get_build_state_github():
    try:
        conn = http.client.HTTPSConnection("api.github.com")
        payload = ''
        headers = {
            'Accept': 'application/vnd.github.v3+json',
            'Authorization': f"Bearer {os.getenv('GITHUB_TOKEN')}",
            'User-Agent': 'github-build-stats/1.0'
        }
        conn.request("GET",
                     f"/repos/{os.getenv('GITHUB_ORG_ID')}/{os.getenv('GITHUB_REPOSITORY_NAME')}/actions/runs/{os.getenv('GITHUB_RUN_ID')}/jobs",
                     payload, headers)
        res = conn.getresponse()
        data = res.read()
        obj = json.loads(data.decode("utf-8"))
        datetime_format = "%Y-%m-%dT%H:%M:%S.%f%z"
        json_object_bq_data = []
        for row in obj['jobs']:
            workflow_name = row['workflow_name']
            job_name = (row['name']).replace("\\", "")
            url = row['html_url']
            for step in range(len(row['steps'])):
                if row['steps'][step]['status'] == "completed":
                    datetime_started_at = datetime.strptime(row['steps'][step]['started_at'], datetime_format)
                    datetime_completed_at = datetime.strptime(row['steps'][step]['completed_at'], datetime_format)
                    time_difference = datetime_completed_at - datetime_started_at
                    if time_difference.total_seconds() != 0.0:
                        print(row['steps'][step]["name"])
                        print(f"This step took: {time_difference.total_seconds()} seconds")
                        send_metric_to_dd(workflow_name,job_name,row['steps'][step]["name"],time_difference.total_seconds())
    except Exception as e:
        print("An exception occurred:", e)
        exit(1)


def send_metric_to_dd(workflow_name,job_name,step_name,time_consumed):
    try:
        metric_name = "github_actions_runtime_stats"
        metric_value = time_consumed
        tags = [
            "environment:cicd",
            f"workflow:{workflow_name}",
            f"job:{job_name}",
            f"step:{step_name}"
        ]
        host = "github_actions_runner"

        api.Metric.send(metric=metric_name, points=metric_value, tags=tags, host=host)
        print(f"Sent metric '{metric_name}' with value {metric_value} to Datadog with tags {tags}.")

    except Exception as e:
        print("An exception occurred on sending metric to datadog:", e)
        exit(1)

if __name__ == "__main__":
    main()
