# datadog-monitor-sync
Sync datadog monitor from local to datadog

## Create Monitor
```
python3 main.py deploy \
    --api-key $DATADOG_API_KEY \
    --app-key $DATADOG_APP_KEY \
    $MONITOR_FILE
```

1.  `$MONITOR_FILE` shoud have `.monitor` extension    
2.  Content of `$MONITOR_FILE` is a list of json-formated monitor (exported from datadog WebUI)



## Sync Monitor
```
python3 main.py sync \
    --api-key $DATADOG_API_KEY \
    --app-key $DATADOG_APP_KEY \
    --datadog-monitors-root $DATADOG_MONITORS_ROOT
```
1.  $DATADOG_MONITORS_ROOT is the root directory of your `.monitor` file (it'll search recursively for `.monitor` file)
2.  Example of directory structure below
    ```
      datadaog_monitor
      ├── int
      │   └── web
      |       └── standard.monitor
      └── prod
          └── web
              └── standard.monitor
    ```
 
## Environment Variables
**DATADOG_API_KEY**: default value for `--datadog-api-key`

**DATADOG_APP_KEY**: default value for `--datadog-app-key`
