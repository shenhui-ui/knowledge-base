---
type: moc
---
# <% tp.file.title %>

## 相关笔记
- 

## 维护 Dashboard
```dataview
TABLE type AS 类型, file.mtime AS 最近修改
FROM "00-收件箱" OR "01-日记" OR "03-软件开发" OR "04-AI与机器学习" OR "05-数据分析" OR "06-项目"
WHERE file.mtime >= date(today) - dur(7 days)
SORT file.mtime DESC
```
