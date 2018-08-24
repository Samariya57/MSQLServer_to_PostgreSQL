#
# To run the tests,
# first install pytest: `pip install pytest`,
# then run py.test from the directory containing this file
#

import statements as s


def test_statements():
    out = []
    for w in s.sql_statements('../initial__scripts/test.sql'):
        out.append(w)

    assert out == [
        'SET QUOTED_IDENTIFIER ON',

        'GO',

        'CREATE TABLE [dbo].[Categories](\n'
        '	[CategoryID] [int] IDENTITY(1,1) NOT NULL,\n'
        '	[CategoryName] [nvarchar](15) NOT NULL,\n'
        '	[Description] [ntext] NULL,\n'
        ' CONSTRAINT [PK_Categories] PRIMARY KEY CLUSTERED\n'
        '(\n'
        '	[CategoryID] ASC\n'
        ')WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, '
        'IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]\n'
        ') ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]',

        'GO',

        '/****** Object:  Table [dbo].[CustomerGroupThresholds]    ******/',

        'SET ANSI_NULLS ON',

        'GO',

        'SET IDENTITY_INSERT [dbo].[Categories] ON',

        'INSERT [dbo].[Categories] ([CategoryID], [CategoryName], [Description]) '
        'VALUES (1, N\'Beverages\', N\'Soft drinks, coffees, teas, beers, and ales\')',

        'INSERT [dbo].[Suppliers] ([SupplierID], [CompanyName], [ContactName], [ContactTitle], '
        '[Address], [City], [Region], [PostalCode], [Country], [Phone], [Fax], [HomePage]) '
        'VALUES (29, N\'Forï뾽ts d\'\'ï뾽rables\', N\'Chantal Goulet\', N\'Accounting Manager\', N\'148 rue Chasseur\', '
        'N\'Ste-Hyacinthe\', N\'Quï뾽bec\', N\'J2S 7S8\', N\'Canada\', N\'(514) 555-2955\', N\'(514) 555-2921\', NULL)',

        'SET IDENTITY_INSERT [dbo].[Suppliers] OFF',

        'ALTER TABLE [dbo].[OrderDetails] ADD  CONSTRAINT [DF_Order_Details_UnitPrice]  DEFAULT (0) FOR [UnitPrice]',

        'GO',

        'ALTER TABLE [dbo].[OrderDetails]  WITH NOCHECK '
        'ADD  CONSTRAINT [FK_Order_Details_Orders] FOREIGN KEY([OrderID])\n'        
        'REFERENCES [dbo].[Orders] ([OrderID])',

        'GO'
    ]
