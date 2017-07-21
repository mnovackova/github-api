import requests
import click
import sys
import threading
import multiprocessing

URL_BASE = 'http://127.0.0.1:5000/'
#URL_BASE = 'https://api.github.com/'

pocet_pristupu = 0

@click.command()
@click.option('--u', 'username')
def searching(username):
    url = "{}users/{}/repos".format(URL_BASE, username)
    r = requests.get(url)
    print(url)
    if not r.ok:
        print('Špatná url u repozitářů:', r.status_code)
        sys.exit(1)

    repos = r.json()

    print('USERNAME: ', username)

    control_list= []
    for repo in repos:
        #t = threading.Thread(target=searching_followers, args=(repo, username))
        t = multiprocessing.Process(target=searching_followers, args=(repo, username))
        control_list.append(t)
        t.start()

    for item in control_list:
        item.join()
    print('Hotovo.')

def searching_followers(repo, username):
    repo_name = repo["name"]

    url = '{}repos/{}/{}/subscribers'.format(URL_BASE, username, repo_name)
    r = requests.get(url)
    global pocet_pristupu
    pocet_pristupu += 1
    print(pocet_pristupu)

    if not r.ok:
        print('Špatná url:', r.status_code)
        sys.exit(1)

    seznam_followeru = r.json()

    print('\tREPO:', repo_name )
    for follower in seznam_followeru:
        print('\t\t', follower['login'])


if __name__ == '__main__':
    searching()
