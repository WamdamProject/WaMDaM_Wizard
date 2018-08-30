
from ..ConnectDB_ParseExcel import DB_Setup
from ..ConnectDB_ParseExcel import SqlAlchemy as sq


'''
This class is used to get data making sheets for meta data.
'''
class GetMetadata(object):
    def __init__(self):
        self.setup = DB_Setup()
        self.session = self.setup.get_session()

    def GetOrganizations(self, selectedResourceType):
        '''
            This method is used to get data of Organizations by selected ResourceTypeAcronym.
            :param  selectedResourceType: value of selected ResourceTypeAcronym.
            :return: list of set of data queried
        '''
        try:
            result = self.session.query(sq.ResourceTypes.ResourceTypeAcronym, sq.Organizations.OrganizationName, sq.Organizations.OrganizationType,
                                        sq.Organizations.OrganizationWebpage, sq.Organizations.Description).\
                    filter(sq.ResourceTypes.ResourceTypeAcronym == selectedResourceType).\
                    join(sq.Methods,
                         sq.Methods.MethodID == sq.ResourceTypes.MethodID).\
                    join(sq.People,
                         sq.People.PersonID == sq.Methods.PersonID).\
                    join(sq.Organizations,
                         sq.Organizations.OrganizationID == sq.People.OrganizationID).all()
            #Get data the remaining data except overlapping OrganizationName.
            nameResult = list()
            dataResult = list()
            for row in result:
                isExisting = False
                for name in nameResult:
                    if name == row.OrganizationName:
                        isExisting = True
                        break
                if not isExisting:
                    nameResult.append(row.OrganizationName)
                    dataResult.append([row.OrganizationName, row.OrganizationType,
                                       row.OrganizationWebpage, row.Description])

            return dataResult
        except Exception as e:
            # define.logger.error('Failed metAData load.\n' + e.message)
            raise Exception('Error occurred in reading Data Structure.\n' + e.message)

    def GetPeople(self, selectedResourceType):
        '''
            This method is used to get data of People by selected ResourceTypeAcronym.
            :param  selectedResourceType: value of selected ResourceTypeAcronym.
            :return: list of set of data queried
        '''
        try:
            result = self.session.query(sq.ResourceTypes.ResourceTypeAcronym, sq.People.PersonName, sq.People.Address,
                                        sq.People.Email, sq.People.Phone, sq.People.PersonWebpage,
                                        sq.People.Position).\
                    filter(sq.ResourceTypes.ResourceTypeAcronym == selectedResourceType).\
                    join(sq.Methods,
                         sq.Methods.MethodID == sq.ResourceTypes.MethodID).\
                    join(sq.People,
                         sq.People.PersonID == sq.Methods.PersonID).all()
            #Get data the remaining data except overlapping PersonName.
            nameResult = list()
            dataResult = list()
            for row in result:
                isExisting = False
                for name in nameResult:
                    if name == row.PersonName:
                        isExisting = True
                        break
                if not isExisting:
                    nameResult.append(row.PersonName)
                    dataResult.append([row.PersonName, row.Address,
                                       row.Email, row.Phone, row.PersonWebpage,
                                       row.Position])

            return dataResult
        except Exception as e:
            # define.logger.error('Failed metAData load.\n' + e.message)
            raise Exception('Error occurred in reading Data Structure.\n' + e.message)

    def GetSources(self, selectedResourceType):
        '''
            This method is used to get data of Sources by selected ResourceTypeAcronym.
            :param  selectedResourceType: value of selected ResourceTypeAcronym.
            :return: list of set of data queried
        '''
        try:
            result = self.session.execute("""Select SourceName,SourceWebpage, SourceCitation,Sources.Description as Description 
                FROM ResourceTypes
                left join ObjectTypes on ObjectTypes.ResourceTypeid=ResourceTypes.ResourceTypeid 
                left join Attributes on Attributes.ObjectTypeid = Objecttypes.Objecttypeid 
                left join Mappings on Mappings.Attributeid = Attributes.Attributeid 
                left join Instances on instances.instanceid = Mappings.Instanceid 
                LEFT JOIN Sources ON Sources.SourceID=Mappings.SourceID 
                WHERE ResourceTypeAcronym='{}'""".format(selectedResourceType)
                )
            #Get data the remaining data except overlapping SourceName.
            nameResult = list()
            dataResult = list()
            for row in result:
                isExisting = False
                if row.SourceName in nameResult:
                    isExisting = True
                if not isExisting:
                    nameResult.append(row.SourceName)
                    dataResult.append([row.SourceName, row.SourceWebpage, '',
                                       row.SourceCitation, row.Description])

            return dataResult
        except Exception as e:
            # define.logger.error('Failed metAData load.\n' + e.message)
            raise Exception('Error occurred in reading GetSources.\n' + e.message)

    def GetMethods(self, selectedResourceType):
        '''
            This method is used to get data of Methods by selected ResourceTypeAcronym.
            :param  selectedResourceType: value of selected ResourceTypeAcronym.
            :return: list of set of data queried
        '''
        try:
            result = self.session.query(sq.ResourceTypes.ResourceTypeAcronym, sq.Methods.MethodName, sq.Methods.MethodWebpage,
                                        sq.Methods.MethodCitation, sq.Methods.MethodTypeCV, sq.Methods.Description).\
                    filter(sq.ResourceTypes.ResourceTypeAcronym == selectedResourceType). \
                        join(sq.Methods,
                             sq.Methods.PersonID == sq.Methods.PersonID).all()
                    # join(sq.Methods,
                    #      sq.Methods.MethodID == sq.ResourceTypes.MethodID).\

            #Get data the remaining data except overlapping MethodName.
            nameResult = list()
            dataResult = list()
            for row in result:
                isExisting = False
                for name in nameResult:
                    if name == row.MethodName:
                        isExisting = True
                        break
                if not isExisting:
                    nameResult.append(row.MethodName)
                    dataResult.append([row.MethodName, row.MethodWebpage,
                                       row.MethodCitation, row.MethodTypeCV, row.Description])

            return dataResult
        except Exception as e:
            # define.logger.error('Failed metAData load.\n' + e.message)
            raise Exception('Error occurred in reading Data Structure.\n' + e.message)

    # def GetOrganizations(self):
    #     '''
    #     This method is used to get data making Organizations_table.
    #     :return: list of row (queried)
    #     '''
    #     result = self.session.query(sq.Organizations.OrganizationName, sq.Organizations.OrganizationType,
    #                                 sq.Organizations.OrganizationWebpage, sq.Organizations.Description).all()
    #     complete_result = list()
    #     nameResult = list()
    #     for row in result:
    #         isExisting = False
    #         for name in nameResult:
    #             if name == row.OrganizationName:
    #                 isExisting = True
    #                 break
    #         if not isExisting:
    #             nameResult.append(row.OrganizationName)
    #             complete_result.append([row.OrganizationName, row.OrganizationType, row.OrganizationWebpage,
    #                                     row.Description])
    #     return complete_result
    # def GetPeople(self):
    #     '''
    #     This method is used to get data making People_table.
    #     :return: list of row (queried)
    #     '''
    #     result = self.session.query(sq.People.PersonName, sq.People.Address, sq.People.Email,
    #                                 sq.People.Phone, sq.People.PersonWebpage,sq.People.Position,
    #                                 sq.Organizations.OrganizationName).\
    #                 join(sq.Organizations,
    #                      sq.Organizations.OrganizationID == sq.People.OrganizationID).all()
    #     complete_result = list()
    #     nameResult = list()
    #     for row in result:
    #         isExisting = False
    #         for name in nameResult:
    #             if name == row.PersonName:
    #                 isExisting = True
    #                 break
    #         if not isExisting:
    #             nameResult.append(row.PersonName)
    #             complete_result.append([row.PersonName, row.Address, row.Email, row.Phone,
    #                                     row.PersonWebpage, row.Position, row.OrganizationName])
    #     return complete_result
    # def GetSources(self):
    #     '''
    #     This method is used to get data making Sources_table.
    #     :return: list of row (queried)
    #     '''
    #     result = self.session.query(sq.Sources.SourceName, sq.Sources.SourceWebpage, sq.Sources.SourceCitation,
    #                                 sq.People.PersonName, sq.Sources.Description).\
    #                 join(sq.People,
    #                      sq.People.PersonID == sq.Sources.PersonID).all()
    #     complete_result = list()
    #     nameResult = list()
    #     ''' duplicate row check'''
    #     for row in result:
    #         isExisting = False
    #         for name in nameResult:
    #             if name == row.SourceName:
    #                 isExisting = True
    #                 break
    #         if not isExisting:
    #             nameResult.append(row.SourceName)
    #             complete_result.append([row.SourceName, row.SourceWebpage, row.SourceCitation,
    #                                     row.PersonName, row.Description])
    #     return complete_result
    # def GetMethods(self):
    #     '''
    #     This method is used to get data making Methods_table.
    #     :return: list of row (queried)
    #     '''
    #     result = self.session.query(sq.Methods.MethodName, sq.Methods.MethodWebpage, sq.Methods.MethodCitation,
    #                                 sq.Methods.MethodTypeCV, sq.People.PersonName, sq.Methods.Description).\
    #                 join(sq.People,
    #                      sq.People.PersonID == sq.Methods.PersonID).all()
    #     complete_result = list()
    #     nameResult = list()
    #     ''' duplicate row check'''
    #     for row in result:
    #         isExisting = False
    #         for name in nameResult:
    #             if name == row.MethodName:
    #                 isExisting = True
    #                 break
    #         if not isExisting:
    #             nameResult.append(row.MethodName)
    #             complete_result.append([row.MethodName, row.MethodWebpage, row.MethodCitation,
    #                                     row.MethodTypeCV, row.PersonName, row.Description])
    #     return complete_result