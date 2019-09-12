
import ta_dbmonitor_declare

from splunktaucclib.rest_handler.endpoint import (
    field,
    validator,
    RestModel,
    MultipleModel,
)
from splunktaucclib.rest_handler import admin_external, util
from splunk_aoblib.rest_migration import ConfigMigrationHandler

util.remove_http_proxy_env_vars()


fields_logging = [
    field.RestField(
        'loglevel',
        required=False,
        encrypted=False,
        default='INFO',
        validator=None
    )
]
model_logging = RestModel(fields_logging, name='logging')


fields_additional_parameters = [
    field.RestField(
        'hec_token',
        required=True,
        encrypted=False,
        default='6b1413a3-d992-483f-9963-0778aadc7138',
        validator=validator.String(
            min_len=0, 
            max_len=8192, 
        )
    ), 
    field.RestField(
        'hec_server_port',
        required=True,
        encrypted=False,
        default='localhost:8088',
        validator=validator.String(
            min_len=0, 
            max_len=8192, 
        )
    ), 
    field.RestField(
        'workingdirectory',
        required=True,
        encrypted=False,
        default='/Users/mwiser/dbmonitor/splunk/etc/apps/TA-dbmonitor/static',
        validator=validator.String(
            min_len=0, 
            max_len=8192, 
        )
    ), 
    field.RestField(
        'java_parameters',
        required=True,
        encrypted=False,
        default='-Xms256m -Xmx2048m',
        validator=validator.String(
            min_len=0, 
            max_len=8192, 
        )
    ), 
    field.RestField(
        'cyberarkpath',
        required=True,
        encrypted=False,
        default='python /Users/mwiser/dbmonitor/splunk/etc/apps/TA-dbmonitor/static/getaccount.py -n ',
        validator=validator.String(
            min_len=0, 
            max_len=8192, 
        )
    ), 
    field.RestField(
        'ms_sql_is_domain',
        required=False,
        encrypted=False,
        default='Splunk',
        validator=validator.String(
            min_len=0, 
            max_len=8192, 
        )
    ), 
    field.RestField(
        'suicidemode',
        required=False,
        encrypted=False,
        default='No',
        validator=validator.String(
            min_len=0, 
            max_len=8192, 
        )
    )
]
model_additional_parameters = RestModel(fields_additional_parameters, name='additional_parameters')


endpoint = MultipleModel(
    'ta_dbmonitor_settings',
    models=[
        model_logging, 
        model_additional_parameters
    ],
)


if __name__ == '__main__':
    admin_external.handle(
        endpoint,
        handler=ConfigMigrationHandler,
    )
