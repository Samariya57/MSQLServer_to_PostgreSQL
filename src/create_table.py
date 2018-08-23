import re

def create_table_psql(tsql):
    """
    Translates the CREATE TABLE statement from T-SQL to PostgresQL.

    :param tsql: The CREATE TABLE statement in T-SQL (i.e., SQL Server) syntax
    :type tsql: string
    :return: The equivalent CREATE TABLE statement in PostgresQL syntax
    :rtype: string
    """

    # force to lower case
    tsql = tsql.lower()

    # replace 'dbo' with 'public'
    tsql = re.sub(r'[dbo]\.', '', tsql, re.M|re.DOTALL)

    # remove square brackets
    tsql = re.sub(r'\[|\]','',tsql, re.M|re.DOTALL)

    # convert types
    tsql = re.sub(r'nchar', 'char', tsql, re.M|re.DOTALL)
    tsql = re.sub(r'nvarchar', 'varchar', tsql, re.M|re.DOTALL)
    tsql = re.sub(r'ntext', 'text', tsql, re.M|re.DOTALL)
    tsql = re.sub(r'money', 'numeric(19,4)', tsql, re.M|re.DOTALL)
    tsql = re.sub(r'datetime', 'timestamp', tsql, re.M|re.DOTALL)

    # remove all non-supported optional keywords
    tsql = re.sub(r'clustered', '', tsql, re.M|re.DOTALL)

    return tsql
