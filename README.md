# matano-scripts




# Useful SQL Queries

```
SELECT source_address, count(*) as count FROM "matano"."matano_alerts_view"
group by source_address 
```
