


Once the user has defined a dataset, network, and scenarios which include nodes and links, they can import data values that describe the attributes of the nodes and links. There are eight different independent “data types” that can describe an attribute (Red tables in ER diagram) but this task will load data to four of them. Users will provide the data values based on their “type” in separate spreadsheets as shown in the workbook. Then users can import the data values for all the attributes of all the nodes and links of the network and scenarios in one time. 


The DataValuesMapperID in the DataValuesMapper is a unique identifier for each combination of an attribute, instance, scenario, source, and method and it connects all of them with a data value in any of the nine Tables. 
In the workbook template, the user will provide the above combinations of metadata in each DataValue sheet (e.g., parameter). The Wizard has to look up the primary key for each metadata and create an entry in the Mapping Table for all of them together. Then this DataValuesMapperID will be used as a foreign key in each of the Data Values Tables. 



Note: the DataValuesMapper bridge table allows “many to many” relationships between the combination and data values. A combination can have many data “text controlled” values like many “reservoir purpose” values for a reservoir instance: “recreation”, flood control”, and “hydropower”. At the same time “recreation” text controlled value can be shared across many reservoir instances like “Hyrum” and “Cutler” reservoirs. So if the user provides the same data value for multiple instances, then the Wizard only loads one data value and reuses its primary key for the other replicates. So the Wizard will not duplicate the same data value if it is shared across instances. 
There is an important software business rule that the Wizard must implement. Users must select a specific “AttributeTypeCVID” value from the controlled vocabulary list in the Attributes Table. The Wizard must allow the users to only populate data values in the corresponding DataValues table. If they select TimeSeries as an AttributeType, then only the TimeSeries table could be populated with data. The TimeSeries table could be left null (all of it). I’m guessing that an “if-clause” statement will track the selected AttributeTypeCVID value and associate it as property to the DataValuesMapperID. A validation error will tell the user if they try to enter data values to a DataValuesMapperID that is different than the assigned property. Any other way to handle it is fine.
 
In addition, any Attribute with an AttributeTypeCV=Dummy, the Wizard should not allow users to import “data values” for it. So none of the DataValues red tables should accept data values for it. 
