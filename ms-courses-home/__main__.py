import re
import copy
from typing import List
from html.parser import HTMLParser

import pulumi
import pulumi_github as github

ADD_REPOS = ["columbia-ms-courses-home"]
IGNORE_REPOS = [
    "e4750-2024fall-assignments-po2311",
    "e4750-2024fall-project-dnpo-dn2614-po2311",
]


class MyIssueLabel:
    def __init__(self, name, color, description=None, url=None):
        self.name = name
        self.color = color
        self.description = description
        self.url = url

    def __str__(self):
        return (
            f'label: "{self.name}", color: "{self.color}", desc: "{self.description}"'
        )


class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.data = []

    def handle_data(self, data):
        """
        Extract the repo from the url in "<tag_1><tag_2>...[Repo](https://wwww.github.com/user/repo)...</tag_2></tag_1>"
        """
        d = data.partition("]")[2]
        url = d[1:-1]
        repo = url.split("/")[-1]

        self.data.append(repo)


def get_col_from_md(md: str, col: str, n: int):
    pattern = r"\|.*?" * n + r"\|"
    regex = re.compile(pattern)

    md_table = []
    for match in regex.finditer(md):
        line = match.group(0).split("|")
        line = list(filter(None, line))
        line = list(map(lambda x: x.strip(), line))
        md_table.append(line)

    cols = md_table[0]
    rows = md_table[2:]

    data = {cols[i]: [row[i] for row in rows] for i in range(len(cols))}

    return data[col]


def set_issue_labels(repo: str, labels: List):
    issue_labels = []
    pulumi.info(f"For repo {repo}...")
    for label in labels:
        pulumi.info(f"  - setting {label}")
        row = {
            "color": label.color,
            "name": label.name,
            "description": label.description,
            "url": label.url,
        }
        issue_labels.append(row)
    res = github.IssueLabels(f"labels-{repo}", repository=repo, labels=issue_labels)
    return res


if __name__ == "__main__":
    labels_config = pulumi.Config("labels")
    readme = labels_config.require("readme")

    labels = [
        MyIssueLabel("urgent", "FF0000", "Top priority. Needed it yesterday."),
        MyIssueLabel("reading", "1A1601", "Research paper, textbook chapter(s), etc."),
        MyIssueLabel(
            "presentation", "C5DEF5", "Presentation for me to give during lecture."
        ),
        MyIssueLabel("programming", "C5A2A9", "Involves writing code."),
    ]

    md = ""
    with open(readme, "r") as f:
        md += f.read()

    repos_col = get_col_from_md(md, "Repositories", 3)

    my_html_parser = MyHTMLParser()
    list(map(my_html_parser.feed, repos_col))
    repos = copy.deepcopy(my_html_parser.data)

    repos = list(filter(lambda x: x not in IGNORE_REPOS, repos))
    repos.extend(ADD_REPOS)
    labels = list(map(lambda r: set_issue_labels(r, labels), repos))
