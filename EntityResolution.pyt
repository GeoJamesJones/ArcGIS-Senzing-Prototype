# -*- coding: utf-8 -*-

from __future__ import annotations

import arcpy

from entity_resolution import EntityResolution


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Entity Resolution"
        self.alias = "Entity Resolution"

        # List of tool classes associated with this toolbox
        self.tools = [
            CreateLocalEntityStore,
            AddRecordsToLocalEntityStore,
            SearchLocalEntityStore,
            ExportLocalEntityStore,
            FindRelationshipsFromArea,
            ProcessRedoRecords,
        ]


class AddRecordsToLocalEntityStore:
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Add Records To Local Entity Store"
        self.description = ""
        self.canRunInBackground = False
        
        self.name_values = [
            EntityResolution.NAME_FULL.value,
            EntityResolution.NAME_ORG.value,
            EntityResolution.NAME_LAST.value,
            EntityResolution.NAME_FIRST.value,
            EntityResolution.NAME_MIDDLE.value,
            EntityResolution.NAME_PREFIX.value,
            EntityResolution.NAME_SUFFIX.value,
        ]

        self.address_values = [
            EntityResolution.ADDR_FULL.value,
            EntityResolution.ADDR_LINE1.value,
            EntityResolution.ADDR_LINE2.value,
            EntityResolution.ADDR_LINE3.value,
            EntityResolution.ADDR_LINE4.value,
            EntityResolution.ADDR_LINE5.value,
            EntityResolution.ADDR_LINE6.value,
            EntityResolution.ADDR_CITY.value,
            EntityResolution.ADDR_STATE.value,
            EntityResolution.ADDR_ZIP.value,
            EntityResolution.ADDR_COUNTRY.value,
            EntityResolution.ADDR_FD.value,
            EntityResolution.ADDR_TD.value,
        ]

        self.phone_types = [
            EntityResolution.HOME.value,
            EntityResolution.MOBILE.value,
            EntityResolution.BUSINESS.value,
            EntityResolution.OTHER.value,
        ]

        self.phone_values = [
            EntityResolution.PHONE_NUM.value,
            EntityResolution.PHONE_FD.value,
            EntityResolution.PHONE_TD.value,
        ]

        self.identifier_values = [
            EntityResolution.PASSPORT.value,
            EntityResolution.PASSPORT_COUNTRY.value,
            EntityResolution.DRIVERS_LICENSE.value, 
            EntityResolution.DRIVERS_LICENSE_STATE.value,
            EntityResolution.SSN.value,
            EntityResolution.SSN_LAST4.value,
            EntityResolution.NIN.value,
            EntityResolution.NIN_COUNTRY.value,
            EntityResolution.TAX_ID_TYPE.value,
            EntityResolution.TAX_ID.value,
            EntityResolution.TAX_ID_COUNTRY.value,
            EntityResolution.OTHER_ID_TYPE.value,
            EntityResolution.OTHER_ID.value,
            EntityResolution.OTHER_ID_COUNTRY.value,
            EntityResolution.TRUSTED_ID_TYPE.value,
            EntityResolution.TRUSTED_ID.value,
            EntityResolution.ACCOUNT_NUMBER.value,
            EntityResolution.ACCOUNT_DOMAIN.value,
            EntityResolution.DUNS_NUMBER.value,
            EntityResolution.NPI_NUMBER.value,
            EntityResolution.LEI_NUMBER.value,
        ]

        self.digital_identifier_values = [
            EntityResolution.WEBSITE.value,
            EntityResolution.EMAIL.value,
            EntityResolution.LINKEDIN.value,
            EntityResolution.FACEBOOK.value,
            EntityResolution.TWITTER.value,
            EntityResolution.SKYPE.value,
            EntityResolution.ZOOMROOM.value,
            EntityResolution.INSTAGRAM.value,
            EntityResolution.WHATSAPP.value,
            EntityResolution.SIGNAL.value,
            EntityResolution.TELEGRAM.value,
            EntityResolution.TANGO.value,
            EntityResolution.VIBER.value,
            EntityResolution.WECHAT.value,
        ]

        self.group_associations_values = [
            EntityResolution.EMPLOYER.value,
            EntityResolution.GROUP_ASSOCIATION_TYPE.value,
            EntityResolution.GROUP_ASSOCATION_ORG_NAME.value,
            EntityResolution.GROUP_ASSN_ID_TYPE.value,
            EntityResolution.GROUP_ASSN_ID.value,
        ]

        self.physical_characteristics_values = [
            EntityResolution.GENDER.value,
            EntityResolution.DOB.value,
            EntityResolution.DOD.value,
            EntityResolution.POB.value,
            EntityResolution.NATIONALITY.value,
            EntityResolution.CITIZENSHIP.value,
            EntityResolution.REGISTRATION_DATE.value,
            EntityResolution.REGISTRATION_COUNTRY.value,
        ]

    def getParameterInfo(self):
        """Define parameter definitions"""
        in_table = arcpy.Parameter(
            displayName="Input Table",
            name="in_table",
            datatype=["GPFeatureLayer", "GPTableView"],
            parameterType="Required",
            direction="Input")

        in_entity_store = arcpy.Parameter(
            displayName="Input Local Entity Store",
            name="in_entity_store",
            datatype="DEFile",
            parameterType="Required",
            direction="Input")

        entity_type = arcpy.Parameter(
            displayName="Entity Type",
            name="entity_type",
            datatype="GPString",
            parameterType="Required",
            direction="Input")

        entity_type.filter.type = 'ValueList'
        entity_type.filter.list = [
            EntityResolution.PERSON.value,
            EntityResolution.ORG.value,
        ]

        name_type = arcpy.Parameter(
            displayName="Name Type",
            name="name_type",
            datatype="GPString",
            parameterType="Optional",
            direction="Input",
            category='Name')

        name_type.filter.type = 'ValueList'
        name_type.filter.list = [
            EntityResolution.PRIMARY.value,
            EntityResolution.AKA.value,
            EntityResolution.OTHER.value,
        ]        

        name_fields = arcpy.Parameter(
            displayName='Name Field(s)',
            name='name_fields',
            datatype='GPValueTable',
            parameterType='Optional',
            direction='Input',
            category='Name')

        name_fields.parameterDependencies = [in_table.name]
        name_fields.columns = [['Field', 'Field'], ['GPString', 'Attribute Type']]
        name_fields.filters[1].type = 'ValueList'
        name_fields.filters[1].list = self.name_values

        include_alias = arcpy.Parameter(
            displayName="Alias Type",
            name="alias_type",
            datatype="GPString",
            parameterType="Optional",
            direction="Input",
            category='Name')

        alias_fields = arcpy.Parameter(
            displayName='Alias Field(s)',
            name='alias_fields',
            datatype='GPValueTable',
            parameterType='Optional',
            direction='Input',
            category='Name')

        alias_fields.parameterDependencies = [in_table.name]
        alias_fields.columns = [['Field', 'Field'], ['GPString', 'Attribute Type']]
        alias_fields.filters[1].type = 'ValueList'
        alias_fields.filters[1].list = self.name_values

        address_type = arcpy.Parameter(
            displayName="Address Type",
            name="address_type",
            datatype="GPString",
            parameterType="Optional",
            direction="Input",
            category='Address')

        address_type.filter.type = 'ValueList'
        address_type.filter.list = [
            EntityResolution.HOME.value,
            EntityResolution.BUSINESS.value,
            EntityResolution.MAILING.value,
            EntityResolution.OTHER.value,
        ]
        
        address_fields = arcpy.Parameter(
            displayName='Address Field(s)',
            name='address_fields',
            datatype='GPValueTable',
            parameterType='Optional',
            direction='Input',
            category='Address')

        address_fields.parameterDependencies = [in_table.name]
        address_fields.columns = [['Field', 'Field'], ['GPString', 'Attribute Type']]
        address_fields.filters[1].type = 'ValueList'
        address_fields.filters[1].list = self.address_values

        alternate_address_type = arcpy.Parameter(
            displayName="Alternate Address Type",
            name="alternate_address_type",
            datatype="GPString",
            parameterType="Optional",
            direction="Input",
            category='Address')

        alternate_address_type.filter.type = 'ValueList'
        alternate_address_type.filter.list = [
            EntityResolution.HOME.value,
            EntityResolution.BUSINESS.value,
            EntityResolution.MAILING.value,
            EntityResolution.OTHER.value,
        ]

        alt_address_fields = arcpy.Parameter(
            displayName='Alternate Address Field(s)',
            name='alt_address_fields',
            datatype='GPValueTable',
            parameterType='Optional',
            direction='Input',
            category='Address')

        alt_address_fields.parameterDependencies = [in_table.name]
        alt_address_fields.columns = [['Field', 'Field'], ['GPString', 'Attribute Type']]
        alt_address_fields.filters[1].type = 'ValueList'
        alt_address_fields.filters[1].list = self.address_values

        phone_type = arcpy.Parameter(
            displayName="Phone Type",
            name="phone_type",
            datatype="GPString",
            parameterType="Optional",
            direction="Input",
            category='Phone Number')

        phone_type.filter.type = 'ValueList'
        phone_type.filter.list = self.phone_types

        phone_fields = arcpy.Parameter(
            displayName='Phone Field(s)',
            name='phone_fields',
            datatype='GPValueTable',
            parameterType='Optional',
            direction='Input',
            category='Phone Number')

        phone_fields.parameterDependencies = [in_table.name]
        phone_fields.columns = [['Field', 'Field'], ['GPString', 'Attribute Type']]
        phone_fields.filters[1].type = 'ValueList'
        phone_fields.filters[1].list = self.phone_values
        
        alt_phone_type = arcpy.Parameter(
            displayName="Alternate Phone Type",
            name="alt_phone_type",
            datatype="GPString",
            parameterType="Optional",
            direction="Input",
            category='Phone Number')

        alt_phone_type.filter.type = 'ValueList'
        alt_phone_type.filter.list = self.phone_types

        alt_phone_fields = arcpy.Parameter(
            displayName='Alternate Phone Field(s)',
            name='alt_phone_fields',
            datatype='GPValueTable',
            parameterType='Optional',
            direction='Input',
            category='Phone Number')

        alt_phone_fields.parameterDependencies = [in_table.name]
        alt_phone_fields.columns = [['Field', 'Field'], ['GPString', 'Attribute Type']]
        alt_phone_fields.filters[1].type = 'ValueList'
        alt_phone_fields.filters[1].list = self.phone_values

        identifier_fields = arcpy.Parameter(
            displayName='Identifier Field(s)',
            name='identifier_fields',
            datatype='GPValueTable',
            parameterType='Optional',
            direction='Input',
            category='Identifiers')

        identifier_fields.parameterDependencies = [in_table.name]
        identifier_fields.columns = [['Field', 'Field'], ['GPString', 'Attribute Type']]
        identifier_fields.filters[1].type = 'ValueList'
        identifier_fields.filters[1].list = self.identifier_values

        digital_identifier_fields = arcpy.Parameter(
            displayName='Digital Identifier Field(s)',
            name='digital_identifier_fields',
            datatype='GPValueTable',
            parameterType='Optional',
            direction='Input',
            category='Digital Identifiers')

        digital_identifier_fields.parameterDependencies = [in_table.name]
        digital_identifier_fields.columns = [['Field', 'Field'], ['GPString', 'Attribute Type']]
        digital_identifier_fields.filters[1].type = 'ValueList'
        digital_identifier_fields.filters[1].list = self.digital_identifier_values

        group_association_fields = arcpy.Parameter(
            displayName='Group Association Field(s)',
            name='group_association_fields',
            datatype='GPValueTable',
            parameterType='Optional',
            direction='Input',
            category='Group Associations')

        group_association_fields.parameterDependencies = [in_table.name]
        group_association_fields.columns = [['Field', 'Field'], ['GPString', 'Attribute Type']]
        group_association_fields.filters[1].type = 'ValueList'
        group_association_fields.filters[1].list = self.group_associations_values

        physical_characteristics_fields = arcpy.Parameter(
            displayName='Physical Characteristics Field(s)',
            name='physical_characteristics_fields',
            datatype='GPValueTable',
            parameterType='Optional',
            direction='Input',
            category='Physical Characteristics')

        physical_characteristics_fields.parameterDependencies = [in_table.name]
        physical_characteristics_fields.columns = [['Field', 'Field'], ['GPString', 'Attribute Type']]
        physical_characteristics_fields.filters[1].type = 'ValueList'
        physical_characteristics_fields.filters[1].list = self.physical_characteristics_values

        other_attribute_fields = arcpy.Parameter(
            displayName='Other Attribute Field(s)',
            name='other_attribute_fields',
            datatype='GPValueTable',
            parameterType='Optional',
            direction='Input',
            category='Other Attributes')

        other_attribute_fields.parameterDependencies = [in_table.name]
        other_attribute_fields.columns = [['Field', 'Field'], ['GPString', 'Attribute Type']]


        in_entity_feature_store = arcpy.Parameter(
            displayName="Input Local Entity Feature Store",
            name="in_entity_feature_store",
            datatype="DEWorkspace",
            parameterType="Required",
            direction="Input")
 
        params = [
            in_table,                        #0
            in_entity_store,                 #1
            in_entity_feature_store,         #2
            entity_type,                     #3
            name_type,                       #4
            name_fields,                     #5
            include_alias,                   #6
            alias_fields,                    #7
            address_type,                    #8
            address_fields,                  #9
            alternate_address_type,          #10
            alt_address_fields,              #11
            phone_type,                      #12
            phone_fields,                    #13
            alt_phone_type,                  #14
            alt_phone_fields,                #15
            identifier_fields,               #16
            digital_identifier_fields,       #17
            group_association_fields,        #18
            physical_characteristics_fields, #19
            other_attribute_fields,          #20

        ]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        from entity_resolution import AddRecordToEntityStore

        """
        identifier_fields,               #16
        digital_identifier_fields,       #17
        group_association_fields,        #18
        physical_characteristics_fields, #19
        other_attribute_fields,          #20"""

        try:
            result = AddRecordToEntityStore()\
                        .source_table(parameters[0].valueAsText)\
                        .entity_store(parameters[1].valueAsText)\
                        .feature_store(parameters[2].valueAsText)\
                        .entity_type(parameters[3].valueAsText)\
                        .name_fields(name_type=parameters[4].valueAsText, name_fields=parameters[5].value)\
                        .address_fields(address_type=parameters[8].valueAsText, address_fields=parameters[9].value)\
                        .alias_fields(alias_type=parameters[6].valueAsText, alias_fields=parameters[7].value)\
                        .alternate_address_fields(address_type=parameters[10].valueAsText, address_fields=parameters[11].value)\
                        .phone_fields(phone_type=parameters[12].valueAsText, phone_fields=parameters[13].value)\
                        .alternate_phone_fields(phone_type=parameters[14].valueAsText, phone_fields=parameters[15].value)\
                        .identifier_fields(parameters[16].value)\
                        .digital_identifier_fields(parameters[17].value)\
                        .group_association_fields(parameters[18].value)\
                        .physical_characteristics(parameters[19].value)\
                        .other_attributes(parameters[20].value)\
                        
            result.add_records.execute()

            if result:
                arcpy.AddMessage("Add Records completed successfully")
            elif not result:
                arcpy.AddError("Add Records finished with an exit code of 1.")
                   
            
        except Exception as e:
            arcpy.AddError("Error in tool class")

            import sys
            import traceback
            
            tb = sys.exc_info()[2]
            tbinfo = traceback.format_tb(tb)[0]
            pymsg = '{}\n{}\n{}'.format(tbinfo,
                                        str(sys.exc_info()[1]),
                                        arcpy.GetMessages(2))
            
            arcpy.AddError(e.__class__.__name__)
            arcpy.AddError(pymsg)
            exit()     


