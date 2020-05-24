### Fuzzy string matching of companies' names

##### Requirements:

- `<dataset>.csv` dataset with company names
- `<queries>.txt` list of queries (separated by newlines '\n')
- `.api_key` for **Google Knowledge Graph Search API** (check: <https://developers.google.com/knowledge-graph>)


##### Launch example:

```
python launcher.py -d some_database.csv -q some_queries.txt -l company_name
```

For more options, check `python launcher.py -h`
