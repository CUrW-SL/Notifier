# Email Notifier to Check and Notify 'curw' Database Inconsistencies

## Installing dependencies
- Create a python3 virtual environment.
- Activate created virtual environment.
- Within virtual environment install PyMySQl using `pip install PyMySQL`
- Within virtual environment run `email_notifier.py`

## Configurations
- All the configurations are in the `config.py`
- DATABASE_CONFIG: contains database configs
- SOURCES: The list of sources against which data consistency should be checked
- FORECAST_DAYS: The map of forecast days per each source.
- RECIPIENT_LIST: The list of emails to whom notifications should be sent.
- EMAIL_SERVER_CONFIG: Configs related to smtp server.
