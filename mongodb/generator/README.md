
# Usage

```bash
python ./dummy_data_generator.py
```

## Arguments
### Generate Data
```bash
python ./dummy_data_generator.py  --generate <apps_num> <models_num> <records_num> <fields_num>
```
for example, ` --generate 10 100 1000 15` will generate:
* 10 apps
    * 100 models per app
        * 1000 records per model
            * 10 fields per record

### Drop Multiple Database (Apps)
This method could be used when a bulk drop of database is needed.
`app_0` to `app_{number_of_apps - 1}` will be dropped in total.
```bash
python ./dummy_data_generator.py  --drop <number_of_apps>
```


