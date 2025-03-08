import re

import pulumi
import pulumi_github as github

LABELS = {
    "name": ["urgent", "reading", "presentation"],
    "color": ["FF0000", "1A16D1", "C5DEF5"],
    "description": [
        "Top priority. Needed it yesterday.",
        "Research paper, textbook chapter(s), etc.",
        "Presentation for me to give during lecture",
    ],
}

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
    for i in range(len(LABELS["name"])):
        row = {}
        for k in LABELS.keys():
            row[k] = LABELS[k][i]
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

    with open("./README.md") as f:
        pulumi.export("readme", f.read())
