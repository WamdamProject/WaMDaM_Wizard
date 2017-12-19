## Generic Excek Workbook template for Input Data  

[Excel Workbook ](https://github.com/WamdamProject/WaMDaM_UseCases/blob/master/UseCases_files/0WorkbookTemplates/InputData_Template/WaMDaM_InputData_template.xlsm?raw=true)  
![](https://github.com/WamdamProject/WaMDaM_UseCases/blob/master/UseCases_files/0WorkbookTemplates/InputData_Template/template.PNG)

Generally, defining and loading data into a WaMDaM database follows this order.   
**First** load the controlled vocabulary or leave them blank.   
**Second** define metadata that will be used for the Attributes and Instances.   
**Third** define the data structure of Object Types and Attributes.       
**Fourth** add the master network, scenario, and nodes and links.  
**Fifth** load data values to each attribute of each Instance. We chose Excel as a generic input data medium which the data sources have to be converted and formatted to fit into a custom Excel workbook that has 17 sheets with fixed column headers for the main tables of input data in WaMDaM.     
Each dataset is prepared to a single workbook one-at-a-time. The Wizard maps all the bridge tables’ complex relationships and users do not need to know anything about primary or foreign keys.
These sheets are: Organizations&People, Sources&Methods, Datasets&ObjectTypes, Attributes, Networks&Scenarios, Nodes, Links, DualValues, NumericValues, DescriptorValues, SeasonalNumericValues, TimeSeries, TimeSeriesValues, MultiAttributeSeries, ObjectCategory, AttributeCategory, and InstanceCategory. The sheets are related with each other through dropdown lists to help users for example to relate metadata elements to the attributes and data values.  


**from the Appendix**  
These sheets are: Organizations&People, Sources&Methods, Datasets&ObjectTypes, Attributes, Networks&Scenarios, Nodes, Links, DualValues, NumericValues, DescriptorValues, SeasonalNumericValues, TimeSeries, TimeSeriesValues, MultiAttributeSeries, ObjectCategory, AttributeCategory, and InstanceCategory. The sheets are related with each other through dropdown lists to help users for example to relate metadata elements to the attributes and data values. A workbook template is available on GitHub. Users have to populate at least six sheets for any dataset and they can populate more as the complexity of the dataset increases. In a simple case, the three sheets of Organizations&People, Sources&Methods, Networks&Scenarios can be populated with only two rows each. Then users define the dataset structure of object types and attributes, add the nodes and links, and finally add the data values for the attributes of each node or link. Controlled vocabulary are available in the template workbook and users can update them in a button on the workbook’s homepage sheet. The button calls the online registry application user interface and updates the list of vocabularies in the sheet. Then the CVs are available as dropdown lists in each sheet where they apply.  