class SearchLocalEntityStore:
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Search Local Entity Store"
        self.description = ""
        self.canRunInBackground = False

        self.field_values = [
            EntityResolution.NAME_FULL.value,
            EntityResolution.NAME_ORG.value,
            EntityResolution.NAME_LAST.value,
            EntityResolution.NAME_FIRST.value,
            EntityResolution.NAME_MIDDLE.value,
            EntityResolution.NAME_PREFIX.value,
            EntityResolution.NAME_SUFFIX.value,
            EntityResolution.ADDR_FULL.value,
            EntityResolution.ADDR_LINE1.value,
            EntityResolution.ADDR_LINE2.value,
            EntityResolution.ADDR_LINE3.value,
            EntityResolution.ADDR_LINE4.value,
            EntityResolution.ADDR_LINE5.value,
            EntityResolution.ADDR_LINE6.value,
            EntityResolution.ADDR_CITY.value,
            EntityResolution.ADDR_STATE.value,
            EntityResolution.ADDR_ZIP.value,
            EntityResolution.ADDR_COUNTRY.value,
            EntityResolution.ADDR_FD.value,
            EntityResolution.ADDR_TD.value,
            EntityResolution.PHONE_NUM.value,
            EntityResolution.PHONE_FD.value,
            EntityResolution.PHONE_TD.value,
            EntityResolution.PASSPORT.value,
            EntityResolution.PASSPORT_COUNTRY.value,
            EntityResolution.DRIVERS_LICENSE.value, 
            EntityResolution.DRIVERS_LICENSE_STATE.value,
            EntityResolution.SSN.value,
            EntityResolution.SSN_LAST4.value,
            EntityResolution.NIN.value,
            EntityResolution.NIN_COUNTRY.value,
            EntityResolution.TAX_ID_TYPE.value,
            EntityResolution.TAX_ID.value,
            EntityResolution.TAX_ID_COUNTRY.value,
            EntityResolution.OTHER_ID_TYPE.value,
            EntityResolution.OTHER_ID.value,
            EntityResolution.OTHER_ID_COUNTRY.value,
            EntityResolution.TRUSTED_ID_TYPE.value,
            EntityResolution.TRUSTED_ID.value,
            EntityResolution.ACCOUNT_NUMBER.value,
            EntityResolution.ACCOUNT_DOMAIN.value,
            EntityResolution.DUNS_NUMBER.value,
            EntityResolution.NPI_NUMBER.value,
            EntityResolution.LEI_NUMBER.value,
            EntityResolution.WEBSITE.value,
            EntityResolution.EMAIL.value,
            EntityResolution.LINKEDIN.value,
            EntityResolution.FACEBOOK.value,
            EntityResolution.TWITTER.value,
            EntityResolution.SKYPE.value,
            EntityResolution.ZOOMROOM.value,
            EntityResolution.INSTAGRAM.value,
            EntityResolution.WHATSAPP.value,
            EntityResolution.SIGNAL.value,
            EntityResolution.TELEGRAM.value,
            EntityResolution.TANGO.value,
            EntityResolution.VIBER.value,
            EntityResolution.WECHAT.value,
            EntityResolution.EMPLOYER.value,
            EntityResolution.GROUP_ASSOCIATION_TYPE.value,
            EntityResolution.GROUP_ASSOCATION_ORG_NAME.value,
            EntityResolution.GROUP_ASSN_ID_TYPE.value,
            EntityResolution.GROUP_ASSN_ID.value,
        ]


    def getParameterInfo(self):
        """Define parameter definitions"""

        in_entity_store = arcpy.Parameter(
            displayName="Input Local Entity Store",
            name="in_entity_store",
            datatype="DEFile",
            parameterType="Required",
            direction="Input")

        search_terms = arcpy.Parameter(
            displayName='Search Terms',
            name='search_terms',
            datatype='GPValueTable',
            parameterType='Required',
            direction='Input')

        search_terms.columns = [['GPString', 'Value'], ['GPString', 'Attribute Type']]
        search_terms.filters[1].type = 'ValueList'
        search_terms.filters[1].list = self.field_values

        params = [
            in_entity_store,
            search_terms,
        ]

        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""

        from entity_resolution import SearchRecords
        
        sr = SearchRecords(parameters[0].valueAsText,
                           parameters[1].value)

        sr.search()
        
        return


