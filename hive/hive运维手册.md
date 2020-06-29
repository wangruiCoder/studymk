# <center>**HIVE 运维手册**</center>

## MetaStore配置
使用Oracle存储MetaStore时如果提示 `Error thrown executing CREATE TABLE TBLS`时修改`${HIVE_HOME}/lib中的hive-metastore-.jar`文件中的`package.jdo`并重新打包修改内容如下:

```xml
<field name="viewOriginalText" default-fetch-group="false">
    <column name="VIEW_ORIGINAL_TEXT" jdbc-type="LONGVARCHAR"/>
</field>

<field name="viewExpandedText" default-fetch-group="false">
    <column name="VIEW_EXPANDED_TEXT" jdbc-type="LONGVARCHAR"/>
</field>
```
自动化初始化sql脚本如果一直执行失败，可手动执行命令
- 进入hive安装目录scripts目录
- 执行 `schematool -initSchema -dbType oracle`

