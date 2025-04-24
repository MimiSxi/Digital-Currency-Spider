"""
This example describes how to use the workflow interface to chat.
"""

import os
# Our official coze sdk for Python [cozepy](https://github.com/coze-dev/coze-py)
from cozepy import COZE_CN_BASE_URL
import sys
from configparser import ConfigParser

config_file = './config.ini'
conf = ConfigParser()
conf.read(config_file,encoding='utf-8')
item = conf['analysis']
# Get an access_token through personal access token or oauth.
coze_api_token = item['api_token']
# The default access is api.coze.com, but if you need to access api.coze.cn,
# please use base_url to configure the api endpoint to access
coze_api_base = COZE_CN_BASE_URL

from cozepy import Coze, TokenAuth, Message, ChatStatus, MessageContentType  # noqa

# Init the Coze client through the access_token.
coze = Coze(auth=TokenAuth(token=coze_api_token), base_url=coze_api_base)

# Create a workflow instance in Coze, copy the last number from the web link as the workflow's ID.
workflow_id = item['workflow_id']

# Call the coze.workflows.runs.create method to create a workflow run. The create method
# is a non-streaming chat and will return a WorkflowRunResult class.
workflow = coze.workflows.runs.create(
    workflow_id=workflow_id,
    parameters={
        "article_url": sys.argv[1]
    }
)

print(workflow.data)