class ExportLocalEntityStore:
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Export Local Entity Store"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        
        in_entity_store = arcpy.Parameter(
            displayName="Input Local Entity Store",
            name="in_entity_store",
            datatype="DEFile",
            parameterType="Required",
            direction="Input")

        out_entity_file = arcpy.Parameter(
            displayName="Out Entity File",
            name="out_entity_file",
            datatype="DEWorkspace",
            parameterType="Required",
            direction="Input")
        
        params = [
            in_entity_store,
            out_entity_file,
        ]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""

        from entity_resolution import ExportRecords
        
        er = ExportRecords(parameters[0].valueAsText, parameters[1].valueAsText)

        er.export()

        return


class CreateLocalEntityStore:
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Create Local Entity Store"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        
        entity_store_location = arcpy.Parameter(
            displayName="Local Entity Store Location",
            name="entity_store_location",
            datatype="DEWorkspace",
            parameterType="Required",
            direction="Input")

        entity_store_location.filter.list = ['File System']

        entity_store_name = arcpy.Parameter(
            displayName="Local Entity Store Name",
            name="entity_store_name",
            datatype="GPString",
            parameterType="Required",
            direction="Output")
        
        params = [entity_store_location, entity_store_name]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        from entity_resolution import CreateEntityStore

        ces = CreateEntityStore(parameters[0].valueAsText, parameters[1].valueAsText)
        ces.create()

        return


