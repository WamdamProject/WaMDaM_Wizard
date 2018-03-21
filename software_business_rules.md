## Software Business Rules the in the WaMDaM Data Loader Wizard

#### The following software business rules are mentioned in the paper and implemented in the WaMDaM Data Loader Wizard. Here we further describe the logic of how they are implemented. 

**1.	Relate an ObjectType and typology with its Instances**   
The WaMDaM Data Loader Wizard automatically defines a new dummy Attribute called ObjectInstances after each new ObjectType is created. The purpose of this rule is to query all the Instances of an ObjectType.

**2.	Relate an Instance with its ObjectType and typology**   
To load Instances into WaMDaM, a modeler must provide the ObjectType along with it under either the Nodes or Links sheets which imply the Instance typology. A software business rule verifies if the provided ObjectType typology matches the typology implied sheet name of the loaded Instance. Another software business rule ensures that each link in the Connections entity has a start and end node. 
When an Instance is loaded into WaMDaM, a software business rule uses its provided ObjectType to look up AttributeID for its dummy attribute called ObjectInstances all its Attributes and fills out the Mappings table foreign keys. Two of these keys are the Source and Method IDs for each Instance.    

**3.	Relate a ResourceType with its MasterNetwork**   
The WaMDaM Data Loader Wizard automatically defines a new dummy ObjectType with a special typology called “network” after creating each new ResourceType. The ObjectType dynamically carries a concatenated name that consists of ResourceAcronym value of the ResourceType and the static words “Global Attributes”. For example, the dummy ObjectType for a WEAP ResourceType would be “WEAP Global Attributes.” This ObjectType then can contain all the global Attributes that apply to all the nodes and links in a model such as the objective function value in an optimization model. If the modelers loads a new MasterNetwork, at least one Scenario, and nodes and links for ResourceType, then before doing so, the WaMDaM Data Loader Wizard automatically creates a new dummy Attribute called “ResourceTypeScenarios” within the dummy global attributes ObjectType. Next, the Wizard creates a new dummy Instance that carries the same name of each Scenario. Now the combination of the dummy global attributes ObjectType, dummy Attribute “ObjectTypeInstances”, and each dummy Instance for each Scenario are mapped all in the Mappings table. This mapping also allows providing a source and method values for each scenario. Using this consistent convention of creating a chain of dummy records from the ResourceType into the MasterNetwork allows to both, connect those two together and to include global attributes. 
   
**4.	Enforce the Attribute data type to the DataValues entities**  
When data are loaded into one of the DataValues group tables for an Attribute, a software business rule, checks if the provided Attribute with the values have the same data types as the table the values being loaded into. A rule fills out the Mappings and ScenarioMappings tables given the provided ObjectType, AttributeName, Source, and Method   

**5.	Share similar data of an Attribute across Instances**   
A software business rule in the WaMDaM Wizard checks if any given value already exists in the table, if so, then it reuses its DataValuesMapperID into the Mappings table  
