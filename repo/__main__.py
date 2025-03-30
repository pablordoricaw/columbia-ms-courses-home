import re

import pulumi
import pulumi_github as github


class MyLabel:
    def __init__(self, name, color, description=None, url=None):
        self.name = name
        self.color = color
        self.description = description
        self.url = url

    def __str__(self):
        return (
            f'label: "{self.name}", color: "{self.color}", desc: "{self.description}"'
        )


LABELS = [
    MyLabel("urgent", "FF0000", "Top priority. Needed it yesterday."),
    MyLabel("reading", "1A1601", "Research paper, textbook chapter(s), etc."),
    MyLabel("presentation", "C5DEF5", "Presentation for me to give during lecture."),
    MyLabel("programming", "C5A2A9", "Involves writing code."),
]

ADD_REPOS = ["columbia-ms-courses-home"]
IGNORE_REPOS = ["e4750-2024fall-assignments-po2311"]


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


def set_issue_labels(repo: str):
    issue_labels = []
    pulumi.info(f"For repo {repo}...")
    for label in LABELS:
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

    md = ""
    with open(readme, "r") as f:
        md += f.read()

    repos_col = get_col_from_md(md, "Repositories", 3)

    url_p = r"https://github\.com/([^/]+)/([^/)]+)"
    repos = list(map(lambda x: re.search(url_p, x).group(2), repos_col))
    repos = list(filter(lambda x: x not in IGNORE_REPOS, repos))
    repos.extend(ADD_REPOS)

    labels = list(map(set_issue_labels, repos))