class FindRelationshipsFromArea:
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Find Relationships From Area"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        in_feature_set = arcpy.Parameter(
            displayName="Input Feature Set",
            name="in_feature_set",
            datatype="GPFeatureRecordSetLayer",
            parameterType="Required",
            direction="Input")

        in_entity_feature_store = arcpy.Parameter(
            displayName="Input Local Entity Feature Store",
            name="in_entity_feature_store",
            datatype="DEWorkspace",
            parameterType="Optional",
            direction="Input")

        in_entity_store = arcpy.Parameter(
            displayName="Input Local Entity Store",
            name="in_entity_store",
            datatype="DEFile",
            parameterType="Required",
            direction="Input")

        out_workspace = arcpy.Parameter(
            displayName="Out Workspace",
            name="out_workspace",
            datatype="DEWorkspace",
            parameterType="Optional",
            direction="Input")
        
        params = [
            in_feature_set, 
            in_entity_feature_store,
            in_entity_store,
            out_workspace
        ]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        from entity_resolution import RelationshipsFromArea

        rfa = RelationshipsFromArea(parameters[0].value, parameters[1].valueAsText, parameters[2].valueAsText, parameters[3].valueAsText)

        rfa.find()
        
        return


class ProcessRedoRecords:
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Process Redo Records"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        
        in_entity_store = arcpy.Parameter(
            displayName="Input Local Entity Store",
            name="in_entity_store",
            datatype="DEFile",
            parameterType="Required",
            direction="Input")

       
        params = [
            in_entity_store,
        ]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""

        from entity_resolution import RedoRecords
        
        redo = RedoRecords(parameters[0].valueAsText)

        redo.process()

        return