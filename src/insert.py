import re


def insert_psql(tsql):
    """
    Translates the `INSERT` statement from T-SQL to PostgresQL.
    
    :param tsql: The `INSERT` statement in T-SQL (i.e., SQL Server) syntax
    :type tsql: string
    :return: The equivalent `INSERT` statement in PostgresQL syntax
    :rtype: string

    Example: 
      input = 
        INSERT [dbo].[Categories] ([CategoryID], [CategoryName], [Description]) 
        VALUES (1, N'Beverages', N'Soft drinks, coffees, teas, beers, and ales')
      output = 
        INSERT INTO Categories (CategoryID, CategoryName, Description) 
        VALUES (1, N'Beverages', N'Soft drinks, coffees, teas, beers, and ales');

    For now, we assume the input would always contain table_name, attr_name, and
    value (in order). For real case, there might be other options in between insert...
    table_name...attr_name...
    """

    substrs = tsql.split(' ', 2)

    # 1) update the INSERT INTO statement
    cmd, table_name = substrs[0].strip(),substrs[1].strip()
    if cmd == 'INSERT':
        cmd += ' INTO'

    # 2) update the table_name by removing [dbo]. and []
    if table_name.startswith('[dbo].'):
        table_name = table_name[7:-1]

    # 3) update the column_name (attributes) by removing []
    ppair = '\(([^()]*)\)' # matching () pair
    m = re.search(ppair,substrs[2])
    si,ei = m.start(),m.end()

    attr = substrs[2][si:ei].replace('[','')
    attr = attr.replace(']','')

    value = substrs[2][ei+1:]+';'

    result = ' '.join([cmd,table_name,attr,value])

    return result
