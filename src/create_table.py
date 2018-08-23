import re

def create_table_psql(tsql):
    """
    Translates the CREATE TABLE statement from T-SQL to PostgresQL.

    :param tsql: The CREATE TABLE statement in T-SQL (i.e., SQL Server) syntax
    :type tsql: string
    :return: The equivalent CREATE TABLE statement in PostgresQL syntax
    :rtype: string
    """

    # replace 'dbo' with 'public'
    tsql = re.sub(r'dbo', 'public', tsql, re.M)

    # remove square brackets
    tsql = re.sub(r'\[|\]','',tsql, re.M)

    # convert types
    tsql = re.sub(r'nchar', 'char', tsql, re.M)
    tsql = re.sub(r'nvarchar', 'varchar', tsql, re.M)
    tsql = re.sub(r'ntext', 'text', tsql, re.M)
    tsql = re.sub(r'datetime', 'date', tsql, re.M)

    return tsql
