import argparse
import requests

parser = argparse.ArgumentParser()

#parser.add_argument("name")

args = parser.parse_args()

endpoint = 'https://api.github.com/graphql'

headers = {
    'Authorization': f'Bearer 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'
}

def getRepositoriesFromOrganization(owner):
    query = """
        query($owner: String!, $cursor: String) {
            organization(login: $owner) {
                repositories(
                    first: 100
                    ownerAffiliations: OWNER
                    privacy: PUBLIC
                    isFork: false
                    isLocked: false
                    orderBy: { field: NAME, direction: ASC }
                    after: $cursor
		        )
                {
                    totalCount
                                
                    pageInfo {
                        hasNextPage
                        endCursor
                    }
                                
                    nodes {
                        name
                    }
		        }
            }
        }
    """

    variables = {
        'owner': owner
    }

    response = requests.post(endpoint, headers=headers, json={'query': query, 'variables': variables})
    json_data = response.json()

    repos = []
    for repo in json_data['data']['organization']['repositories']['nodes']:
        repos.append(repo['name'])
    
    return repos

def getRepositoriesFromUser(owner):
    query = """
        query($owner: String!, $cursor: String) {
            user(login: $owner) {
                repositories(
                    first: 100
                    ownerAffiliations: OWNER
                    privacy: PUBLIC
                    isFork: false
                    isLocked: false
                    orderBy: { field: NAME, direction: ASC }
                    after: $cursor
		        )
                {
                    totalCount
                                
                    pageInfo {
                        hasNextPage
                        endCursor
                    }
                                
                    nodes {
                        name
                    }
		        }
            }
        }
    """

    variables = {
        'owner': owner
    }

    response = requests.post(endpoint, headers=headers, json={'query': query, 'variables': variables})
    json_data = response.json()

    repos = []
    for repo in json_data['data']['user']['repositories']['nodes']:
        repos.append(repo['name'])
    
    return repos



repos = getRepositoriesFromOrganization("ISPP-G8")
print(repos)

repos = getRepositoriesFromUser("RingoML")
print(repos)
