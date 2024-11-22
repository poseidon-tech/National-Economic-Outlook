# NEO Readme
The analysis of economic trends has long been an indispensable pillar of strategic business
planning, investment strategies, and policy formulation. These are invaluable tools for
informed decision making spanning various sectors and domains. They offer critical insights
into the health and the direction of the economy as well as its impact on society.
With this application, we intend to build a platform that empowers such studies. The
application will be an interactive trend visualization tool to allow end users to streamline their
research or study processes. Users will have control over most parameters of each trend to
further enhance the practicality of the application. The broader goal is to make large-scale
economic data more accessible, understandable, and actionable.
Economic trends are affected by a wide array of factors ranging from environmental to
sociopolitical elements. Thus, we recognize the importance of trying to accommodate as
much of this data into our trend studies. Consequently, we have chosen trends that can
represent and leverage various sources of data like demographics/population distribution,
crimes, business and GDP data, mortgage data, employment and poverty data.

## Motivation
Economic trends show us how certain factors like GDP, crime, mortgage rate, etc. which
influence the development of a country have been changing over the years. Accurately
depicting this requires vast amounts of historical data for each economic factor. These
datasets contain records on the scale of millions. The breadth of the trends we have
selected also means numerous datasets and sources that need to be cleaned and collated
in a single place. Storage and accurately processing these quantities of data for useful
information and trends can be challenging. Introducing a database helps significantly bring
down the complexity of these tasks. The natural correlation between various datasets that
have been chosen will also be easy to extract using a database.

## ER Diagram
![Screenshot 2024-11-22 153739](https://github.com/user-attachments/assets/6388ba45-c9c9-4af1-931a-a53b4d5a37dc)

## Login Page
![Screenshot 2024-11-22 154055](https://github.com/user-attachments/assets/9ccddf23-a776-43e2-9b9f-b7904362c1e0)

## Home Page
![Screenshot 2024-11-22 154049](https://github.com/user-attachments/assets/a89bb950-b4b8-45ec-a47a-23fd81c0ded7)

## Trend Visualization
![Screenshot 2024-11-22 154113](https://github.com/user-attachments/assets/34a6972c-23f8-4321-8968-b7506b3c538e)
![Screenshot 2024-11-22 154130](https://github.com/user-attachments/assets/3a7e60f8-2fe0-47db-9221-8f5487e2dec9)






## Development Setup

### Prerequisites
Python 3.x
pip

### Setup
We use virtualenv for our environment.
* [Virtual Environments Guide](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#create-and-use-virtual-environments)

```commmandline
# Clone the repository if not already done. 
git clone https://github.com/harshith47/DBMS-Group20-BE.git

# Create a virtualenv
python -m venv .venv

# Activate the environment
.venv\Scripts\Activate #on windows, Try source command for linux or check guide linked above.

# Install requirements
pip install -r requirements.txt
```

### Running the app
```commandline
# Environment Variables
There's a .env file in the neo directory. 
It's already part of gitignore but since the base copy exists in the repo, run the below git command to make sure it's untracked

git update-index --skip-worktree neo/.env

Update your credentials like database username and password in the file.
DO NOT forget to connect to the VPN since we're using cise oracle.

# Flask Run
flask --app neo run --debug
```
 


