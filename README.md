# Columbia MS Courses Home

The following table lists the courses I took during my Computer Engineering MS degree at Columbia University and links to the repositories for assignments, projects, and other course materials.

| Semester | Course | Repositories | Summary |
| -------- | ------ | ------------ | ------- |
| Fall 2024 | Natural Language Processing | <ul><li>[Assignments Repo](https://github.com/pablordoricaw/comsw4705-nlp-assignments)</li></ul> | Implemented foundational and deep learning NLP models in Python, including a trigram language model for text classification and a neural network for dependency parsing. Developed advanced applications using PyTorch, such as a conditioned LSTM language model for image captioning and a Semantic Role Labeling system utilizing BERT. |
| Fall 2024 | Introduction to Databases | <ul><li>[Projects Repo](https://github.com/pablordoricaw/comsw4111-intro-to-dbs-projects)</li></ul> | |
| Fall 2024 | System-on-Chip Platforms | <ul><li>[Assignments Repo](https://github.com/pablordoricaw/cseew4868-socp-assignments)</li></ul> | |
| Fall 2024 | Heterogenous Computing for Signal and Data Processing | <ul><li>[Assignments Repo](https://github.com/eecse4750/e4750-2024fall-assignments-po2311)</li><li>[Project Repo](https://github.com/eecse4750/e4750-2024fall-project-dnpo-dn2614-po2311)</li></ul> | |
| Spring 2025 | Private Systems | <ul><li>[Assignments Repo](https://github.com/pablordoricaw/comse6998-private-systems-assignments)</li><li>[Project Repo](https://github.com/pablordoricaw/comse6998-private-systems-project)</li></ul> | |
| Spring 2025 | Applied ML in the Cloud | <ul><li>[Assignments Repo](https://github.com/pablordoricaw/comse6998-applied-ml-cloud-assignments)</li><li>[Final Project Repo](https://github.com/pablordoricaw/comse6998-applied-ml-cloud-project)</li></ul> | |
| Spring 2025 | Embedded Scalable Platforms | <ul><li>[Project Repo](https://github.com/pablordoricaw/csee6868-esp-project)</li></ul> | |
| Spring 2025 | Large-Scale Stream Processing | <ul><li>[Assignments Repo](https://github.com/pablordoricaw/elene6889-stream-processing-assignments)</li></ul> | |
| Fall 2025 | Parallel Functional Programming | <ul><li>[Assignments Repo](https://github.com/pablordoricaw/comsw4995-parallel-fp-assignments)</li><li>[Project Repo](https://github.com/pablordoricaw/comsw4995-parallel-fp-project)</li></ul> | |
| Fall 2025 | Artificial Intelligence-of-Things | <ul><li>[Labs Repo](https://github.com/pablordoricaw/eecse4764-aiot-labs)</li><li>[Project Repo](https://github.com/pablordoricaw/eecse4764-aiot-project)</li></ul> | |
| Fall 2025 | Computer Networks | <ul><li>[Assignments Repo](https://github.com/pablordoricaw/cseew4119-computer-networks-assignments)</li></ul> | |
| Fall 2025 | Malware Analysis & Reverse Engineering | <ul><li>[Assignments Repo](https://github.com/pablordoricaw/comsw4186-malware-analysis-reverse-eng-assignments)</li></ul> | |
| Spring 2026 | Hardware Security | <ul><li>[Assignments Repo](https://github.com/pablordoricaw/comse6424-hw-security-assignments)</li></ul> | |
| Spring 2026 | Computer Hardware Design | <ul><li>[Assignments Repo](https://github.com/pablordoricaw/eecse4340-computer-hw-design-assignments)</li></ul> |

## Getting Started

1. Create a GitHub repository for a course assignments and/or project following the naming convention `<course-code>-<course-name>-<[assignments/project]>` i.e. `comsw4705-nlp-assignments`.

2. Create an entry for the course with the created repo in the table above.

3. Run the Pulumi Python [ms-courses-home](./ms-courses-home/) app **locally** to configure specific settings of the newly created repo.

## Template Metadata

Useful metadata to have handy for homeworks and projects.

```md
**Author:** Pablo Ordorica Wiener (UNI: po2311)

**Course:** <Course Number> <Course Name>

- **Semester:** <Fall/Spring> <yyyy>
- **Instructor:** <Instructor Full Name> (UNI: <xxxx>)

- **TA:** <TA Full Name> (UNI: <xxxx>)
```

## Cloud Infrastructure Strategy for Assignments and Projects

Some of the assignments and projects require cloud computing, and this section explains my approach to managing cloud resources for those courses.

As seen on the table above, there are two type of repositories:

- Individual assignments: One single repository per course containing all individual homework.
- Team projects: Separate repository per project (especially for team collaborations).

| Feature        | 👤 Individual Assignments        | 👥 Team Projects          |
| -------------- | -------------------------------- | ------------------------- |
| GCP Project    | Shared GCP Project               | New Dedicated GCP Project |
| Pulumi Project | Unique name per Assignments Repo | Unique name per Project   |
| Pulumi Stack   | main (local deployment)          | Depends on the project.   |
| State Backend  | Pulumi Cloud (Personal Org)      | GCP Bucket Storage        |

## Workflow for New Repositories

### 1. Individual Assignments

All individual assignments

1. share a single GCP Project to avoid overhead, but
2. use separate Pulumi Projects (one per assignments repo) to keep state isolated.

Run this in the root of your assignment repo:

```bash
# Initialize a new Pulumi Python project using 'uv' as the package manager
# --force is used because the directory already exists (the repo root)
pulumi new python --name <course-code>-<assignment-name> --toolchain uv --force
```

After initialization, add the my shared cloud infra library:

```bash
uv add "git+https://github.com/pablordoricaw/my-cloud-lib.git@v0.2.0#subdirectory=pulumi"
```

### Team Projects

For group projects, I use:

- A dedicated GCP Project is created for the team. This ensures my personal credits are not billed for team usage and allows teammates to have IAM access.
- A GCP Storage Bucket inside the team's project. This allows all teammates to read/write state without needing access to my personal Pulumi Cloud organization.

**Prerequisites:**

- A new GCP Project in the Google Cloud Console.
- Grant "Editor" IAM roles to all team members on that GCP Project.
- A storage bucket to use as the backend for the IaC state

Run this in the root of the project repo:

```bash
# 1. Authenticate to the Team's State Bucket (Teammates must do this too)
#    Ensure you have 'Storage Object Admin' on the bucket.
gcloud auth application-default login
pulumi login gs://<team-project-bucket-name>

# 2. Initialize the project (same as individual)
pulumi new python --name <project-name> --description "Course Code Team Project"

# 3. Configure the Stack to use the Team's GCP Project
pulumi config set gcp:project <team-gcp-project-id>
```


Add my shared infrastructure library if needed:

```bash
uv add "git+https://github.com/pablordoricaw/my-cloud-lib.git@v0.2.0#subdirectory=pulumi"
```
